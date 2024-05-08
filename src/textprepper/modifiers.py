from .base import Preprocessor

import re
from typing import Optional, Dict, List

from spellchecker import SpellChecker
from deep_translator import GoogleTranslator
from deep_translator.base import BaseTranslator
from langchain_core.documents import Document


class LowerText(Preprocessor):
    """A preprocessor class for converting all text to lowercase."""

    def process_text(self, text: str, *args, **kwargs) -> str:
        return text.lower()


class UpperText(Preprocessor):
    """A preprocessor class for converting all text to uppercase."""

    def process_text(self, text: str, *args, **kwargs) -> str:
        return text.upper()


# TODO: Write Tests
# TODO: handle punctuations and none types
class SpellChecking(Preprocessor):
    """A preprocessor class to correct spelling in the text.This spellchecker
    uses pyspellchecker.
    """

    language: str = "en"
    distance: int = 2
    case_sensitive: bool = False
    known_words: Optional[List[str]] = None
    known_words_from_file: Optional[str] = None
    _spell_checker: SpellChecker = None

    def model_post_init(self, __context) -> None:
        if not self._spell_checker:
            self._spell_checker = SpellChecker(
                language=self.language,
                distance=self.distance,
                case_sensitive=self.case_sensitive,
            )
        if self.known_words:
            self._spell_checker.word_frequency.load_words(self.known_words)

        if self.known_words_from_file:
            self._spell_checker.word_frequency.load_text_file(
                self.known_words_from_file
            )

    def process_text(self, text: str, *args, **kwargs) -> str:
        corrected_text = []
        misspelled_words = self._spell_checker.unknown(text.split())
        for word in text.split():
            if word in misspelled_words:
                corrected_text.append(self._spell_checker.correction(word))
            else:
                corrected_text.append(word)

        return " ".join(corrected_text)


class MultipleRegexStringReplacer(Preprocessor):
    """A preprocessor class to replace strings based on multiple regex rules."""

    rules: Dict
    _rep: Dict = dict()
    _pattern: re.Pattern = None

    def model_post_init(self, __context) -> None:
        self._rep = dict((re.escape(k), v) for k, v in self.rules.items())
        self._pattern = re.compile("|".join(self.rules.keys()))

    def process_text(self, text: str, *args, **kwargs) -> str:
        text = self._pattern.sub(lambda m: self._rep[re.escape(m.group(0))], text)
        return text


class AnyTextReplacer(Preprocessor):
    """A preprocessor class to replace specified substrings with another substring."""

    strings_to_replace: List[str]
    repl_with: str
    count: int = -1

    def process_text(self, text: str, *args, **kwargs) -> str:
        for word in self.strings_to_replace:
            text = text.replace(word, self.repl_with, self.count)
        return text


class AnyRegReplacer(Preprocessor):
    """A preprocessor class to replace text based on a regex pattern. The
    processor uses re.sub(...).
    """

    regex_pattern: str
    repl_with: str

    def process_text(self, text: str, *args, **kwargs) -> str:
        return re.sub(self.regex_pattern, self.repl_with, text)


class AddAnyMetadata(Preprocessor):
    """A preprocessor class to add arbitrary metadata to a document."""

    metadata: dict

    def process_text(self, text: str, *args, **kwargs) -> str:
        return text

    def add_metadata(self, doc: Document, **kwargs) -> dict:
        return self.metadata


class LanguageTranslator(Preprocessor):
    """Base abstract class for language translators"""

    source_lng: str
    target_lng: str


class GoogleTrans(LanguageTranslator):
    """A preprocessor class for translating text using Google's translation
    services. The class uses deep-translators implementation.
    """

    source_lng: str = "auto"
    _translator: BaseTranslator = None

    def model_post_init(self, __context) -> None:
        self._translator = GoogleTranslator(
            source=self.source_lng, target=self.target_lng
        )

    def process_text(self, text: str, *args, **kwargs) -> str:
        return self._translator.translate(text)
