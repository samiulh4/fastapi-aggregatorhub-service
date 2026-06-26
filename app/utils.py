import json

def load_context():
    with open("data/context.txt", "r", encoding="utf-8") as f:
        return f.read()
    
def load_message():
    with open("data/messages.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        return data['messages']   