from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from get_books_data import find_related_books

# Tu token de Hugging Face
huggingface_token = "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"

# Configuración del modelo
model_name = "meta-llama/Llama-3.2-1B-Instruct"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar el tokenizador y el modelo con tu token
print("Cargando el modelo...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_auth_token=huggingface_token
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # FP16 para usar menos memoria
    use_auth_token=huggingface_token,
    device_map="auto"
)

def build_prompt(quest_name, quest_content, related_books):
    """
    Construye un prompt para el modelo basado en la quest y libros relacionados.
    """
    prompt = f"Generate an immersive story based in the Tibia (RPG) quest:'{quest_name}'.\n"
    prompt += f"Quest legend: {quest_content}\n\n"

    if related_books:
        prompt += "Addional information that may be useful based on books in the game:\n"
        for book in related_books:
            prompt += f"- Title: {book['title']}\n"
            prompt += f"Text: {book['text'][:300]}...\n"  # Limitar a 300 caracteres
    else:
        prompt += "No books found.\n"

    prompt += "\nCreate a rich and colorful story with this information. Say truth."
    return prompt

# Función para generar la historia
def generate_story(quest_name, quest_content, books):
    """
    Genera una historia basada en la quest y los libros relacionados.
    """
    # Buscar libros relacionados
    related_books = find_related_books(quest_name, books, quest_content)

    # Crear el prompt
    prompt = build_prompt(quest_name, quest_content, related_books)

    model.to(device)
    # Tokenizar y generar texto
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=500,  # Incrementar para historias más largas
        do_sample=True,
        temperature=0.8,  # Más creatividad
        top_p=0.85  # Ajustar para mayor coherencia
    )

    # Decodificar el texto generado
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text
