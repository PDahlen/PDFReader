import streamlit as st
import chromadb
from pypdf import PdfReader

# streamlit run app.py

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="researchpapers")

file_name = "2307.07487.pdf"

reader = PdfReader(file_name)
number_of_pages = len(reader.pages)
text = ''
for i in range(number_of_pages):
    page = reader.pages[0]
    text += page.extract_text()

n = 1000
docs = [text[i:i+n] for i in range(0, len(text), n)]

ids = []
i = 0
for doc in docs:
    i = i + 1
    ids.append(str(i))

collection.add(
    documents=docs,
    ids=ids
)

st.title('🦜🔗 Scientist')
prompt = st.text_input('Input your prompt here')

if prompt:
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )

    st.write(results)
