#Lane Chainを使ったPAGElyzabを用いて試してみた
#https://note.com/alexweberk/n/n3cffc010e9e9
#https://nynupe! readthedocs, 10/ja/latest/rag himi
#https://unstructuree-ie github.io/unstructured/bricks himitoartition potx
#https://github.com/langchain-ai/langchain/discussions/18559
from trafilatura import fetch_url, extract
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain.chains import LLMChain, RetrievalQA, SimpleSequentialChain
from langchain.retrievers import ParentDocumentRetriever, MultiVectorRetriever
from langchain.schema import Document
from langchain.schema.embeddings import Embeddings
from langchain.storage import InMemoryStore
from langchain.chains.summarize import load_summarize_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader, PyPDFLoader, JSONLoader, Docx2txtLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import TokenTextSplitter, CharacterTextSplitter, RecursiveCharacterTextSplitter

import os
from typing import Any
import uuid

class JapaneseCharacterTextSplitter(RecursiveCharacterTextSplitter):
    def __init__(self, **kwargs: Any):
        separators = ["\n\n", "\n", "。", "、", " ", ""]
        super().__init__(separators=separators, **kwargs)

#ローダー
#https://www.ai-shift.co.jp/techblog/4037
#https://github.com/langchain-ai/langchain/discussions/16573

loaders = {
    '.txt' : UnstructuredFileLoader,
    '.pdf' : PyPDFLoader, #PyMuPDFLoader, FUnstructured PDFLoader,
    '.pptx' : UnstructuredPowerPointLoader,
    '.xlsm' : UnstructuredExcelLoader,
    '.xlsx' : UnstructuredExcelLoader,
    '.html' : UnstructuredHTMLLoader,
    '.xml' : UnstructuredXMLLoader,
    '.md' : UnstructuredMarkdownLoader,
    '.json' : JSONLoader,
    '.docs' : Docx2txtLoader,
    '.csv' : CSVLoader,
}

#https://www.sato-susumu.com/entry/2023/04/30/131338

#Define a function to create a DirectoryLoader for a specific file type
def create_directory_loader(file_type, directory_path):
    return DirectoryLoader (
        path = directory_path,
        glob = f'**/*{file_type}',
        loader_cls = loaders[file_type],
    )

def append_loaders_list(loaders_list, dir):
    loaders_list.append (create_directory_loader('.txt', dir))
    loaders_list.append (create_directory_loader('.json', dir))
    loaders_list.append (create_directory_loader('.pdf', dir))
    loaders_list.append (create_directory_loader('.docs', dir))
    loaders_list.append (create_directory_loader('.csv', dir))
    loaders_list.append (create_directory_loader('.pptx', dir))
    loaders_list.append (create_directory_loader('.xlsm', dir))
    loaders_list.append (create_directory_loader('.xlsx', dir))
    loaders_list.append (create_directory_loader('.html', dir))
    loaders_list.append (create_directory_loader('.xml', dir))
    loaders_list.append (create_directory_loader('.md', dir))

def initialize(dbpath, commondir, privatedir):
    embeddings = HuggingFaceEmbeddings(model_name = 'intfloat/multilingual-e5-large')
    # #do有無の確認
    # if os.path.exists (dbpath) == True:
    #     #db読み込み
    #     db = FAISS.load_local (dbpath, embeddings, allow_dangerous_deserialization=True) 
    # else:
    #Create DirectoryLoader instances for each file type
    loaders_list = []
    append_loaders_list(loaders_list, commondir)
    append_loaders_list(loaders_list, privatedir) 

    #フォルダからファイルをロードする
    documents = []
    for loader in loaders_list:
        # Use UnstructuredFileLoader to load each file
        # pip uninstall python-magic
        # pip install python-magic-bin==0.4.14
        # pip install python-pptx
        docs = loader.load()
        documents.extend(docs)

    # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    #     separator = '\n',
    #     chunk_size = 300,
    #     chunk_overlap = 20
    # )

    text_splitter = RecursiveCharacterTextSplitter(
        separators = ['\n', '。'],
        chunk_size = 300,
        chunk_overlap = 20,
    )

    texts = text_splitter.split_documents(documents)
    #print(len(texts))

    db = FAISS.from_documents(texts, embeddings)
    #距離尺度をコサイン類似度にする
    #db = FAISS.from_documents(texts, embeddings, distance_strategy = DistanceStrategy.MAX_INNER_PRODUCT, normalize_L2 = True)

    #dbの保存
    db.save_local(dbpath)

    #一番類似するチャンクをいくつロードするかを変数kに設定できる
    #retriever = db.as_retriever (search_kwargs={'K': 5})
    #類似度のスコアと値を設定して、閾値以上の類似度を持つDocumentsオブジェクトを返します。
    retriever = db.as_retriever(search_type = 'similarity_score_threshold', search_kwargs = {'score_threshold' : 0.8})

    return retriever

