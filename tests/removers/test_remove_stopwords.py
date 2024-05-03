from textprepper.removers import NLTKRemoveStopwords
from textprepper.base import DocumentPreprocessorPipe

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pytest
from ..utils import create_documents_with_simple_metadata



@pytest.fixture(params=["english", "german"])
def processor_options(request):
    return request.param


@pytest.fixture
def input_strings(processor_options):
    if processor_options == "english":
        texts = [
            "This is an example of a sentence with stopwords.",
            "Can you remove the unnecessary words from this query?",
            "She looked around but did not find anything interesting.",
        ]
    elif processor_options == "german":
        texts = [
            "Dies ist ein Beispiel für einen Satz mit Stoppwörtern.",
            "Können Sie die unnötigen Wörter aus dieser Anfrage entfernen?",
            "Sie schaute sich um, fand aber nichts Interessantes.",
        ]
    return texts


@pytest.fixture
def input_documents(input_strings):
    return create_documents_with_simple_metadata(input_strings)


@pytest.fixture
def setup_processor(processor_options):
    if processor_options == "english":
        processor = NLTKRemoveStopwords()  # Default behavior
    elif processor_options == "german":
        processor = NLTKRemoveStopwords(language="german")  # Adjusted Example

    return processor

@pytest.fixture
def results(processor_options, input_strings):
    def _remove_stopwords(input_strings, lang):
        stop_words = set(stopwords.words(lang))
        words = word_tokenize(input_strings)
        filtered_sentence = [word for word in words if word.lower() not in stop_words]
        return " ".join(filtered_sentence)
    
    results = [_remove_stopwords(text, processor_options) for text in input_strings]
    return results

@pytest.fixture
def doc_results(results):
    return create_documents_with_simple_metadata(results)


def test_process_text_method(setup_processor):
    pass


def test_rm_stopwords_in_str(input_strings, setup_processor, results):
    transformed = [setup_processor(text) for text in input_strings]

    assert len(results) == len(transformed), "The Length are not equal"
    assert all(
        [result == transform for result, transform in zip(results, transformed)]
    ), "The strings of the processor aren't equal with the expected results"


def test_rm_stopwords_in_doc(input_documents, setup_processor, doc_results):
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
