
from haystack.document_stores import PineconeDocumentStore

from params import *


def primer_input_func():

    #Initializing the PineconeDocumentStore
    document_store = PineconeDocumentStore(
        api_key="ead8051e-8608-497a-beb2-a8d7d9092bd4",
        environment='asia-southeast1-gcp-free',
        index='haystack-extractive-qa',
        similarity="cosine",
        embedding_dim=384
    )

    return document_store
