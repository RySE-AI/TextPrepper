import abc
from typing import List, Dict, Union
from pydantic import BaseModel

from langchain_core.documents import Document


class Preprocessor(BaseModel, abc.ABC):
    """Abstract base class to create a Langchain Document preprocessor.
    Inherit from the class and change the preprocess method.

    Example:
    class AddABC123ToMetadata(Preprocessor):
        def preprocess_page(self, doc, *args, **kwargs):
            doc.metadata.update({"ABC": 123})
            return doc

    for doc in documents: # LangChain Documents
        doc = AddABC123ToMetadata(doc)
    """

    def __call__(self, content: Union[str, Document], *args, **kwargs) -> Union[str, Document]:
        if isinstance(content, Document):
            out = self.process_document(content, *args, **kwargs)
        elif isinstance(content, str):
            out = self.process_text(content, *args, **kwargs)
        else:
            raise ValueError("The input must be a LangChain Document or a string")

        return out

    def process_document(self, doc: Document, *args, **kwargs) -> Document:
        doc.metadata.update(self.add_metadata(doc, **kwargs))
        doc.page_content = self.process_text(doc.page_content, *args, **kwargs)
        return doc

    def add_metadata(self, doc: Document, **kwargs) -> Dict:
        return {}

    @abc.abstractmethod
    def process_text(self, text: str, *args, **kwargs) -> str:
        pass


class DocumentPreprocessorPipe:
    """Composes several preprocessors together.

    Args:
        preprocessors (List[Preprocessor]): A list of preprocessors which will be
        applied sequentially to a document.

    Example:
        compose = PreprocessorComposer(
                preprocessors=[
                            RemoveHeader(),
                            SimpleDehyphens(),
                            RemoveStartingNumbers(),
                            AddSectionNamesWithTOC(file_path=file_path)])

        for doc in documents: # LangChain Documents
            doc = compose(doc)
    """

    def __init__(self, preprocessors) -> None:
        self.preprocessors: List[Preprocessor] = preprocessors

    def __call__(self, input: Union[str, Document], *args, **kwargs) -> Union[str, Document]:
        for p in self.preprocessors:
            input = p(input, *args, **kwargs)

        return input
    
    def from_documents(self, docs: List[Document]) -> List[Document]:
        return [self(doc) for doc in docs]
