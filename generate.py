from pathlib import Path

TEMPLATE_DIR = Path("templates")
OUTPUT_PATH = Path("cards.html")
WORDS_PATH = Path("words.tsv")


def read_tsv(file_path: Path) -> list[str]:
    """Reads a TSV file and returns a list of strings."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def generate_card(base_html: Path, word: str, description: str, question: str) -> str:
    """Generates an HTML card for a given word, description, and question."""

    base_html_text = base_html.read_text(encoding="utf-8")

    card_html = base_html_text.replace("{{WORD}}", word)
    card_html = card_html.replace("{{DESCRIPTION}}", description)
    card_html = card_html.replace("{{QUESTION}}", question)
    return card_html


def main() -> None:
    base_html = TEMPLATE_DIR / "card.html"
    index_html = TEMPLATE_DIR / "page.html"
    words = read_tsv(WORDS_PATH)
    cards_html = ""
    for line in words:
        word, description, question = line.split("\t")
        card_html = generate_card(base_html, word, description, question)
        cards_html += card_html + "\n"

    final_html = index_html.read_text(encoding="utf-8").replace("{{CARDS}}", cards_html)
    OUTPUT_PATH.write_text(final_html, encoding="utf-8")


if __name__ == "__main__":
    main()
