from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

# Load API key directly from environment
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model="llama-3.1-8b-instant"
)

# Memory to remember chat history
memory = ConversationBufferMemory()

# Conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

print("Chatbot with memory is ready! Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye! 👋")
        break
    response = conversation.predict(input=query)
    print("Bot:", response)
