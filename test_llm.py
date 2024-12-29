from get_books_data import load_books
from LLM_model import generate_story


# Cargar los libros
books = load_books("books_data.json")

# Generar historia basada en una quest
quest_name = "The Pits of Inferno Quest"
quest_content = (
    "The once glorious Nightmare Knights have established themselves under the fiery pits of inferno to fight off evil. "
    "The pits of inferno, however, contain thrones that have a little of the spirit of each of the ruthless seven trapped in there. "
    "Absorb their spirit to claim your prize!"
)
story = generate_story(quest_name, quest_content, books)

# Mostrar la historia generada
print("\nHistoria Generada:")
print(story)