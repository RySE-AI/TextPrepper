from langchain_core.documents import Document
from pathlib import Path

from typing import List


def create_documents_with_simple_metadata(strings):
    docs = []
    for i, text in enumerate(strings):
        doc = Document(page_content=text, metadata={"page": i})
        docs.append(doc)
    return docs


def get_file_paths_with_ext(dir_path: str, ext: str = "html") -> List[str]:
    """
    Recursively finds all PDF files in the given directory and its subfolders
    using glob and pathlib.
    """
    base_path = Path(dir_path)
    pdf_files = list(base_path.rglob(f"*.{ext}"))
    pdf_file_paths = [str(pdf) for pdf in pdf_files]
    return pdf_file_paths