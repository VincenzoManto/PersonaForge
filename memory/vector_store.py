import chromadb
import json

def build_memory_bank(dataset_file, collection_name="persona_memory"):
    """
    Ingests the entire chat history into a local Vector DB (Chroma)
    so the agent has 'infinite memory' of past events via RAG.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=collection_name)
    
    documents = []
    ids = []
    
    print("📚 Building Infinite Memory Bank (VectorDB)...")
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            user_msg = data["messages"][1]["content"]
            target_msg = data["messages"][2]["content"]
            
            
            doc = f"User said: {user_msg}\nTarget replied: {target_msg}"
            documents.append(doc)
            ids.append(f"mem_{i}")
            
    
    batch_size = 5400
    for i in range(0, len(documents), batch_size):
        collection.add(
            documents=documents[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
        
    print(f"🧬 Memory Bank built! {len(documents)} memories embedded.")

def recall_memories(query, collection_name="persona_memory", n_results=3):
    """
    Fetches relevant past conversations based on the current context.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=collection_name)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return results['documents'][0] if results['documents'] else []
