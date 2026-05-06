import re
from datetime import datetime

def parse_whatsapp(file_path):
    """
    Parses a WhatsApp chat export (.txt).
    Format typically: [DD/MM/YY, HH:MM:SS] Sender Name: Message
    or DD/MM/YY, HH:MM - Sender Name: Message
    """
    messages = []
    
    # Regex to match basic whatsapp format (brackets or no brackets)
    pattern = re.compile(r'^(?:\[)?(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}[, ]+\d{1,2}:\d{2}(?::\d{2})?)(?:\])?[\s\-]+([^:]+):\s*(.*)$')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                date_str, sender, content = match.groups()
                messages.append({
                    "timestamp": date_str,
                    "sender": sender.strip(),
                    "text": content.strip()
                })
            elif messages:
                # Append multi-line messages
                messages[-1]["text"] += "\n" + line.strip()
                
    return messages
