from langchain_groq import ChatGroq

# Initialize Groq chatbot (Llama 3 model)
llm = ChatGroq(model="llama3-8b-8192")

print("🤖 Chatbot is ready! Type 'quit' anytime to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Bot: Goodbye 👋")
        break
    response = llm.invoke(user_input)
    print("Bot:", response.content)
