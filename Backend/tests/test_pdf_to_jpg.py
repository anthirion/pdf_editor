import unittest
from pathlib import Path
from pdf2image import convert_from_path
from pypdf import PdfReader

from Backend.pdf_operations import pdf_to_jpg

class TestPDFToJPGConversion(unittest.TestCase):
    def setUp(self):
        # Création d'un dossier temporaire pour les tests
        self.test_output_folder = Path("/home/thiran/projets_persos/pdf_editor/tests/test_output_folder")
        self.test_output_folder.mkdir(exist_ok=True)
        self.test_pdf = Path("/home/thiran/projets_persos/pdf_editor/tests/Python-w1.pdf")

    def tearDown(self):
        # Nettoyage après les tests
        for item in self.test_output_folder.glob("*.jpg"):
            item.unlink()
        self.test_output_folder.rmdir()

    def test_pdf_to_jpg_conversion(self):
        # Appel de la fonction avec le fichier PDF de test
        pdf_to_jpg(self.test_pdf, self.test_output_folder)

        # Vérification de la présence des fichiers jpg dans le dossier de sortie
        jpg_files = list(self.test_output_folder.glob("*.jpg"))
        # Vérifier que le nombre de fichiers jpg dans le dossier de sortie correspond au nombre
        # de pages du pdf d'entrée
        reader = PdfReader(self.test_pdf)
        num_pages = reader.get_num_pages()
        self.assertEqual(len(jpg_files), num_pages)

        # Vérification des noms de fichiers générés
        expected_files = {self.test_output_folder / f"page_{i+1}.jpg" for i in range(num_pages)}
        actual_files = set(jpg_files)
        self.assertEqual(actual_files, expected_files)

    def test_non_existing_pdf_conversion(self):
        # Test avec un PDF vide
        non_existing_pdf = Path("non_existing_pdf.pdf")
        with self.assertRaises(FileNotFoundError):
            pdf_to_jpg(non_existing_pdf, self.test_output_folder)

        # Vérifie qu'il n'y a pas de fichiers JPG créés
        jpg_files = list(self.test_output_folder.glob("*.jpg"))
        self.assertEqual(len(jpg_files), 0)

if __name__ == "__main__":
    unittest.main()
