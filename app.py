import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Mentor de Backend - Clean Code", page_icon="🤖")
st.title("Mentor de Backend & Code Reviewer")
st.write("Faça perguntas sobre boas práticas, arquitetura e Clean Code baseadas no manual oficial.")

@st.cache_resource
def carregar_agente():
    caminho_pdf = "Boas_Praticas_de_Codigo_e_Clean_Code.pdf"
    if not os.path.exists(caminho_pdf):
        return None, "pdf_ausente"

    if not os.environ.get("GOOGLE_API_KEY"):
        return None, "chave_ausente"

    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pedacos_texto = text_splitter.split_documents(documentos)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    banco_vetorial = Chroma.from_documents(pedacos_texto, embeddings)
    retriever = banco_vetorial.as_retriever()

    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.3)

    system_prompt = (
        "Você é um Engenheiro de Software Sênior e Mentor de Backend. "
        "Use os trechos de contexto a seguir extraídos do nosso manual de boas práticas "
        "para responder à pergunta do desenvolvedor júnior. "
        "Seja didático, encorajador e dê exemplos de código se possível. "
        "Se a resposta não estiver no contexto, diga educadamente que o manual não cobre esse tópico.\n\n"
        "Contexto:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    agente = create_retrieval_chain(retriever, question_answer_chain)
    return agente, None

agente, erro = carregar_agente()

if erro == "pdf_ausente":
    st.error("Documento 'Boas_Praticas_de_Codigo_e_Clean_Code.pdf' não encontrado na pasta raiz.")
elif erro == "chave_ausente":
    st.error("Variável de ambiente GOOGLE_API_KEY não configurada no servidor.")
else:
    pergunta_usuario = st.text_input("Qual a sua dúvida de código hoje, Dev?")

    if st.button("Consultar Mentor"):
        if pergunta_usuario:
            with st.spinner("Analisando a base de arquitetura..."):
                try:
                    resposta = agente.invoke({"input": pergunta_usuario})
                    st.success("Resposta do Mentor:")
                    st.markdown(resposta["answer"])
                except Exception as e:
                    st.error(f"Ocorreu um erro ao consultar o Mentor: {e}")
        else:
            st.warning("Por favor, digite uma pergunta antes de consultar.")