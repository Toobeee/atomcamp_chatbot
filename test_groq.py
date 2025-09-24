import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

resp = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello Groq, just testing!"}]
)

print(resp.choices[0].message.content)
