# 🤖 Chatbot com Histórico de Mensagens e Otimização de Tokens

Este projeto implementa um chatbot inteligente baseado na **API Groq**, utilizando a **LangChain** para gerenciar o histórico de conversas e otimizar o uso de tokens.

## 📌 Funcionalidades

✅ **Integração com a API Groq** para processamento de linguagem natural  
✅ **Gerenciamento de histórico de conversas** por sessão de usuário  
✅ **Otimização de tokens** para reduzir consumo de memória  
✅ **Sistema de prompts dinâmicos** para maior controle sobre as respostas  
✅ **Pipeline de execução otimizado** para melhor eficiência  

---

## 🛠 Tecnologias Utilizadas

- **Python 3.8+**  
- [LangChain](https://python.langchain.com/) - Framework para IA conversacional  
- [Groq API](https://groq.com/) - Modelo de IA para geração de respostas  
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente  

---

## 🚀 Como Configurar o Projeto

### 1️⃣ Clone o repositório  
```bash
git clone https://github.com/Raphaguizan/AI_app_memory.git
cd seu-repositorio
```

### 2️⃣ Crie um ambiente virtual e ative  
```bash
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate  # Windows  
```

### 3️⃣ Instale as dependências  
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure a chave da API Groq  
Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API:  
```env
GROQ_API_KEY=your_api_key_here
```

### 5️⃣ Execute o chatbot  
```bash
python main.py
```

---

## 📝 Exemplo de Uso  

```python
# Exemplo de interação com o chatbot
response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="Qual é o sorvete que eu gosto?")]
    }
)
print(response.content)
```

---

## 📖 Documentação do Código

### 📂 Estrutura do Projeto
```
/seu-repositorio
│── main.py               # Arquivo principal do chatbot
│── requirements.txt      # Dependências do projeto
│── .env                 # Chaves da API (não incluso no repositório)
│── README.md            # Documentação do projeto
```

### 📜 Explicação do Código

#### 📌 Importação de Bibliotecas
```python
import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
```
O código importa bibliotecas necessárias para interação com a API Groq e gerenciamento de histórico de mensagens.

#### 📌 Configuração do Ambiente
```python
load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```
Carrega as variáveis de ambiente do arquivo `.env` para acessar a API.

#### 📌 Inicialização do Modelo de IA
```python
llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=1
)
```
Cria uma instância do modelo **Groq AI** para processar mensagens.

#### 📌 Gerenciamento do Histórico de Conversas
```python
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
```
Cria e armazena históricos de mensagens por sessão.

#### 📌 Configuração do Pipeline de Execução
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente útil. Responda todas as perguntas com precisão."),
    MessagesPlaceholder(variable_name="messages")
])
```
Define um **template de prompt** para estruturar mensagens enviadas ao modelo.

#### 📌 Otimização do Uso de Tokens
```python
trimmer = trim_messages(
    max_tokens=45,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=False,
    start_on="human"
)
```
Implementa um **limitador de tokens** para evitar alto consumo de memória.

#### 📌 Execução da IA
```python
chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
    | prompt
    | llm
)
```
Cria um **pipeline de execução** para conectar as entradas do usuário ao modelo de IA.

#### 📌 Exemplo de Interação
```python
response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="Qual é o sorvete que eu gosto?")]
    }
)
print(response.content)
```
Executa uma consulta ao chatbot e exibe a resposta da IA.

---

## 📜 Licença  

Este projeto está licenciado sob a **MIT License**.  

---

💡 **Dúvidas ou sugestões?** Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.  

