# TextPrepper

A text preprocessing tool to modify queries and Langchain Documents.

## Installation

I'll create a pypi package soon.

## Introduction
Work in Progress

## Quickstart

#### Example: Query Manipulation

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

You can find a more detailed example how to integrate a preprocessor in this
[notebook](./examples/01_How-to_use_processor_in_LCEL.ipynb). 

#### Example: Document Preprocessing / Cleaning

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

You can find a more detailed example about the basic usages [here](./examples/00_Basic_usage_of_preprocessors.ipynb).
There is an example to create your custom preprocessor too.