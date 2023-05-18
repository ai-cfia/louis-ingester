# https://docs.pinecone.io/docs/semantic-text-search
import pinecone

from sentence_transformers import SentenceTransformer
import torch
import glob
import os
import re
import lxml.etree as ET

from tqdm.auto import tqdm

# load .env file
from dotenv import load_dotenv
load_dotenv()

# get api key from app.pinecone.io
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY'
# find your environment next to the api key in pinecone console
PINECONE_ENV = os.environ.get('PINECONE_ENVIRONMENT') or 'PINECONE_ENVIRONMENT'

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

def get_index(index_name):
    return pinecone.Index(index_name)

def load_chunks_text(chunks):
    chunks_text = []
    for chunk in chunks:
        with open(chunk) as fhand:
            text = fhand.read()
            chunks_text.append(text)
    return chunks_text

def to_act_name(fname):
    return fname.replace('data/sections/', '').replace('.txt', '').split('/')[0]


def to_section_name(fname):
    return fname.replace('data/sections/', '').replace('.txt', '').split('/')[1]

def create_index(model):
    if model.index_name() not in pinecone.list_indexes():
        pinecone.create_index(
            name=model.index_name(), 
            dimension=model.get_dimension())

class MiniLM:
    def __init__(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if device != 'cuda':
            print(f"You are using {device}. This is much slower than using "
                "a CUDA-enabled GPU. If on Colab you can change this by "
                "clicking Runtime > Change runtime type > GPU.")

        self.model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

    def encode_slice(self, slice):
        return self.model.encode(slice).tolist()
    
    def get_dimension(self):
        return self.model.get_sentence_embedding_dimension()
    
    def index_name(self):
        return 'semantic-search-fast'
    
    def batch_size(self):
        return 128

class CohereModel:
    def __init__(self):
        import cohere
        self.co = cohere.Client(api_key=os.environ.get('COHERE_API_KEY'))
        self.model_name = "embed-multilingual-v2.0"
    
    def encode_slice(self, slice):
        return self.co.embed(
            slice,
            model=self.model_name,
            truncate='END'
        ).embeddings
    
    def encode(self, query):
        return self.co.embed(
            [query],
            model=self.model_name,
            truncate='END'
        ).embeddings
    
    def get_dimension(self):
        # https://docs.cohere.com/reference/embed
        return 768
    
    def batch_size(self):
        return 96
    
    def index_name(self):
        return 'cohere-multingual'


def index_chunks(model):
    create_index(model)
    index = get_index(model.index_name())

    chunks = glob.glob('data/sections/*/*.txt')
    for i in tqdm(range(0, len(chunks), model.batch_size())):
        # find end of batch
        i_end = min(i+model.batch_size(), len(chunks))
        # create IDs batch
        ids = [str(x) for x in range(i, i_end)]
        # create metadata batch
        chunks_slice = load_chunks_text(chunks[i:i_end])
        metadatas = []
        # for loop with iterator index and value in chunks_slice
        for i, text in enumerate(chunks_slice):
            assert text is not None
            metadatas.append({
                'text': text, 
                'act': to_act_name(chunks[i]),
                'section': to_section_name(chunks[i])
            })
        # create embeddings
        xc = model.encode_slice(chunks_slice)
        # create records list for upsert
        records = zip(ids, xc, metadatas)
        # upsert to Pinecone
        index.upsert(vectors=records)

    # check number of records in the index
    index.describe_index_stats()


if __name__ == '__main__':
    # model = MiniLM()
    model = CohereModel()    
    index_chunks(model)