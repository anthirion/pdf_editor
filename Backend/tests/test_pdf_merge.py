import unittest
from pathlib import Path

from pypdf import PdfReader

from Backend.pdf_operations import merge_pdf


class TestPDFMerge(unittest.TestCase):

    def setUp(self):
        output_folder_path = Path("/home/thiran/projets_persos/pdf_editor/tests/")
        # Configure les chemins pour les tests
        output_folder_path.mkdir(parents=True, exist_ok=True)
        self.test_output = output_folder_path / Path("test_output.pdf")
        self.test_pdf1 = output_folder_path / Path("attestation_suivi_cours_python.pdf")
        self.test_pdf2 = output_folder_path / Path("Python-w1.pdf")

        # Crée des fichiers PDF pour les tests
        self.test_pdf1.touch()
        self.test_pdf2.touch()

    def tearDown(self):
        # Nettoyer les fichiers temporaires créés après le test
        self.test_output.unlink(missing_ok=True)

    def test_merge_two_pdfs(self):
        merge_pdf(self.test_output, [self.test_pdf1, self.test_pdf2])
        self.assertTrue(self.test_output.exists())
        # Vérifie que le nombre de pages du pdf fusionné est égal à la somme des pages
        # des pdfs d'entrée
        reader = PdfReader(self.test_output)
        self.assertEqual(reader.get_num_pages(),
                         totalpage_count(self.test_pdf1, self.test_pdf2)
                         )

    def test_merge_empty_list(self):
        with self.assertRaises(ValueError):
            merge_pdf(self.test_output, [])
        self.assertFalse(self.test_output.exists())  # Pas de fichier créé pour une liste vide

    def test_nonexistent_file_in_list(self):
        nonexistent_pdf = Path("nonexistent.pdf")
        merge_pdf(self.test_output, [nonexistent_pdf])
        self.assertFalse(self.test_output.exists())


def totalpage_count(pdf_path1: Path, pdf_path2: Path) -> int:
    """
    Calcule le nombre total de pages de deux fichiers PDF.

    :param pdf_path1: Chemin du premier fichier PDF.
    :param pdf_path2: Chemin du deuxième fichier PDF.
    :return: Somme du nombre de pages des deux PDF.
    """
    pdf1 = PdfReader(pdf_path1)
    pdf2 = PdfReader(pdf_path2)
    return pdf1.get_num_pages() + pdf2.get_num_pages()


# Exécution des tests
if __name__ == "__main__":
    unittest.main()
