
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.document_stores import InMemoryDocumentStore



def primer_input_func():

    document_store = InMemoryDocumentStore(use_bm25=True)

    #file path local
    file_path_local = 'WAR_and_PEACE_TEXT_FORMAT.txt'

    #Función primer input

    indexing_pipeline = TextIndexingPipeline(document_store)
    document_store_f=indexing_pipeline.run(file_path=file_path_local)

    return document_store_f
