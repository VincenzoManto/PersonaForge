import json
import os
from litellm import completion
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from memory.vector_store import recall_memories

load_dotenv()
console = Console()

def chat_with_persona(dataset_file, model_name, use_memory=False):
    """
    Starts an interactive terminal chat simulating the persona using few-shot learning
    and optional RAG memory via ChromaDB. Uses a beautiful Rich TUI.
    """
    examples = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))
            
    if not examples:
        console.print("[bold red]Dataset is empty![/bold red]")
        return

    # Extract target name
    system_prompt = examples[0]["messages"][0]["content"]
    target_name = system_prompt.replace("You are ", "").split(".")[0]

    # Load psychological profile if exists
    profile_data = ""
    if os.path.exists("character_card.json"):
        with open("character_card.json", "r", encoding="utf-8") as f:
            profile_data = f.read()

    enhanced_system_prompt = system_prompt
    if profile_data:
        enhanced_system_prompt += f"\n\nPsychological Profile & Traits:\n{profile_data}"
        
    messages = [{"role": "system", "content": enhanced_system_prompt + " Use the following examples to understand the tone."}]
    
    for ex in examples[-5:]:  # few-shot examples
        messages.append(ex["messages"][1]) # User
        messages.append(ex["messages"][2]) # Assistant

    console.print(Panel.fit(f"[bold green]NEURAL LINK ESTABLISHED[/bold green]\nTarget: [bold cyan]{target_name}[/bold cyan]\nModel: [yellow]{model_name}[/yellow]\nMemory Bank (RAG): [{'green]ACTIVE' if use_memory else 'red]OFF'}][/]", border_style="green"))
    console.print("[dim italic]Type 'exit' or 'esci' to sever the connection.[/dim italic]\n")
    
    while True:
        try:
            user_input = Prompt.ask(f"[bold magenta]You[/bold magenta]")
            if user_input.lower() in ['esci', 'exit', 'quit']:
                console.print("\n[bold red]Connection severed.[/bold red]")
                break
                
            # RAG Memory integration
            current_prompt = user_input
            if use_memory:
                memory_context = recall_memories(user_input)
                if memory_context:
                    current_prompt = f"[System: The user just said: '{user_input}'. Here are some past memories that might be relevant: {memory_context}]\n\nRespond to the user naturally based on this memory context: {user_input}"
            
            messages.append({"role": "user", "content": current_prompt})
            
            with console.status(f"[bold cyan]{target_name}[/bold cyan] is typing...", spinner="dots"):
                response = completion(
                    model=model_name,
                    messages=messages
                )
            
            assistant_reply = response.choices[0].message.content
            
            # Print with panel
            console.print(Panel(assistant_reply, title=f"[bold cyan]{target_name}[/bold cyan]", border_style="cyan"))
            
            # Append clean reply to history
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Connection severed.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
