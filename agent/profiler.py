import json
from litellm import completion

def extract_psychological_profile(dataset_file, model_name="gpt-4-turbo", output_file="character_card.json"):
    """
    Uses an LLM to read the chat dataset and generate a psychological profile,
    catchphrases, and personality traits (Character Card V2 format).
    """
    messages_text = ""
    with open(dataset_file, 'r', encoding='utf-8') as f:
        # Read a sample of the dataset to avoid token limits, say last 50 interactions
        lines = f.readlines()[-50:]
        for line in lines:
            data = json.loads(line)
            # user and assistant
            messages_text += f'User: {data["messages"][1]["content"]}\n'
            messages_text += f'Target: {data["messages"][2]["content"]}\n\n'

    prompt = f"""
    Analyze the following chat history and extract the psychological profile of 'Target'.
    Create a highly detailed personality profile including:
    1. Personality traits (Big Five).
    2. Common catchphrases or slang used.
    3. Fears, hopes, and relationships mentioned.
    4. Speech style (e.g., uses emojis? short sentences? sarcastic?).
    
    Chat History:
    {messages_text}
    
    Return ONLY a raw JSON object matching the TavernAI Character Card V2 spec, or a general descriptive JSON.
    """
    
    print("🧠 Extracting digital soul... this might take a minute.")
    response = completion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    
    card = response.choices[0].message.content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(card)
        
    print(f"✨ Psychological profile saved to {output_file}!")
