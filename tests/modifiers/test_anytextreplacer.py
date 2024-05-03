from textprepper.modifiers import AnyTextReplacer
from textprepper.base import DocumentPreprocessorPipe
from ..utils import create_documents_with_simple_metadata

import pytest


@pytest.fixture
def input_strings():
    texts = [
        "Hello, the weather is nice today!",
        "What is the job of the scrum master? Nobody knows.",
        "This is a string",
        "no change",
        "",
    ]
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture(params=["option_1", "option_2"])
def processor_options(request):
    return request.param


@pytest.fixture
def setup_processor(processor_options):
    if processor_options == "option_1":
        processor = AnyTextReplacer(strings_to_replace=["is"], repl_with="are")
    elif processor_options == "option_2":
        processor = AnyTextReplacer(strings_to_replace=["is", "the"], repl_with="X")

    return processor


@pytest.fixture
def results(processor_options):
    if processor_options == "option_1":
        results = [
            "Hello, the weather are nice today!",
            "What are the job of the scrum master? Nobody knows.",
            "Thare are a string",
            "no change",
            "",
        ]
    elif processor_options == "option_2":
        results = [
            "Hello, X weaXr X nice today!",
            "What X X job of X scrum master? Nobody knows.",
            "ThX X a string",
            "no change",
            "",
        ]
    return results


@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_modify_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_modify_doc(input_documents, setup_processor, doc_results):
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
