#Initializing the PineconeDocumentStore --de esta manera llamo a la base de datos (la cual puede estar vacia inicialmente)
from haystack.document_stores import PineconeDocumentStore
from params import *
import pinecone
from haystack.nodes.retriever.dense import EmbeddingRetriever

document_store = PineconeDocumentStore(
    api_key="ead8051e-8608-497a-beb2-a8d7d9092bd4",
    environment='asia-southeast1-gcp-free',
    index = 'haystack-extractive-qa',
    similarity="cosine",
    embedding_dim=384
)

# convertir libro en formato de texto en formato que pueda leer haystack
from haystack.nodes import TextConverter, PreProcessor

converter = TextConverter(remove_numeric_tables=True, valid_languages=["en"])
doc_txt = converter.convert(file_path="WAR_and_PEACE_TEXT_FORMAT.txt", meta=None)[0]

#preprocesar el libro --> realizar el split
from haystack.nodes import PreProcessor

# This is a default usage of the PreProcessor.
# Here, it performs cleaning of consecutive whitespaces
# and splits a single large document into smaller documents.
# Each document is up to 1000 words long and document breaks cannot fall in the middle of sentences
# Note how the single document passed into the document gets split into 5 smaller documents

preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=100,
    split_respect_sentence_boundary=True,
)
docs_default = preprocessor.process([doc_txt])
print(f"n_docs_input: 1\nn_docs_output: {len(docs_default)}")


#con lo que sigue se sube a la base de datos en pinecone (se actualiza la abse de datos)
from haystack import Document
document_store.write_documents(docs_default)

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="multi-qa-MiniLM-L6-cos-v1",
    model_format="sentence_transformers"
)

document_store.update_embeddings(
    retriever,
    batch_size=16
)
