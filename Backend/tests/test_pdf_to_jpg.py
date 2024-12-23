import unittest

from pathlib import Path
from pypdf import PdfReader

from Backend.pdf_operations import pdf_to_jpg


class TestPDFToJPGConversion(unittest.TestCase):
    def setUp(self) -> None:
        # Création d'un dossier temporaire pour les tests
        self.test_output_folder = Path("Backend/tests/resources/output_jpgs")
        self.test_output_folder.mkdir(exist_ok=False)
        self.test_pdf = Path("Backend/tests/resources/Python-w1.pdf")

    def tearDown(self) -> None:
        # Nettoyage après les tests
        for item in self.get_jpg_files():
            item.unlink()
        self.test_output_folder.rmdir()

    def get_jpg_files(self):
        return list(self.test_output_folder.glob("*.jpg"))

    def test_pdf_to_jpg_conversion(self) -> None:
        pdf_to_jpg(self.test_pdf, self.test_output_folder)
        # Vérifier que le nombre de fichiers jpg dans le dossier de sortie correspond au nombre
        # de pages du pdf d'entrée
        reader = PdfReader(self.test_pdf)
        num_pages = reader.get_num_pages()
        self.assertEqual(len(self.get_jpg_files()), num_pages)
        # Vérification des noms de fichiers générés
        expected_files = {self.test_output_folder / f"page_{i + 1}.jpg" for i in range(num_pages)}
        actual_files = set(self.get_jpg_files())
        # s'assurer que les fichiers créés correspondent aux fichiers attendus
        self.assertTrue(all([file in expected_files for file in actual_files]))
        self.assertEqual(len(expected_files), len(actual_files))

    def test_non_existing_pdf_conversion(self) -> None:
        non_existing_pdf = Path("non_existing_pdf.pdf")
        with self.assertRaises(FileNotFoundError):
            pdf_to_jpg(non_existing_pdf, self.test_output_folder)
        # Vérifier qu'il n'y a pas de fichiers JPG créés
        self.assertEqual(len(self.get_jpg_files()), 0)


if __name__ == "__main__":
    unittest.main()
