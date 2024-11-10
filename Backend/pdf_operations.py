from pathlib import Path
import pdf2image
from pypdf import PdfMerger, PdfReader
from PIL import Image

import global_variables as GV


def text_occurences(file_path: str, search: str) -> int:
    """
    Cherche le mot ou groupe de mots 'search' dans le pdf
    @param search: mot ou groupe de mots à chercher
    @param file_path: chemin vers le fichier où chercher le mot
    """
    global_occurences = 0
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        occurences_on_page = text.count(search)
        if occurences_on_page > 0:
            global_occurences += occurences_on_page
    return global_occurences


def merge_pdf(output_path: str, pdf_paths: list[str]):
    """
    Fusionne plusieurs fichiers PDF en un seul.

    :param output_path: Chemin du fichier obtenu après fusion
    :param pdf_paths: Liste des chemins des fichiers PDF à fusionner.
    """
    merger = PdfMerger()

    try:
        # Ajouter chaque fichier PDF à la fusion
        for pdf in pdf_paths:
            merger.append(pdf)

        # Écrire le fichier fusionné dans le fichier de sortie
        with open(output_path, 'wb') as output_pdf:
            merger.write(output_pdf)

    except Exception as e:
        print(f"Erreur lors de la fusion des PDF : {str(e)}")

    finally:
        merger.close()


def split_pdf(output_path: str, pdf_path: str):
    pass


def pdf_to_jpg(pdf_path: str, output_folder: str = GV.output_folder) -> None:
    """
    Convertit chaque page d'un fichier pdf en images jpg
    :param pdf_path: chemin vers le fichier pdf à convertir
    :param output_folder: chemin vers le dossier contenant les images jpg issues de la conversion
    """
    output_folder_path = Path(output_folder)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    images = pdf2image.convert_from_path(pdf_path)
    for page_num, image in enumerate(images):
        jpg_path = output_folder_path / f"page_{page_num+1}.jpg"
        image.save(jpg_path, "JPEG")


def jpg_to_pdf(output_pdf_path: str, jpg_files_list: list[str]) -> str:
    """
    Retourne une chaine de caractères indiquant l'erreur produite ou
    "NO_ERROR" si pas d'erreur
    :param output_pdf_path: chemin du fichier obtenu après conversion
    :param jpg_files_list: liste de chemins vers des fichiers jpg à convertir
    """
    try:
        images = [Image.open(jpg) for jpg in jpg_files_list]

        images[0].save(output_pdf_path, "PDF",
                       resolution=100.0,
                       save_all=True,
                       append_images=images[1:]
                       )
        return "NO_ERROR"
    except FileNotFoundError:
        return "FILE_NOT_FOUND"
    except OSError:
        return "INVALID_IMAGE"
    except PermissionError:
        return "PERMISSION_DENIED_WHEN_SAVING_FILE"
