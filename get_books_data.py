import json
import re
from nltk.corpus import stopwords

def load_books(json_file):
    # Abrir y leer el archivo JSON
    with open(json_file, 'r') as json_file:
        books = json.load(json_file)  # Convierte el JSON a un diccionario
    return books


def find_related_books(words, books):
    """
    Busca libros relacionados con una quest basándose en el título y contenido
    y los ordena por la cantidad de palabras coincidentes en el título.
    """
    related_books = []

    for book in books:
        # Count the number of matching words in the title
        matching_word_count = sum(1 for word in words if word.lower() in book["title"].lower())
        if matching_word_count > 0:
            # Append the book and the count as a tuple
            related_books.append((book, matching_word_count))

    # Sort the books by the count of matching words in descending order
    related_books.sort(key=lambda x: x[1], reverse=True)

    # Extract only the books from the sorted tuples
    return [book for book, _ in related_books]


def extract_relevant_words(text):
    # Tokenize and remove non-alphabetic characters
    words = re.findall(r'\b\w+\b', text.lower())

    # Load English stopwords
    stop_words = set(stopwords.words('english'))

    # Filter words that are not in stopwords
    filtered_words = [word for word in words if word not in stop_words]

    return filtered_words


