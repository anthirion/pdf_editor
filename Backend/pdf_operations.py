from pypdf import PdfMerger


def merge_pdf(output_path, *pdf_paths):
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


def jpg_to_pdf():
    pass
