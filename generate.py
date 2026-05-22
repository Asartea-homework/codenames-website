from pathlib import Path


def read_tsv(file_path: Path) -> list[str]:
    """Reads a TSV file and returns a list of strings."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def generate_card(base_html: str, word: str, description: str, question: str) -> str:
    """Generates an HTML card for a given word, description, and question."""
    card_html = base_html.replace("{{WORD}}", word)
    card_html = card_html.replace("{{DESCRIPTION}}", description)
    card_html = card_html.replace("{{QUESTION}}", question)
    return card_html


def main():
    base_html = Path("card.html").read_text(encoding="utf-8")
    index_html = Path("page.html").read_text(encoding="utf-8")
    words = read_tsv(Path("words.tsv"))
    cards_html = ""
    for line in words:
        word, description, question = line.split("\t")
        card_html = generate_card(base_html, word, description, question)
        cards_html += card_html + "\n"

    final_html = index_html.replace("{{CARDS}}", cards_html)
    Path("index.html").write_text(final_html, encoding="utf-8")


if __name__ == "__main__":
    main()
