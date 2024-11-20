import unittest
from pathlib import Path

from Backend.pdf_operations import jpg_to_pdf


class TestJPGToPDFConversion(unittest.TestCase):
    def setUp(self) -> None:
        # Dossier stockant les fichiers JPG à convertir
        self.test_folder = Path("/home/thiran/projets_persos/pdf_editor/tests")
        self.test_input_folder = self.test_folder / Path("ilovepdf_pages-to-jpg")
        self.test_input_folder.mkdir(exist_ok=True)
        # liste des fichiers JPG à convertir
        self.jpg_files = list(self.test_input_folder.glob("*.jpg"))
        # Chemin du fichier PDF de sortie
        self.output_pdf_path = self.test_folder / "output.pdf"

    def tearDown(self) -> None:
        # Supprimer le fichier PDF de sortie créé après chaque test
        self.output_pdf_path.unlink(missing_ok=True)

    def test_jpg_to_pdf_conversion(self) -> None:
        # Conversion des fichiers JPG en PDF
        jpg_to_pdf(self.output_pdf_path, self.jpg_files)
        # Vérification que le fichier PDF est bien créé
        self.assertTrue(self.output_pdf_path.exists())

    def test_empty_jpg_list(self) -> None:
        # Test avec une liste de fichiers JPG vide
        with self.assertRaises(ValueError):
            jpg_to_pdf(self.output_pdf_path, [])

    def test_file_not_found(self) -> None:
        # Test avec un fichier JPG manquant
        missing_file = self.test_input_folder / "missing_image.jpg"
        with self.assertRaises(FileNotFoundError):
            jpg_to_pdf(self.output_pdf_path, [missing_file])

    def test_invalid_file_format(self) -> None:
        # Crée un fichier texte au lieu d'une image JPG pour simuler une erreur de format
        invalid_file = self.test_input_folder / "invalid_file.txt"
        invalid_file.write_text("This is not a valid image file.")
        with self.assertRaises(OSError):
            jpg_to_pdf(self.output_pdf_path, [invalid_file])


if __name__ == "__main__":
    unittest.main()
