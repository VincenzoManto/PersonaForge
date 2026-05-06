import json
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def chat_with_persona(dataset_file, model_name):
    """
    Starts an interactive terminal chat simulating the persona using few-shot learning
    based on the extracted dataset.
    """
    # Load some examples from the dataset to use as context
    examples = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))
            
    if not examples:
        print("Dataset is empty.")
        return

    # Extract target name from the system prompt of the first example
    system_prompt = examples[0]["messages"][0]["content"]
    target_name = system_prompt.replace("You are ", "").split(".")[0]

    # Build history with system prompt and some few-shot examples
    messages = [{"role": "system", "content": system_prompt + " Use the following examples to understand the tone."}]
    
    for ex in examples[-5:]:  # Use last 5 interactions as few-shot
        messages.append(ex["messages"][1]) # User
        messages.append(ex["messages"][2]) # Assistant
        
    print(f"\n--- Inizio Chat con {target_name} ---")
    print("Scrivi 'esci' per terminare.\n")
    
    while True:
        try:
            user_input = input("Tu: ")
            if user_input.lower() in ['esci', 'exit', 'quit']:
                break
                
            messages.append({"role": "user", "content": user_input})
            
            response = completion(
                model=model_name,
                messages=messages
            )
            
            assistant_reply = response.choices[0].message.content
            print(f"\n{target_name}: {assistant_reply}\n")
            
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Errore: {e}")
