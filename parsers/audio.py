import json
import os
import shutil

def extract_voice_notes(telegram_json_path, output_dir="voice_dataset"):
    """
    Scans a Telegram JSON export for voice messages sent by the target
    and copies them to a dedicated directory for Voice Cloning (e.g., ElevenLabs, RVC).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(telegram_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    base_dir = os.path.dirname(telegram_json_path)
    count = 0
    
    print(f"🎙️ Scanning for voice notes...")
    for msg in data.get("messages", []):
        if msg.get("media_type") == "voice_message" and msg.get("file"):
            file_path = os.path.join(base_dir, msg["file"])
            if os.path.exists(file_path):
                dest = os.path.join(output_dir, os.path.basename(file_path))
                shutil.copy2(file_path, dest)
                count += 1
                
    print(f"✅ Extracted {count} voice notes to {output_dir}/. Ready for Voice Cloning!")
