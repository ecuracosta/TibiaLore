from get_books_data import load_books, find_related_books, extract_relevant_words
from get_tibiawiki_data import get_page_sections, get_page_content, extract_section_by_anchor, extract_text

def gather_data(quest):
    sections = get_page_sections(quest)
    html_content = get_page_content(quest)
    wiki_scrapped = []
    for each_section in sections:
        section = {}
        each_section_anchor = each_section["anchor"]
        if each_section_anchor.startswith("Transcriptions") or each_section_anchor.startswith("Dialogs"):
            break
        else:
            content = extract_section_by_anchor(html_content, each_section_anchor)
            text = extract_text(content)
            section["section"] = each_section["line"]
            section["content"] = text
            wiki_scrapped.append(section)

    legend = extract_section_by_anchor(html_content, "Legend")
    legend_text = extract_text(legend)
    words = extract_relevant_words(legend_text)
    books = load_books("books_data.json")
    important_books = find_related_books(words, books)

    return quest, legend_text, wiki_scrapped, important_books[:6]

