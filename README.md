## <font color="chocolate">Ready-Tensor-Publication-Explorer-- RAG Chatbot </font>

### Project Description

### Concise Project Summary

### Project Overview
I will add detailed project overview

### Core Technologies 🛠️

    LangChain: For the core pipeline.
    Gemini API: For the LLM and embeddings (requires an API key).
    FAISS: For local vector storage (lightweight and fast).
    Python's input(): For a basic Command Line Interface (CLI).
    Python's logging: For basic logging.
    ConversationBufferMemory: For session-based memory (optional extension).


### 📸 ⛶ Screenshot
![Chatbot demo answering questions](image.png)
    ***`Chatbot demo answering questions`***

### Video demo


### Features
- 
- 
-
-
-
-
-



---


### Repository Structure
```
RAG_Chatbot_Project/
 ├─ data/
 │   ├─ project_1_publication.json
 │   ├─ raw/                # put source PDFs, txt, md, json
 │   └─ processed/          # normalized text, optional
 ├─ database/             # persisted Chroma or FAISS db
 ├─ assets/                 # logos, images
 ├─ src/
 │   ├─ __init__.py
 │   ├─ config.py           # central settings (chunk, k, provider, model)
 │   ├─ loaders.py          # handles pdf, md, txt, json
 │   ├─ splitter.py         # text split logic
 │   ├─ embeddings.py       # embedder factory (HF/Gemini/OpenAI)
 │   ├─ vectordb.py         # Chroma / FAISS wrapper
 │   ├─ retriever.py
 │   ├─ prompts.py          # keep all prompt templates
 │   ├─ llm.py
 │   ├─ rag_chain.py
 │   └─ ui/                 # user interfaces
 │       ├─ cli.py
 │       └─ gradio_app.py
 ├─ ingest.py
 ├─ app.py                  # thin launcher for Gradio UI
 └─ tests/                  # add later (pytest)
 ├─ .gitignore              # 
 ├─ .env_example
 ├─ README.md
 ├─ LICENSE
 ├─ requirements.txt        # dependencies
```
---



### 🚀 Getting Started

Welcome! This guide will help you set up and run your project with ease.
#### 📋 Prerequisites

Before you begin, make sure you have the following:

    ✅ Python 3.11 or higher installed

    🔑 Groq API Key (required)

    🔑 Google API Key (optional)

#### 🛠️Setup and Installation Guide
**Step 1: Create and Activate a Virtual Environment**

Open your command line interface (Command Prompt on Windows or Terminal on macOS/Linux), navigate to the root directory of your project directory, and run the following commands:
```env
    # Windows
    python -m venv venv
    venv\Scripts\activate
```
```env
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
```
<!-- If you're working on desktop, your command line should now look like: -->
Once activated, your command line prompt should look like:
```
    (venv) C:\Users\HP\Desktop\RAG_Chatbot_Project>  # Windows
    (venv) ~/Desktop/RAG Chatbot_Project$            # macOS / Linux
```


**Step 2. Install Dependencies**
Once your virtual environment is activated, you can install all required packages using a `requirements.txt` file.

🔹Create a file named `requirements.txt` inside the root with this content:
```txt
# Core
langchain>=0.2.12
langchain-community>=0.2.11
langchain-text-splitters>=0.2.2

# LLM providers
langchain-groq>=0.1.4
langchain-google-genai>=2.0.1

# Embeddings
sentence-transformers>=2.2.2
transformers>=4.30.0

# Vector DBs
chromadb>=0.5.5
faiss-cpu>=1.8.0

# UI, env, typing
gradio>=4.10
python-dotenv>=1.0
pydantic>=2.7
pytest>=7.4

```
Then install dependencies: `pip install -r requirements.txt`

**Step 3: Configuration**

Create a `.env` file in the root directory with the following variables to securely store your API key:
This helps keep sensitive information out of your codebase.
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```
>💡Replace your_groq_api_key_here and your_openai_api_key_here with your actual API keys. These keys are used to authenticate requests to Groq and OpenAI services.


**3. documents/ Folder and Sample Documents**<br/>
Create a folder named documents inside your rag_chatbot_project/ directory. <br/> You can add your custom .txt files here.

For example:

documents/project_alpha.txt<br/>
documents/company_info.txt<br/>
(You need to look at the sample code provided in the GitHub repository.)



---


```Python
// This is a code block
const a = 1;
```

### License
Licensed under the [MIT license](https://github.com/AbdiD21/Ready-Tensor-Publication-Explorer--Chatbot/blob/main/LICENSE).


###  Reference
I will put my publication link here

### Contact: 
abdid.yadata@gmail.com