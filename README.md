# Mentor de Backend & Code Reviewer 🤖

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Render-blue?style=for-the-badge&logo=render)](https://ai-code-mentor-4uai.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.62-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3.6_Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)

> **Mentor Virtual Inteligente de Engenharia de Software Backend.**  
> Projeto desenvolvido como desafio final para o programa **Oracle Tech AI Builder**. É uma aplicação interativa baseada em **RAG (Retrieval-Augmented Generation)** que atua como mentor sênior e leitor de código, tirando dúvidas sobre boas práticas, arquitetura e **Clean Code** fundamentadas no manual oficial.

---

## 📸 Casos de Uso & Exemplos Reais

### 1. Orientação de Clean Code & Refatoração (Ruim vs. Bom)
> **Pergunta:** *"Como nomear variáveis em Java corretamente?"*  
> O mentor consulta o manual oficial, extrai os princípios de **revelação de intenção** e **clareza**, e fornece sugestões práticas comparando trechos de código **Ruim vs. Bom**.

| Pergunta & Início da Resposta | Detalhamento com Princípios Clean Code |
| :---: | :---: |
| ![Chat Flow](docs/images/print1.png) | ![Exemplo Ruim vs Bom](docs/images/print2.png) |

---

### 2. Convenções da Linguagem & Dicas do Mentor
> Aplicação automática das convenções padrões (`lowerCamelCase` em Java) acompanhada por dicas motivacionais de engenharia de software para o desenvolvedor júnior.

![Convenções e Dica do Mentor](docs/images/print3.png)

---

### 3. Controle de Escopo Semântico (RAG Sem Alucinações)
> **Pergunta fora do escopo:** *"Quem é Juan Estevan?"*  
> O sistema analisa a base de dados vetorial e identifica que o tópico não consta no manual. O mentor responde educadamente sem inventar informações, reforçando o escopo coberto (Clean Code, SOLID, DRY, KISS, YAGNI, Uncle Bob).

![Controle de Escopo RAG](docs/images/print4.png)

---

## 🔗 Acesse a Aplicação ao Vivo

🚀 **Link do Deploy no Render:** [https://ai-code-mentor-4uai.onrender.com](https://ai-code-mentor-4uai.onrender.com)

---

## 🎯 Sobre o Projeto

O **Mentor de Backend & Code Reviewer** foi desenvolvido para apoiar desenvolvedores na escrita de código limpo, sustentável e bem estruturado. Utilizando uma arquitetura de **RAG (Geração Aumentada por Recuperação)**, o mentor consulta o manual oficial de boas práticas em PDF para fornecer respostas precisas, didáticas e acompanhadas de exemplos de código práticos.

### ✨ Principais Funcionalidades
- **🤖 Mentor Didático & Encorajador:** Respostas formatadas em Markdown com explicações conceituais e exemplos de refatoração de código.
- **📚 Consulta Fundamentada (RAG):** Todas as orientações são extraídas do manual `Boas_Praticas_de_Codigo_e_Clean_Code.pdf`.
- **💬 Interface de Chat Interativa:** Histórico de conversa fluido integrado com `st.session_state` e opção de limpar mensagens.
- **🔑 Configuração Dinâmica da API Key:** Suporte para inserção de chave `GOOGLE_API_KEY` diretamente pela barra lateral (Sidebar) ou via variáveis de ambiente.
- **🧠 Persistência Vetorial Inteligente:** Indexação rápida de documentos utilizando **ChromaDB** e embeddings do **Google Gemini**.

---

## 🛠️ Arquitetura e Fluxo de Dados (RAG)

```mermaid
graph TD
    A[Boas_Praticas_de_Codigo_e_Clean_Code.pdf] -->|PyPDFLoader| B[Documentos Extraídos]
    B -->|RecursiveCharacterTextSplitter| C[Text Chunks]
    C -->|GoogleGenerativeAIEmbeddings gemini-embedding-001| D[(ChromaDB VectorStore)]
    E[Pergunta do Desenvolvedor] -->|Streamlit UI| F[Retriever]
    D <-->|Busca por Similaridade Semântica| F
    F -->|Contexto Relevante + Prompt| G[Google Gemini 3.6 Flash]
    G -->|Resposta Didática + Clean Code| H[Interface de Chat Streamlit]
```

---

## 🧰 Stack Tecnológica

| Componente | Tecnologia / Modelo |
| :--- | :--- |
| **Linguagem Principal** | Python 3.11+ |
| **Framework Web / UI** | Streamlit |
| **Orquestração de IA** | LangChain / LangChain Classic |
| **LLM (Modelo de Linguagem)** | Google Gemini 3.6 Flash (`gemini-3.6-flash`) |
| **Modelo de Embeddings** | Google Generative AI Embeddings (`gemini-embedding-001`) |
| **Banco de Dados Vetorial** | ChromaDB (`chromadb`) |
| **Processamento de PDF** | `pypdf` + `PyPDFLoader` |
| **Hospedagem & Deploy** | Render |

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.11+** instalado.
- Uma chave de API do Google Gemini ([Google AI Studio](https://aistudio.google.com/)).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/JBEstevan/ai-code-mentor.git
   cd ai-code-mentor
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```powershell
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina sua Chave de API do Gemini (ou insira na barra lateral do app):**
   ```powershell
   # Windows (PowerShell)
   $env:GOOGLE_API_KEY="sua_chave_aqui"
   ```

5. **Inicie a aplicação Streamlit:**
   ```bash
   python -m streamlit run app.py
   ```

6. **Acesse no seu navegador:**
   [http://localhost:8501](http://localhost:8501)

---

## ⚙️ Variáveis de Ambiente & Deploy

Para configurar o deploy em serviços como **Render**, **Streamlit Cloud** ou **Railway**:

- **Variável de Ambiente:** `GOOGLE_API_KEY` (Sua chave da API do Google Gemini).
- **Comando de Build:** `pip install -r requirements.txt`
- **Comando de Inicialização:** `streamlit run app.py`

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---

<p align="center">
  Desenvolvido por <a href="https://github.com/JBEstevan">JBEstevan</a>
</p>