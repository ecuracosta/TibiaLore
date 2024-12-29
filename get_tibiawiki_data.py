import requests
import re

def get_page_sections(page_title: str):
    """
    Obtiene las secciones de una página de Tibia Wiki usando la API de MediaWiki.
    """
    endpoint = "https://tibia.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "sections"
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if "parse" in data and "sections" in data["parse"]:
            return data["parse"]["sections"]
    return None

def get_section_content(page_title: str, section_index: int):
    """
    Obtiene el contenido de una sección específica de una página.
    """
    endpoint = "https://tibia.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text",
        "section": section_index
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if "parse" in data and "text" in data["parse"]:
            return data["parse"]["text"]["*"]
    return None

def get_page_content(page_title: str):
    """
    Obtiene el contenido completo de una página de Tibia Wiki.
    """
    endpoint = "https://tibia.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text"
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if "parse" in data and "text" in data["parse"]:
            return data["parse"]["text"]["*"]
    return None

def extract_section_by_anchor(html_content: str, anchor: str) -> str:
    """
    Extracts the content of a specific section from the HTML using its anchor (id).
    """
    start_marker = f'id="{anchor}"'
    start_index = html_content.find(start_marker)
    if start_index == -1:
        return None

    end_index = html_content.find('<h', start_index + len(start_marker))
    section_content = html_content[start_index:end_index] if end_index != -1 else html_content[start_index:]
    return section_content.strip()


def extract_text(html_content: str) -> str:
    """
    Extracts the text from paragraphs in HTML content.
    """
    lines = html_content.splitlines()
    if lines and 'id=' in lines[0]:
        lines = lines[1:]
    merged_content = "\n".join(lines)
    text = re.sub(r"<br\s*/?>", "\n", merged_content)
    text = re.sub(r"<p>(.*?)</p>", r"\1\n\n", text)
    text = re.sub(r"<.*?>", "", text)
    return text.strip()


def extract_images(html_content: str) -> list:
    """
    Extracts the URLs of images from HTML content.
    """
    image_urls = re.findall(r'<img[^>]+src="([^"]+)"', html_content)
    return [url for url in image_urls if url.startswith("http")]
