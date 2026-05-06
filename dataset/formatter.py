import json

def create_jsonl_dataset(messages, target_name, output_file):
    """
    Creates a conversational JSONL dataset format suitable for fine-tuning.
    Pairs user messages with the target's replies.
    """
    dataset = []
    
    
    
    
    conversations = []
    current_user_msg = ""
    current_target_msg = ""
    last_sender = None
    
    for msg in messages:
        sender = msg["sender"]
        text = msg["text"]
        
        if not text:
            continue
            
        if sender == target_name:
            if last_sender != target_name and last_sender is not None:
                current_target_msg = text
            else:
                current_target_msg += "\n" + text
        else:
            if last_sender == target_name and current_user_msg and current_target_msg:
                
                conversations.append({
                    "messages": [
                        {"role": "system", "content": f"You are {target_name}. Respond as they would, matching their tone and style."},
                        {"role": "user", "content": current_user_msg.strip()},
                        {"role": "assistant", "content": current_target_msg.strip()}
                    ]
                })
                current_user_msg = text
                current_target_msg = ""
            else:
                current_user_msg += "\n" + text if current_user_msg else text
                
        last_sender = sender

    with open(output_file, 'w', encoding='utf-8') as f:
        for conv in conversations:
            f.write(json.dumps(conv) + '\n')
