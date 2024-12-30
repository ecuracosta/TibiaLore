from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def build_prompt(nombre_quest, leyenda, secciones, libros, story, index):
    """
    Generates a prompt for the LLM to create an immersive quest narrative.
    """
    prompt = f"""
    You are an expert medieval fantasy storyteller tasked with creating an immersive and cohesive narrative for 
    adventurers engaging in the quest **{nombre_quest}** in the RPG Tibia. 
    Your goal is to write a clear, meaningful context for the quest.

    **Quest Legend (This is the most important information)**: 
    {leyenda}
    """
    prompt += "\n**Books and Historical Context (This is for you to fill gaps and be creating without need of inventing)**:\n"
    for i, libro in enumerate(libros, start=1):
        prompt += f"\n{i}. {libro}"
        
    prompt +=  "\nHere is the story of the quest so far:"
    prompt += f"{story}"
    prompt +=  "\nYou need to write a story that encompasses the following quest section:"
    prompt += f"{secciones[index]['section']}: {secciones[index]['content']}"
    prompt +=  "\nYou need to provide them with a clear purpose to feel emotionally invested in this particular part of quest."
    prompt += "\nPlease write the context for this part of the quest as one paragraph only, keep it SHORT and only write that (no titles, no introductions, the paragraph ONLY)."
    return prompt

def generate_story(nombre_quest, leyenda, secciones, libros, story, index):
    # Model setup

    model_name = "meta-llama/Llama-3.2-1B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    
    # Build prompt
    quest_prompt = build_prompt(nombre_quest, leyenda, secciones, libros, story, index)

    # Generate output
    output = generation_pipeline(
        quest_prompt,
        max_new_tokens=500,
        temperature=0.7,
        top_p=0.9
    )
    
    # Print the generated narrative
    generated_text = output[0]["generated_text"]
    generated_only = generated_text[len(quest_prompt):].strip()  # Remove the prompt part
    return generated_only
