from groq import Groq

client = Groq(api_key="YOUR_GROQ_KEY")
print(client.models.list())