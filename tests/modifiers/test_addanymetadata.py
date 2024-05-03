from textprepper.modifiers import AddAnyMetadata
from textprepper.base import DocumentPreprocessorPipe

import pytest
from ..utils import create_documents_with_simple_metadata


@pytest.fixture
def input_strings():
    texts = ["Hello", "HELLO WORLD", "@I Like APPles", "12345 iS a NUMber"]
    return texts


@pytest.fixture()
def results(input_strings):
    results = input_strings
    return results


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture
def dummy_metadata():
    return {"Test": 1, "Test_2": "Hello"}


@pytest.fixture
def doc_results(results, dummy_metadata):
    docs = create_documents_with_simple_metadata(results)
    for doc in docs:
        doc.metadata.update(dummy_metadata)
    return docs


@pytest.fixture
def setup_processor(dummy_metadata):
    return AddAnyMetadata(metadata=dummy_metadata)


def test_lower_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_lower_doc(input_documents, setup_processor, doc_results):
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
