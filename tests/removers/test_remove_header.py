from textprepper.removers import RemoveHeader
from textprepper.base import DocumentPreprocessorPipe

import pytest
from langchain_core.documents import Document

from ..utils import create_documents_with_simple_metadata

@pytest.fixture
def input_strings():
    texts = [
        "This is the header of a page\nThe real Title starts here",
        """Header
        Paragraph starts here about stuff
        2nd Paragraph starts afterwards
        3nd Paragraph\tuses a tab
        Here starts the footer""",
        "Only remove this\nNot\nThis\nLines",
        "no change",
        ""
    ]
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture
def setup_processor():
    return RemoveHeader()


@pytest.fixture
def results():
    results = [
        "The real Title starts here",
        """        Paragraph starts here about stuff
        2nd Paragraph starts afterwards
        3nd Paragraph\tuses a tab
        Here starts the footer""",
        "Not\nThis\nLines",
        "no change",
        ""
    ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_process_text_method(setup_processor):
    pass


def test_rm_header_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_header_in_doc(input_documents, setup_processor, doc_results):
    transformed = [setup_processor(doc) for doc in input_documents]

    assert len(doc_results) == len(transformed), "The Length are not equal"
    assert all(
        [
            result.page_content == transform.page_content
            for result, transform in zip(doc_results, transformed)
        ]
    ), "The strings of the processor aren't equal with the expected results"
    assert all(
        [
            result.metadata == transform.metadata
            for result, transform in zip(doc_results, transformed)
        ]
    ), "The metadata should be equal"


def test_processor_in_pipe(input_documents, setup_processor, doc_results):
    doc_pipe = DocumentPreprocessorPipe([setup_processor])
    transformed = [doc_pipe(doc) for doc in input_documents]

    assert len(doc_results) == len(transformed), "The Length are not equal"
    assert all(
        [
            result.page_content == transform.page_content
            for result, transform in zip(doc_results, transformed)
        ]
    ), "The strings of the processor aren't equal with the expected results"
    assert all(
        [
            result.metadata == transform.metadata
            for result, transform in zip(doc_results, transformed)
        ]
    ), "The metadata should be equal"
