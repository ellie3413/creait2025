import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from langchain_community.document_loaders import TextLoader
from pathlib import Path

dotenv_path = '.env'

load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

response = requests.get(
    "https://en.wikipedia.org/w/api.php",
    params={
        "action": "query",
        "format": "json",
        "titles": "OpenAI",
        "prop": "extracts",
        "explaintext": True,
    },
).json()

from langchain_community.document_loaders import TextLoader
from pathlib import Path

path = Path('openai.txt').expanduser()
loader = TextLoader(path, encoding='utf-8')


#from langchain_community.document_loaders import PyPDFLoader

#loader = PyPDFLoader("./Mistral_AI.pdf")
docs = loader.load()
#print(docs)

from langchain_text_splitters import CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.split_documents(docs)

print(documents)
