import os
from dotenv import load_dotenv
import anthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

CHROMA_DIR = "vectorstore/chroma_db"

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_answer(question, selected_class=None):
    
    if selected_class:
        filter_dict = {"class": selected_class}
        docs = vectorstore.similarity_search(question, k=4, filter=filter_dict)
    else:
        docs = vectorstore.similarity_search(question, k=4)

    if not docs:
        return "Sorry, I could not find relevant information in the study material.", []

    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([doc.metadata.get("source", "") for doc in docs]))

    prompt = f"""You are a helpful CBSE AI subject tutor for students of Class 9 to 12.
Answer the student's question using ONLY the study material provided below.
If the answer is not in the material, say "This topic is not covered in the available study material."
Always be clear, simple and student-friendly in your explanation.

Study Material:
{context}

Student Question: {question}

Answer:"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.content[0].text
    return answer, sources