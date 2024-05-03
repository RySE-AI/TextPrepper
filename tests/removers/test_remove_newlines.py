from textprepper.removers import RemoveNewLines
from textprepper.base import DocumentPreprocessorPipe

import pytest
from ..utils import create_documents_with_simple_metadata


@pytest.fixture
def input_strings():
    texts = [
        "Hello\n\n\nWorld\n\n\n\nThis is\n a test\n\n\n\n\n",
        "\n\n\n",
        "Only remove this\n\n\nNot\n\nThis\nLines",
        "no change",
        "",
    ]
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture(params=["default", "double", "triple"])
def processor_options(request):
    return request.param


@pytest.fixture
def setup_processor(processor_options):
    if processor_options == "default":
        processor = RemoveNewLines()  # ONLY Single New Lines
    elif processor_options == "double":
        processor = RemoveNewLines(count=2)  # ONLY Double New Lines
    elif processor_options == "triple":
        processor = RemoveNewLines(count=3)  # ONLY Triple New Lines

    return processor


@pytest.fixture
def results(processor_options):
    if processor_options == "default":
        results = [
            "Hello\n\n\nWorld\n\n\n\nThis is a test\n\n\n\n\n",
            "\n\n\n",
            "Only remove this\n\n\nNot\n\nThisLines",
            "no change",
            "",
        ]
    elif processor_options == "double":
        results = [
            "Hello\n\n\nWorld\n\n\n\nThis is\n a test\n\n\n\n\n",
            "\n\n\n",
            "Only remove this\n\n\nNotThis\nLines",
            "no change",
            "",
        ]
    elif processor_options == "triple":
        results = [
            "HelloWorld\n\n\n\nThis is\n a test\n\n\n\n\n",
            "",
            "Only remove thisNot\n\nThis\nLines",
            "no change",
            "",
        ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_process_text_method(setup_processor):
    pass


def test_rm_newlines_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_newlines_in_doc(input_documents, setup_processor, doc_results):
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
