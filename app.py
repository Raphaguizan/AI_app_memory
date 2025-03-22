# IMPORTAÇÃO DE BIBLIOTECAS
import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory                   # Permite criar históricos de mensagens
from langchain_core.chat_history import BaseChatMessageHistory                              # Classe base para histórico de mensagens
from langchain_core.runnables.history import RunnableWithMessageHistory                     # Permite gerenciar o histórico de mensagens
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder                  # Permite criar prompts / mensagens
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages   # Mensagem humanas, do sistema e da AI
from langchain_core.runnables import RunnablePassthrough                                    # Permite criar fluxos de execução e reutilizaveis
from operator import itemgetter                                                             # Facilita a extração de valores de dicionários


# CARREGAR AS VARIÁVEIS DE AMBIENTE DO ARQUIVO DOTENV
load_dotenv(find_dotenv())

# OBTER A CHAVE DA API DO GROQ ARMAZENADA DO ARQUIVO DOTENV
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# INICIALIZAR O MODELO DE AI UTILIZANDO A API DA GROQ
llm = ChatGroq(
    model = "gemma2-9b-it",
    groq_api_key = GROQ_API_KEY,
    temperature=1
)

# DICIONÁRIO PARA ARMAZENAR O HISTÓRICO DE MENSAGENS
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Recupera ou cria um histórico de mensagens para uma detremidada sessão.
    Isso permite manter o contexto contínuo para diferentes usuários e interações
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Criar um gerencador de histórico que conecta o modelo ao armazenamento de mensagem
with_message_history = RunnableWithMessageHistory(llm, get_session_history)

# Configuração da sessão (identificador único para cada chat/usuário)
config = {"configurable":{"session_id":"chat1"}}

# Exemplo de interação inicial do usuário
#response = with_message_history.invoke(
#    [HumanMessage(content="oi, meu nome é Raphael e eu sou programador.")],
#    config=config
#)

# Criação de um prompt template para estruturar a entrada do modelo
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil. Responda todas as perguntas com precisão."),
        MessagesPlaceholder(variable_name="messages") # Permiritr adicionar mensagens de forma dinâmica
    ]
)

# Conectar o modelo ao template de prompt
chain = prompt | llm # Usando LCEL para conectar o prompt ao modelo

# Exemplo de interação com o modelo usando o template
#response = chain.invoke(
#    {"messages": [HumanMessage(content="Oi, o meu nome é Raphael")]}
#)

# Gerenciamento da memória do chatbot
trimmer = trim_messages(
    max_tokens = 45, # define um limite máximo de tokens para evitar ultrapassar o conseumo de memória
    strategy = "last",  # define a estratégia de corte para remover mensagens antigas
    token_counter = llm, # Usa o modelo para contar os tokens
    include_system = True, # Inclui mensagens do sistema no histórico
    allow_partial = False, # evita que as mesagens sejam cortadas parcialmente
    start_on = "human"  # começa a contagem com a mensagem humana
)

# Exemplo de histórico de mensagens
messages = [
    SystemMessage(content="Você é um assistente útil. reponda todas as perguntas de forma precisa."),
    HumanMessage(content="oi, meu nome é John Wick."),
    AIMessage(content="Olá John, Como você tá?"),
    HumanMessage(content="Eu gosto de sorvete de tapioca.")
]


# aplicar o limitador de memória ao histórico
trimmer.invoke(messages)

# criando um pipeline de excução para otimizar a passagem de informações entre componentes
chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) # Aplica a otimização do histórico
    | prompt # passa a entrada pelo template do prompt
    | llm # passa a entrada pelo modelo
)


#exemplo de interação utilizando o pipeline otimizado
response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="Qual é o sorvete que eu gosto?")]
    }
)

# Exibir a resposta do modelo
print("resposta do modelo:\n", response.content)