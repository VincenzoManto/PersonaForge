import json

def parse_telegram(file_path):
    """
    Parses a Telegram chat export (.json).
    """
    messages = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for msg in data.get("messages", []):
        if msg.get("type") == "message" and msg.get("from") and msg.get("text"):
            
            # Handle text that is a list of entities
            text = msg["text"]
            if isinstance(text, list):
                parsed_text = ""
                for entity in text:
                    if isinstance(entity, str):
                        parsed_text += entity
                    elif isinstance(entity, dict) and "text" in entity:
                        parsed_text += entity["text"]
                text = parsed_text
                
            messages.append({
                "timestamp": msg.get("date"),
                "sender": msg.get("from"),
                "text": text.strip()
            })
            
    return messages
