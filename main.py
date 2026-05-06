import argparse
import json
import os
from parsers.whatsapp import parse_whatsapp
from parsers.telegram import parse_telegram
from parsers.audio import extract_voice_notes
from dataset.formatter import create_jsonl_dataset
from agent.chat import chat_with_persona
from agent.profiler import extract_psychological_profile
from memory.vector_store import build_memory_bank

def main():
    parser = argparse.ArgumentParser(description="PersonaForge: Resurrect digital footprints.")
    subparsers = parser.add_subparsers(dest="command")

    # Parse Command
    parse_parser = subparsers.add_parser("parse", help="Parse chat logs into a dataset")
    parse_parser.add_argument("--app", choices=["whatsapp", "telegram"], required=True, help="Messaging app")
    parse_parser.add_argument("--file", required=True, help="Path to the exported chat file")
    parse_parser.add_argument("--target", required=True, help="Name of the person you want to clone")
    parse_parser.add_argument("--output", default="dataset.jsonl", help="Output JSONL dataset file")

    # Chat Command
    chat_parser = subparsers.add_parser("chat", help="Chat with the digital twin")
    chat_parser.add_argument("--dataset", required=True, help="Path to the parsed JSONL dataset")
    chat_parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use")

    # Profile Command
    profile_parser = subparsers.add_parser("profile", help="Generate a psychological profile (Character Card V2)")
    profile_parser.add_argument("--dataset", required=True, help="Path to the parsed JSONL dataset")
    profile_parser.add_argument("--model", default="gpt-4-turbo", help="LLM to use for profiling")

    # Memory Command
    memory_parser = subparsers.add_parser("memory", help="Build Infinite Memory VectorDB (RAG)")
    memory_parser.add_argument("--dataset", required=True, help="Path to the parsed JSONL dataset")

    # Voice Command
    voice_parser = subparsers.add_parser("voice", help="Extract voice notes for ElevenLabs/RVC")
    voice_parser.add_argument("--file", required=True, help="Path to Telegram JSON export")

    args = parser.parse_args()

    if args.command == "parse":
        print(f"Parsing {args.app} chat from {args.file}...")
        if args.app == "whatsapp":
            messages = parse_whatsapp(args.file)
        elif args.app == "telegram":
            messages = parse_telegram(args.file)
        create_jsonl_dataset(messages, args.target, args.output)
        print(f"Dataset saved to {args.output}")

    elif args.command == "chat":
        print(f"Starting chat with model {args.model} using {args.dataset}...")
        chat_with_persona(args.dataset, args.model)
        
    elif args.command == "profile":
        extract_psychological_profile(args.dataset, args.model)
        
    elif args.command == "memory":
        build_memory_bank(args.dataset)
        
    elif args.command == "voice":
        extract_voice_notes(args.file)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
