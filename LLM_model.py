from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from transformers import pipeline

# Your Hugging Face token
huggingface_token = "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"

# Model configuration
model_name = "meta-llama/Llama-3.2-1B"

# Initialize the pipeline
print("Loading model...")
pipe = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

def build_prompt(nombre_quest, leyenda, secciones, libros):
    """
    Generates a prompt for the LLM to create an immersive quest narrative.

    Args:
        nombre_quest (str): Name of the quest.
        leyenda (str): Legend or introduction of the quest.
        secciones (list): List of sections with their descriptions.
        libros (list): List of books providing historical context.

    Returns:
        str: Generated prompt.
    """
    prompt = f"""You are an expert fantasy storyteller tasked with creating an immersive and cohesive narrative for a player engaging in the quest **{nombre_quest}** in a fantasy world. Your goal is to provide players with a clear, meaningful context for their actions as they progress through the quest. The story should align with the following structure:

1. **Introduction/Legend**: Introduce the quest, incorporating the legend or background provided. Make it engaging and mysterious, drawing players into the world while hinting at the significance of the challenges they will face.

2. **Quest Sections**: For each section of the quest, write a short narrative that seamlessly transitions from one objective to the next. Each section should explain:
   - Why the player is performing the task.
   - What they hope to achieve.
   - How this fits into the broader context of the quest or world.

3. **Books and Historical Context**: Use the historical details from the provided books as flavor or supporting details, but avoid creating contradictions with the main quest information. These elements should enhance the immersion but remain secondary to the quest narrative.

**Tone**: The tone should be serious and immersive, matching the grandeur of an epic story, while remaining clear and easy to follow for players.

**Rules**:
- Do not invent lore that contradicts the quest or book details provided.
- Focus on creating a sense of purpose and intrigue for each quest step.
- Use rich and evocative language to bring the world to life, but ensure the instructions and purpose for each section are clear.

### Information Provided:
1. **Quest Name**: {nombre_quest}

2. **Quest Legend/Introduction**: 
{leyenda}

3. **Quest Sections**:
"""
    for i, seccion in enumerate(secciones, start=1):
        prompt += f"\n{i}. **{seccion['section']}**: {seccion['content']}"

    prompt += "\n\n4. **Books and Historical Context**:\n"
    for i, libro in enumerate(libros, start=1):
        prompt += f"\n{i}. {libro}"

    prompt += """

When the narrative is ready, it should captivate the players, providing them with both a clear purpose and a reason to feel emotionally invested in the quest. Make sure each section transitions naturally into the next, creating a seamless and compelling journey."""
    prompt += "\nI will read the corresponding part before each step in the quest. They have the instructions, we need motivation."
    prompt += "\nWrite as if all of this was real."
    instructions_dict = {seccion['section']: "Fill with this step" for seccion in secciones}
    prompt += f"\nI need this format as output:\n{instructions_dict}"
    return prompt


def generate_story(quest_name, legend, sections, related_books):
    """
    Generates a story using the pipeline text generation API.

    Args:
        quest_name (str): Name of the quest.
        legend (str): Quest legend/introduction.
        sections (list): List of sections with their content.
        related_books (list): List of books for historical context.

    Returns:
        str: Generated story.
    """
    # Build the prompt
    prompt = build_prompt(quest_name, legend, sections, related_books)

    # Generate the story
    print("Generating story...")
    result = pipe(prompt, max_new_tokens=2000) #, temperature=0.8, top_p=0.85)
    # Extract the generated text and remove the prompt
    generated_text = result[0]["generated_text"]
    generated_only = generated_text[len(prompt):].strip()  # Remove the prompt part

    return generated_only

