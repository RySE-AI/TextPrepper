import abc
from typing import List, Dict, Union
from pydantic import BaseModel

from langchain_core.documents import Document


class Preprocessor(BaseModel, abc.ABC):
    """Abstract base class to create a Langchain Document/string preprocessor.
    Inherit from the class and change the preprocess_text method for your purpose.
    Please be aware of that changes on documents are inplace, the process_document
    method
    

    Example:
    class LowerTextAndAdd123ToMetadata(Preprocessor):
        def preprocess_text(self, text, *args, **kwargs):
            text = text.lower()
            return text
        
        def add_metadata(self, doc: Document, **kwargs)
            return {"123": "ABC"}
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
    """Composes several preprocessors together and call the pipe on strins and
    langchain documents. THh pipe performs the preprocessors sequentially.

    Args:
        preprocessors (List[Preprocessor]): A list of preprocessors which will be
        applied sequentially to a document.

    Example:
        doc_pipe = DocumentPreprocessorPipe(
                            [LowerText(),
                            RemoveNewLines(count=1),
                            RemoveWhitespace()])

        doc_pipe(single_text_or_document)
        doc_pipe.from_documents(your_documents)
    """

    def __init__(self, preprocessors) -> None:
        self.preprocessors: List[Preprocessor] = preprocessors

    def __call__(self, input: Union[str, Document], *args, **kwargs) -> Union[str, Document]:
        for p in self.preprocessors:
            input = p(input, *args, **kwargs)

        return input
    
    def from_documents(self, docs: List[Document]) -> List[Document]:
        return [self(doc) for doc in docs]
