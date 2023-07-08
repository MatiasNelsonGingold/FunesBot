
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.document_stores import InMemoryDocumentStore



def primer_input_func():

    document_store = InMemoryDocumentStore(use_bm25=True)

    #file path local
    file_path_local = r'c:\Users\Matías NG\Downloads\FunesBot-Ian(1)\FunesBot-Ian\model_1\WAR_and_PEACE_TEXT_FORMAT.txt'

    #Función primer input

    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run(file_path=file_path_local)

    return document_store