#https://giita.com/shinaj iroxyz/items/facf409b81f59bb68775
def get_empty_faiss_vectorstore(embedding:Embeddings, dim =None, **kwargs):
    dummy_text, dummy_id = '1', 1
    if not dim: #次元数が未知の場合
        dummy_emb = embedding.query(dummy_text)
    else: #次元数が既知の場合
        dummy_emb = [0]*dim
    vectorstore = FAISS.from_embeddings([(dummy_text, dummy_emb)], embedding, ids = [dummy_id], **kwargs)
    vectorstore.delete ([dummy_id])
    return vectorstore

def initialize_ParentDocumentRetriever(dbpath, commondir, privatedir):
    #https://giita.com/shimajiroxyz/items/facf409b81f59tt68775
    #https://giita.com/mashmoeiar11/items/d7ba174c770a0f05356c
    embeddings = HuggingFaceEmbeddings(model_name = 'intfloat/multilingual-e5-large')
    loaders_list = []
    append_loaders_list(loaders_list, commondir)
    append_loaders_list(loaders_list, privatedir)

    #フォルダからファイルをロードする
    documents = []
    for loader in loaders_list:
        # Use UnstructuredFileLoader to load each file
        # pip uninstall python-magic
        # pip install python-magic-bin=0.4.14
        # pip install python-pptx
        docs = loader.load()
        documents.extend(docs)

    #文書を細切れにするためのsplitter
    # parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
    # child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    parent_splitter = JapaneseCharacterTextSplitter(chunk_size=2000)
    child_splitter = JapaneseCharacterTextSplitter(chunk_size=400)

    id_key = 'doc_id'
    #The vectorstore to use to index the child chunks
    #vectorstore = get_empty_faiss_vectorstore (embeddings, 1536)
    vectorstore = Chroma(collection_name="full_documents", embedding_function = embeddings)
    docstore = InMemoryStore()

    #Retrieverを作成
    retriever = ParentDocumentRetriever(vectorstore = vectorstore, docstore = docstore, child_splitter = child_splitter, parent_splitter=parent_splitter, id_key = id_key)

    #Add texts
    retriever.add_documents(documents, ids=None)

    return retriever, vectorstore
 
def create_context(retriever, text):
    #一致度
    found_docs = retriever.invoke(text)
    print(len(found_docs))
    context = '\n'.join([document.page_content for document in found_docs])
    print (context)
    return context

def create_context_sub(vectorstore, text):
    #一致度
    found_docs = vectorstore.similarity_search(text)
    print(len(found_docs))
    context = '\n'.join([document.page_content for document in found_docs])
    print (context)
    return context

def summary (model, tokenizer, document):
    #https://book.st-hakky.com/data-science/langchain-long-document/
    template = '''
    ユーザー: 以下のテキストを参照して、それに続く質問に答えてください。

    [context]

    [question]

    システム: '''

    prompt = PromptTemplate(
        template = template,
        input_variable = ['context', 'qcuestion'],
        template_format = 'f-string'
    )

    pipe = pipeline (
        'text-generation',
        mode = model, 
        tokenizer = tokenizer,
        max_new_tokens = 128,
        do_sample = True,
        temperature = 0.01,
        repetition_penalty = 2.0,
    )

    llm = HuggingFacePipeline(pipeline = pipe)

    max_tokens:int = 60
    text_splitter = TokenTextSplitter(chunk_size = max_tokens, chunk_overlap = 20)

    summary_chain = load_summarize_chain(llm, chain_type = 'map_reduce')

    promptSubject = PromptTemplate(input_variables=['text'], template='''\'\'\'{text}\'\'\'\
    上記のテーマは以下の通り：\n\n* ''')
    chainSubject = LLMChain(llm = llm, prompt=promptSubject)

    overall_Chain_map_reduce = SimpleSequentialChain(chains = [summary_chain, chainSubject])
    subject = overall_Chain_map_reduce.run(text_splitter.create_documents ([document]))
    print (subject)

    return subject

def response (retriever, model, tokenizer, text):
    #呼び出し例
    #outputids = rag.response(db, model, tokenizer, text)['result']
    #outout = outputids [outputids.find('システム：'+ len ('システム：'):]

    template = '''
    ユーザー：以下のテキストを参照して、それに続く質問に答えてください。

    [context]

    [question]

    システム：'''

    prompt = PromptTemplate(
        template = template,
        input_variable = ['context', 'question'],
        template_format = 'f-string'
    )

    pipe = pipeline(
        'text-generation',
        model = model,
        tokenizer = tokenizer,
        nax_new_takens = 128,
        do_sample = True,
        temperature = 0.01,
        repetition_penalty = 2.0,
    )

    llm = HuggingFaceEmbeddings(pipeline=pipe)

    qa = RetrievalQA.from_chain_type(
        llm = llm,
        retriever = retriever,
        chain_type = 'stuff',
        return_source_documents = True,
        chain_Type_kwargs = {'prompt':prompt},
        verbose=True,
    )

    output = qa.invoke (text)

    return output 

if __name__ == '__main__':
    # retriever = initialize('./data/ppe.db', './data', './mem')
    retriever, vectorstore = initialize_ParentDocumentRetriever('./data/ppe.db', './data', './mem')

    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break

        context = create_context(retriever, text)