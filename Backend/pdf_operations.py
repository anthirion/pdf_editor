from pathlib import Path

import pdf2image
from PIL import Image
from pypdf import PdfWriter, PdfReader

import global_variables as GV


def text_occurences(file_path: Path, search: str) -> int:
    """
    Cherche le mot ou groupe de mots 'search' dans le pdf
    @param search: mot ou groupe de mots à chercher
    @param file_path: chemin vers le fichier où chercher le mot
    """
    if file_path.exists() and search:
        try:
            global_occurences = 0
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                occurences_on_page = text.count(search)
                if occurences_on_page > 0:
                    global_occurences += occurences_on_page
            return global_occurences
        except:
            raise Exception("[text_occurences] Erreur lors de la décompte du nombre de mots")
    else:
        raise FileExistsError(f"[text_occurences] {GV.file_exists_error_msg}")


def merge_pdf(output_path: Path, pdf_paths: list[Path]):
    """
    Fusionne plusieurs fichiers PDF en un seul.

    :param output_path: Chemin du fichier obtenu après fusion
    :param pdf_paths: Liste des chemins des fichiers PDF à fusionner.
    """
    if pdf_paths:
        # pdf_paths_correct indique si la liste de fichiers pdf contient
        # au moins un fichier existant
        pdf_paths_correct = False
        if not output_path.exists():
            output_path.touch()

        merger = PdfWriter()
        try:
            # Ajouter chaque fichier PDF à la fusion
            for pdf in pdf_paths:
                if pdf.exists():
                    pdf_paths_correct = True
                    merger.append(pdf)
            # Écrire le fichier fusionné dans le fichier de sortie
            with open(output_path, 'wb') as output_pdf:
                merger.write(output_pdf)
        except Exception as e:
            print(f"Erreur lors de la fusion des PDF : {str(e)}")
        finally:
            if not pdf_paths_correct:
                output_path.unlink()
            merger.close()
    else:
        raise ValueError(f"[merge_pdf] {GV.empty_list_error_msg}")


def split_pdf(output_path: Path, pdf_path: Path):
    pass


def pdf_to_jpg(pdf_path: Path, output_folder_path: Path = GV.output_folder) -> None:
    """
    Convertit chaque page d'un fichier pdf en images jpg
    :param pdf_path: chemin vers le fichier pdf à convertir
    :param output_folder_path: chemin vers le dossier contenant les images jpg issues de la conversion
    """
    if pdf_path.exists():
        try:
            output_folder_path.mkdir(parents=True, exist_ok=True)
            images = pdf2image.convert_from_path(pdf_path)
            for page_num, image in enumerate(images):
                jpg_path = output_folder_path / f"page_{page_num + 1}.jpg"
                image.save(jpg_path, "JPEG")
        except:
            raise Exception(
                "[pdf_to_jpg] Erreur lors de la conversion : vérifiez que le fichier PDF fourni est correct")
    else:
        raise FileNotFoundError(f"[pdf_to_jpg] {GV.file_not_found_error_msg}")


def jpg_to_pdf(output_pdf_path: Path, jpg_files_list: list[Path]) -> None:
    """
    :param output_pdf_path: chemin du fichier obtenu après conversion
    :param jpg_files_list: liste de chemins vers des fichiers jpg à convertir
    :return chaine de caractères indiquant l'erreur produite ou
    "NO_ERROR" si pas d'erreur
    """
    if jpg_files_list:
        try:
            images = [Image.open(jpg) for jpg in jpg_files_list]

            images[0].save(output_pdf_path, "PDF",
                           resolution=100.0,
                           save_all=True,
                           append_images=images[1:]
                           )
        except FileNotFoundError:
            raise FileNotFoundError(f"[jpg_to_pdf] {GV.file_not_found_error_msg}")
        except OSError:
            raise OSError("[jpg_to_pdf] Image invalide")
    else:
        raise ValueError(f"[jpg_to_pdf] {GV.empty_list_error_msg}")
