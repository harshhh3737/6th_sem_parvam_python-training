import random

def chatbot_response(user_input):
    user_input = user_input.lower()

    greetings = ["hello", "hi", "hey"]
    goodbye = ["bye", "exit", "quit"]
    
    if any(word in user_input for word in greetings):
        return random.choice(["Hello!", "Hi there!", "Hey! How can I help you?"])
    
    elif "how are you" in user_input:
        return "I'm just a program, but I'm doing great! 😊"
    
    elif "your name" in user_input:
        return "I'm your Python chatbot."
    
    elif "help" in user_input:
        return "I can chat with you. Try saying hello, ask my name, or say bye."
    
    elif any(word in user_input for word in goodbye):
        return "Goodbye! Have a nice day!"
    
    else:
        return "Sorry, I don't understand that yet."

# Chat loop
print("Chatbot: Hello! Type 'bye' to exit.")

while True:
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("Chatbot:", response)
    
    if user_input.lower() in ["bye", "exit", "quit"]:
        break
    tokens = tokenize_and_clean(user_input)