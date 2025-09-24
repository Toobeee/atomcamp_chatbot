# atomcamp_bot_day4.py - Polished Conversation

from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import random
import time
import sys

# -------------------------
# 1. Load API Key
# -------------------------
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY! Please set it in your environment.")

# -------------------------
# 2. Load Chroma DB
# -------------------------
print("📂 Loading Chroma DB...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# -------------------------
# 3. Setup memory
# -------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# -------------------------
# 4. Setup LLM (Groq)
# -------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=groq_api_key,
    temperature=0.7
)

# -------------------------
# 5. Build Conversational Retrieval Chain
# -------------------------
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)

# -------------------------
# 6. Predefined casual responses
# -------------------------
casual_responses = {
    "hi": "Hi there! I'm Atom AI, your friendly assistant at Atomcamp. How can I help you today?",
    "hello": "Hello! I'm Atom AI. Ask me anything about courses, bootcamps, or webinars!",
    "hey": "Hey! I'm Atom AI, your friendly assistant. What would you like to know today?",
    "thank you": "You're welcome! 😊 Happy to help.",
    "thanks": "Anytime! Let me know if you have more questions.",
     "thanku": "Anytime! Let me know if you have more questions.",
      "Thanks": "Anytime! Let me know if you have more questions.",
       "Thanku so much": "Anytime! Let me know if you have more questions."
}

fallback_responses = [
    "Hmm, I'm not entirely sure about that. Can you rephrase?",
    "Good question! Let me think… 🤔",
    "I'm still learning about that. Maybe try asking differently?"
]

# -------------------------
# 7. Typing effect function
# -------------------------
def bot_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

# -------------------------
# 8. Introduce bot
# -------------------------
bot_print("🤖 Hello! I am Atom AI, your friendly assistant for Atomcamp. Ask me anything about courses, bootcamps, or webinars. Type 'exit' to quit.\n")

# -------------------------
# 9. Run chat loop
# -------------------------
while True:
    query = input("You: ").strip()
    if query.lower() in ["exit", "quit"]:
        bot_print("Bot: Goodbye! 👋")
        break

    user_input_lower = query.lower()

    # Handle casual greetings or thanks first
    if user_input_lower in casual_responses:
        bot_print("Bot: " + casual_responses[user_input_lower])
        continue

    # Use QA chain
    result = qa.invoke({"question": query})
    answer = result.get("answer", "").strip()

    # -------------------------
    # 1. Fallback if answer is empty
    # -------------------------
    if not answer:
        answer = random.choice(fallback_responses)

    # -------------------------
    # 2. Add context reminder for follow-ups
    # -------------------------
    if memory.chat_memory.messages:
        if len(memory.chat_memory.messages) > 1:
            last_user_msg = memory.chat_memory.messages[-2].content
            if last_user_msg.lower() != query.lower():
                answer = f"(Regarding your previous question: '{last_user_msg}') {answer}"

    # -------------------------
    # 3. Make long answers readable
    # -------------------------
    if len(answer) > 300:
        sentences = answer.split(". ")
        answer = ".\n".join(sentences[:5]) + ("…" if len(sentences) > 5 else "")

    # -------------------------
    # 4. Optional truncation
    # -------------------------
    if len(answer) > 500:
        answer = answer[:500] + "…"

    # -------------------------
    # 5. Print bot answer with typing effect
    # -------------------------
    bot_print("Bot: " + answer)
