from textprepper.base import Preprocessor
from langchain_core.documents import Document

import pytest


class SimplePreprocessor(Preprocessor):
    def process_text(self, text: str, *args, **kwargs) -> str:
        return text


@pytest.fixture
def input():
    return "Basic Test"


@pytest.fixture
def input_document(input):
    return Document(page_content=input, metadata={"Test": "Test"})


@pytest.fixture
def preprocessor():
    return SimplePreprocessor()


def test_preprocessor_with_document(input_document, preprocessor):
    doc = preprocessor(input_document)
    
    assert doc.page_content == "Basic Test"
    assert doc.metadata == {"Test": "Test"}
    
    
def test_preprocessor_with_string(input, preprocessor):
    str_result = preprocessor(input)
    
    assert str_result == "Basic Test"


def test_preprocessor_with_invalid_input(preprocessor):
    with pytest.raises(ValueError):
        preprocessor(123)
        
        
def test_abstract_base_class_instantiation():
    with pytest.raises(TypeError):
        p = Preprocessor() 