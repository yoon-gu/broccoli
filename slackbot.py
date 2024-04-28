import re
from pathlib import Path
from typing import Dict, List, Optional
from fsspec import AbstractFileSystem

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document


class IPYNBReader(BaseReader):
    """Image parser."""

    def __init__(
        self,
        parser_config: Optional[Dict] = None,
        concatenate: bool = False,
    ):
        """Init params."""
        self._parser_config = parser_config
        self._concatenate = concatenate

    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
        """Parse file."""
        if file.name.endswith(".ipynb"):
            try:
                import nbconvert
            except ImportError:
                raise ImportError("Please install nbconvert 'pip install nbconvert' ")
        if fs:
            with fs.open(file, encoding="utf-8") as f:
                string = nbconvert.exporters.ScriptExporter().from_file(f)[0]
        else:
            string = nbconvert.exporters.ScriptExporter().from_file(file)[0]
        # split each In[] cell into a separate string
        splits = re.split(r"In\[\d+\]:", string)

        if self._concatenate:
            docs = [Document(text="\n\n".join(splits), metadata=extra_info or {})]
        else:
            docs = [Document(text=s, metadata=extra_info or {}) for s in splits]
        return docs


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llms import llms_dict
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
documents = SimpleDirectoryReader("docs", recursive=True,
                                file_extractor={".ipynb": IPYNBReader()}).load_data()

index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
qe = index.as_query_engine(llm=llms_dict["gemini-pro"])
response = qe.query("What kind agent is used in this document?")
print(response.response)
print(response.get_formatted_sources())

response = qe.query("What datasets are used in this documents?")
print(response.response)
print(response.get_formatted_sources())