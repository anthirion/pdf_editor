from pypdf import PdfMerger
from PIL import Image
from typing import List


def merge_pdf(output_path: str, *pdf_paths) -> None:
    """
    Fusionne plusieurs fichiers PDF en un seul.

    :param output_path: Chemin du fichier de sortie.
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


def split_pdf():
    pass


def pdf_to_jpg():
    pass


def jpg_to_pdf(jpg_files_list: List[str], pdf_path: str) -> str:
    """Convertit des images au format jpg en un fichier pdf

    :param jpg_files_list: liste de fichiers jpg
    :param pdf_path: chemin du fichier pdf à créer
    :return une chaine de caractères indiquant l'erreur produite ou
    "NO_ERROR" si pas d'erreur
    """
    try:
        images = [Image.open(jpg) for jpg in jpg_files_list]

        images[0].save(pdf_path, "PDF",
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
