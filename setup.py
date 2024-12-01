from setuptools import setup, find_packages

setup(
    name="pdf_editor_app",
    packages=find_packages(),
    # gérer les numéro de versions automatiquement
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
