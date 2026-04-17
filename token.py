import re

text = "Hello Harshala! Welcome to NLP @2026. Let's build AI models."

tokens = re.findall(r"[A-Za-z]+", text)
print(tokens)