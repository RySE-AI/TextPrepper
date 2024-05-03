from textprepper.removers import RemoveEmails
from textprepper.base import DocumentPreprocessorPipe, Preprocessor
from ..utils import create_documents_with_simple_metadata

import pytest

@pytest.fixture
def input_strings():
    texts = [
        "FirstName.LastName@mail-domain.de",
        "This is my mail: Name@test.com",
        "This is the mail: your-name@ABC.com but better use this Another.Name@test-domain.de",
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
        processor = RemoveEmails()  # Default behavior
    elif processor_options == "adapted":
        processor = RemoveEmails(repl_with="blank")  # Adapted behavior

    return processor


@pytest.fixture
def results(processor_options):
    if processor_options == "default":
        results = [
            "",
            "This is my mail: ",
            "This is the mail:  but better use this ",
            "no change",
            "",
        ]
    elif processor_options == "adapted":
        results = [
            "blank",
            "This is my mail: blank",
            "This is the mail: blank but better use this blank",
            "no change",
            "",
        ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_processor(setup_processor, processor_options):
    setup_processor = setup_processor
    assert isinstance(setup_processor, Preprocessor)

    assert (
        setup_processor.regex_pattern
        == r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}\b"
    )
    if processor_options == "default":
        assert setup_processor.repl_with == ""
    elif processor_options == "adapted":
        assert setup_processor.repl_with == "blank"


def test_rm_email_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_email_in_doc(input_documents, setup_processor, doc_results):
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
