import json

def load_books(json_file):
    # Abrir y leer el archivo JSON
    with open(json_file, 'r') as json_file:
        books = json.load(json_file)  # Convierte el JSON a un diccionario
    return books

def find_related_books(quest_name, books, quest_content=None):
    """
    Busca libros relacionados con una quest basándose en el título y contenido.
    """
    related_books = []
    for book in books:
        # Buscar en el título
        if quest_name.lower() in book["title"].lower():
            related_books.append(book)
    return related_books


