import argparse
import json
import os
import time
from rich.console import Console
from parsers.whatsapp import parse_whatsapp
from parsers.telegram import parse_telegram
from parsers.audio import extract_voice_notes
from dataset.formatter import create_jsonl_dataset
from agent.chat import chat_with_persona
from agent.profiler import extract_psychological_profile
from memory.vector_store import build_memory_bank

console = Console()

def main():
    parser = argparse.ArgumentParser(description="PersonaForge: Resurrect digital footprints.")
    subparsers = parser.add_subparsers(dest="command")

    # One-Click God Mode: Resurrect
    resurrect_parser = subparsers.add_parser("resurrect", help="GOD MODE: Parse, Profile, Memorize, and Chat in one command!")
    resurrect_parser.add_argument("--app", choices=["whatsapp", "telegram"], required=True)
    resurrect_parser.add_argument("--file", required=True)
    resurrect_parser.add_argument("--target", required=True)
    resurrect_parser.add_argument("--model", default="gpt-4-turbo")

    # Parse Command
    parse_parser = subparsers.add_parser("parse", help="Parse chat logs into a dataset")
    parse_parser.add_argument("--app", choices=["whatsapp", "telegram"], required=True)
    parse_parser.add_argument("--file", required=True)
    parse_parser.add_argument("--target", required=True)
    parse_parser.add_argument("--output", default="dataset.jsonl")

    # Chat Command
    chat_parser = subparsers.add_parser("chat", help="Chat with the digital twin")
    chat_parser.add_argument("--dataset", required=True)
    chat_parser.add_argument("--model", default="gpt-3.5-turbo")
    chat_parser.add_argument("--use-memory", action="store_true", help="Enable RAG memory")

    # Profile Command
    profile_parser = subparsers.add_parser("profile", help="Generate a psychological profile")
    profile_parser.add_argument("--dataset", required=True)
    profile_parser.add_argument("--model", default="gpt-4-turbo")

    # Memory Command
    memory_parser = subparsers.add_parser("memory", help="Build Infinite Memory VectorDB")
    memory_parser.add_argument("--dataset", required=True)

    # Voice Command
    voice_parser = subparsers.add_parser("voice", help="Extract voice notes")
    voice_parser.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.command == "resurrect":
        console.print("[bold red]INITIATING DIGITAL RESURRECTION SEQUENCE...[/bold red]")
        output_ds = f"{args.target.replace(' ', '_').lower()}.jsonl"
        
        # 1. Parse
        console.print(f"[cyan]1. Parsing {args.app} logs...[/cyan]")
        if args.app == "whatsapp":
            messages = parse_whatsapp(args.file)
        else:
            messages = parse_telegram(args.file)
        create_jsonl_dataset(messages, args.target, output_ds)
        
        # 2. Profile
        console.print("[cyan]2. Extracting Psychological Profile...[/cyan]")
        extract_psychological_profile(output_ds, args.model)
        
        # 3. Memory
        console.print("[cyan]3. Building Neural Memory Bank (ChromaDB)...[/cyan]")
        build_memory_bank(output_ds)
        
        console.print("[bold green]RESURRECTION COMPLETE. LINKING CONSCIOUSNESS...[/bold green]")
        time.sleep(1)
        # 4. Chat
        chat_with_persona(output_ds, args.model, use_memory=True)

    elif args.command == "parse":
        print(f"Parsing {args.app} chat from {args.file}...")
        if args.app == "whatsapp":
            messages = parse_whatsapp(args.file)
        elif args.app == "telegram":
            messages = parse_telegram(args.file)
        create_jsonl_dataset(messages, args.target, args.output)
        print(f"Dataset saved to {args.output}")

    elif args.command == "chat":
        chat_with_persona(args.dataset, args.model, args.use_memory)
        
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
