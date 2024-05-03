from .base import Preprocessor
from .modifiers import AnyRegReplacer, AnyTextReplacer

import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List


class RemovePunctuation(Preprocessor):
    punctuations: str = string.punctuation

    def process_text(self, text: str, *args, **kwargs) -> str:
        return text.translate(str.maketrans("", "", self.punctuations))


class RemoveWhitespace(Preprocessor):
    remove_double_whitespaces: bool = False

    def process_text(self, text: str, *args, **kwargs) -> str:
        if self.remove_double_whitespaces:
            return " ".join(re.split(r"\s+", text.strip(), flags=re.UNICODE))
        return text.strip()


class NLTKRemoveStopwords(Preprocessor):
    language: str = "english"
    _stopwords: List[str] = list()

    def model_post_init(self, __context) -> None:
        try: 
            self._stopwords = set(stopwords.words(self.language))
        except LookupError as e:
            print(f"Failed to find: {e}")

    def process_text(self, text: str, *args, **kwargs) -> str:
        tokens = word_tokenize(text)
        words = [word for word in tokens if word.lower() not in self._stopwords]
        return " ".join(words)


class RemoveHeader(Preprocessor):
    """Simply removes the first line a string or document. E.g. if you want to
    remove the title of a page or the header line."""

    def process_text(self, text: str, *args, **kwargs) -> str:
        if "\n" in text:
            return text.split("\n", 1)[1]
        else:
            return text


class RemoveNewLines(AnyRegReplacer):
    count: int = 1
    repl_with: str = ""
    regex_pattern: str = ""

    def model_post_init(self, __context) -> None:
        self.regex_pattern: str = r"(?<!\n)\n{" + str(self.count) + r"}(?!\n)"


class RemoveEmojis(Preprocessor):
    regex_compiler: re.Pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoji
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )

    def process_text(self, text: str, *args, **kwargs) -> str:
        # Reference : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
        return self.regex_compiler.sub(r"", text)


class RemoveHyphens(AnyTextReplacer):
    strings_to_replace: List[str] = ["\xc2\xad", "\xad", "\u00ad", "-\n"]
    repl_with: str = ""


class RemoveURL(AnyRegReplacer):
    regex_pattern: str = r"(www|http)\S+"
    repl_with: str = ""


class RemoveEmails(AnyRegReplacer):
    regex_pattern: str = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}\b"
    repl_with: str = ""


class RemoveHTMLTags(AnyRegReplacer):
    regex_pattern: str = r"<.*?>"
    repl_with: str = ""
