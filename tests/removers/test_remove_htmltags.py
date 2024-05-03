from textprepper.removers import RemoveHTMLTags
from textprepper.base import DocumentPreprocessorPipe
from pathlib import Path

import pytest
from ..utils import create_documents_with_simple_metadata, get_file_paths_with_ext


@pytest.fixture
def input_strings():
    texts = []
    file_path = Path(__file__).parent / Path("data/html")
    paths = get_file_paths_with_ext(file_path)
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        texts.append(text)
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture
def setup_processor():
    processor = RemoveHTMLTags()  # Default behavior
    return processor


@pytest.fixture
def results():
    results = [
        "\n\n\n\nMy First Heading\n\nMy first paragraph.\n\n\n\n\n",
        "\n\n\n\nThis is a heading\nThis is a paragraph.\n\n\n\n\n",
    ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_rm_emoji_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_emoji_in_doc(input_documents, setup_processor, doc_results):
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
