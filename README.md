# 🤖 Chatbot com Histórico de Mensagens e Otimização de Tokens

Este projeto implementa um chatbot inteligente baseado na **API Groq**, utilizando a **LangChain** para gerenciar o histórico de conversas e otimizar o uso de tokens.

## 📌 Funcionalidades

✅ **Integração com a API Groq** para processamento de linguagem natural\
✅ **Gerenciamento de histórico de conversas** por sessão de usuário\
✅ **Otimização de tokens** para reduzir consumo de memória\
✅ **Sistema de prompts dinâmicos** para maior controle sobre as respostas

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

## 📜 Licença

Este projeto está licenciado sob a **MIT License**.

---

💡 **Dúvidas ou sugestões?** Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

