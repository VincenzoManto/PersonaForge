import argparse
import json
import os
from parsers.whatsapp import parse_whatsapp
from parsers.telegram import parse_telegram
from dataset.formatter import create_jsonl_dataset
from agent.chat import chat_with_persona

def main():
    parser = argparse.ArgumentParser(description="PersonaForge: Create digital twins from chat logs.")
    subparsers = parser.add_subparsers(dest="command")

    # Parse Command
    parse_parser = subparsers.add_parser("parse", help="Parse chat logs into a dataset")
    parse_parser.add_argument("--app", choices=["whatsapp", "telegram"], required=True, help="Messaging app")
    parse_parser.add_argument("--file", required=True, help="Path to the exported chat file")
    parse_parser.add_argument("--target", required=True, help="Name of the person you want to clone (exact name in chat)")
    parse_parser.add_argument("--output", default="dataset.jsonl", help="Output JSONL dataset file")

    # Chat Command
    chat_parser = subparsers.add_parser("chat", help="Chat with the digital twin")
    chat_parser.add_argument("--dataset", required=True, help="Path to the parsed JSONL dataset")
    chat_parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use (e.g., gpt-4, claude-3-opus, gemini-pro)")

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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
