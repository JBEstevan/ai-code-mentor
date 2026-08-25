import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

# Tratamento de compatibilidade do LangChain
try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ModuleNotFoundError:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Mentor de Backend - Clean Code", page_icon="🤖", layout="centered")
st.title("Mentor de Backend & Code Reviewer 🤖")
st.write("Faça perguntas sobre boas práticas, arquitetura e Clean Code baseadas no manual oficial.")


# Função em Cache para carregar o RAG via API
@st.cache_resource(show_spinner=False)
def carregar_agente(api_key: str):
    os.environ["GOOGLE_API_KEY"] = api_key
    caminho_pdf = "Boas_Praticas_de_Codigo_e_Clean_Code.pdf"
    caminho_chroma = "./chroma_db"

    if not os.path.exists(caminho_pdf):
        return None, "pdf_ausente"

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    if os.path.exists(caminho_chroma) and os.listdir(caminho_chroma):
        banco_vetorial = Chroma(
            persist_directory=caminho_chroma,
            embedding_function=embeddings
        )
    else:
        loader = PyPDFLoader(caminho_pdf)
        documentos = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        pedacos_texto = text_splitter.split_documents(documentos)
        banco_vetorial = Chroma.from_documents(
            pedacos_texto,
            embeddings,
            persist_directory=caminho_chroma
        )

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

env_key = os.environ.get("GOOGLE_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Opções")

    if env_key:
        api_key_input = env_key
        st.success("Chave de API configurada pelo servidor.")
    else:
        api_key_input = st.text_input(
            "Chave API Google Gemini",
            value="",
            type="password",
            help="O servidor não tem uma chave configurada. Insira a sua própria chave do Google Gemini."
    )

    if st.button("🗑️ Limpar Histórico de Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Projeto:** Oracle Tech AI Builder\n**Stack:** LangChain, ChromaDB, Gemini 3.6 Flash.")

if not api_key_input:
    st.error("🔑 Variável de ambiente GOOGLE_API_KEY não configurada. Por favor, insira sua chave na barra lateral (Sidebar) ao lado.")
else:
    agente, erro = carregar_agente(api_key_input)

    if erro == "pdf_ausente":
        st.error("⚠️ Documento 'Boas_Praticas_de_Codigo_e_Clean_Code.pdf' não encontrado na pasta raiz.")
    elif agente is not None:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        if pergunta_usuario := st.chat_input("Qual a sua dúvida de código hoje, Dev?"):
            st.session_state.messages.append({"role": "user", "content": pergunta_usuario})
            with st.chat_message("user"):
                st.markdown(pergunta_usuario)

            with st.chat_message("assistant"):
                with st.spinner("Analisando o manual e consultando o Mentor..."):
                    try:
                        resposta = agente.invoke({"input": pergunta_usuario})
                        conteudo = resposta["answer"]
                        st.markdown(conteudo)
                        st.session_state.messages.append({"role": "assistant", "content": conteudo})
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao consultar o Mentor: {e}")