from textprepper.removers import RemoveURL
from textprepper.base import DocumentPreprocessorPipe

import pytest
from langchain_core.documents import Document

from ..utils import create_documents_with_simple_metadata


@pytest.fixture
def input_strings():
    texts = [
        "https://www.test-domain.de/",
        "This is my profile: http://www.test123domain.com/profile/123",
        """This is the mail: https://www.test-domain.de/ but better use
        this www.I-like-doplhins.de/ Crazy website""",
        "no change",
        "",
    ]
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture(params=["default", "adapted"])
def processor_options(request):
    return request.param


@pytest.fixture
def setup_processor(processor_options):
    if processor_options == "default":
        processor = RemoveURL()  # Default behavior
    elif processor_options == "adapted":
        processor = RemoveURL(repl_with="blank")  # Adapted behavior

    return processor


@pytest.fixture
def results(processor_options):
    if processor_options == "default":
        results = [
            "",
            "This is my profile: ",
            """This is the mail:  but better use
        this  Crazy website""",
            "no change",
            "",
        ]
    elif processor_options == "adapted":
        results = [
            "blank",
            "This is my profile: blank",
            """This is the mail: blank but better use
        this blank Crazy website""",
            "no change",
            "",
        ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_process_text_method(setup_processor):
    pass


def test_rm_urls_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_urls_in_doc(input_documents, setup_processor, doc_results):
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
