# TextPrepper

TextPrepper is a simple text preprocessing tool designed to modify queries and
documents for Langchain applications. It offers a collection of common NLP 
preprocessing/cleaning techniques from removing newlines to more advanced regex-based removals.
This module should help you from simple text/document transformations to seamless integration with Langchain's LCEL workflows.

## Installation

> [!WARNING]
> This is my first published pypi package, so there might be some issues. And some preprocessors are not tested yet!

```bash
pip install textprepper
```

## Introduction

TextPrepper helps you with the preprocessing steps essential for natural language processing tasks. Data understanding and cleaning are important steps in building effective ML applications, but let's be honest, not everyone has the time to analyze every PDF, text file, or other documents in their company and maybe you can't/are not allowed use tools like unstructured. Additionally I struggled to find an effective tool for creating a preprocessing pipeline that could be easily integrated into my LCEL Chains, e.g. to manipulating the query in the same way I manipulated my documents.

That’s why I began building my own collection of text preprocessors, which I can not only reuse across various projects but also adapt seamlessly into LCEL chains. I primarily adapted the content from berknolgoy's package [text-preprocessing](https://github.com/berknology/text-preprocessing) and some kaggle examples in object-oriented fashion. My approach was inspired by the torchvision's [compose/transform](https://pytorch.org/vision/main/generated/torchvision.transforms.Compose.html) behavior.

## Quickstart

> [!IMPORTANT]
> If you're using a preprocessor, it will overwrite the document's page_content **inplace**!

### Example 1: Document Preprocessing / Cleaning

```python
from textprepper.modifiers import LowerText
from textprepper.removers import RemoveNewLines
from textprepper import DocumentPreprocessorPipe
from langchain_core.documents import Document

doc_pipe = DocumentPreprocessorPipe([LowerText(), RemoveNewLines(count=2)])

dummy_doc = Document(page_content="I AM\n\nMr.\nCAPSLOCK")

print(doc_pipe(dummy_doc))

# Output
# page_content='i ammr.\ncapslock'

## Or if you have mutiple documents, use the .from_document() method
dummy_docs = [dummy_doc.copy() for i in range(5)]
results = doc_pipe.from_documents(dummy_docs)
```

A more detailed guide on basic usages is available [here](./examples/00_Basic_usage_of_preprocessors.ipynb).

### Example 2: Query Manipulation

```python
from textprepper.modifiers import GoogleTrans
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

# Setup an instance to translate the input text to german
translator = GoogleTrans(source_lng="auto",
                         target_lng="german")

# Define a simple LCEL Chain
prompt = ChatPromptTemplate.from_template("""Question: {question}""")
simple_chain = RunnablePassthrough() | translator | prompt
print(simple_chain.invoke("This is a test."))

# Output:
# messages=[HumanMessage(content='Question: Das ist ein Test.')]
```

Explore a more detailed LCEL integration example in this [notebook](./examples/01_How-to_use_processor_in_LCEL.ipynb). 
You find an example with a retriever [here](./examples/02_Translate_Query_to_another_language.ipynb).


## Create your custom Preprocessor

To extend TextPrepper with your custom functionality, you can create a new
preprocessor by inheriting from the base class, which utilizes Pydantic's
BaseModel under the hood.

- The preprocessor class has one abstract method whichyou need to define `process_text()`
  - this will get the string of the document, performs the string manipulation and needs to return a string back
- Optional: You can define the `add_metadata()` if you want to edit the metadata of the document too. The add_metadata will be called before the process_text method

```python
from textprepper import Preprocessor

class RemoveAllNumbers(Preprocessor):
    # Abstractmethod which you need to define
    def process_text(self, text: str, *args, **kwargs) -> str:
        return ''.join([char for char in text if not char.isdigit()])
    
    # Optional
    def add_metadata(self, doc, **kwargs) -> Dict:
        return {"removed_all_numbers": True}
```

# Note

My primary motivation is to learn and gain practical experience in developing my own PyPI package, which I plan to release soon. This project is an opportunity for me to get practical experience with testing frameworks like pytest, as well as familiarize myself with GitHub actions. This is my first attempt at creating my own module.

I welcome any suggestions for improvements or corrections, so please feel free to share your feedback. I'm eager to learn from your insights.