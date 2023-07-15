
from haystack.document_stores import PineconeDocumentStore

from params import *


def primer_input_func():

    #Initializing the PineconeDocumentStore
    document_store = PineconeDocumentStore(
        api_key=ian_pinecone_api,
        environment='us-west4-gcp-free',
        index='haystack-extractive-qa',
        similarity="cosine",
        embedding_dim=384
    )

    return document_store
