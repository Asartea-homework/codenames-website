from pathlib import Path
from typing import TypedDict

TEMPLATE_DIR = Path("templates")
OUTPUT_PATH = Path("cards.html")
WORDS_PATH = Path("words.tsv")
REFERENCES_PATH = Path("references.tsv")


class CardData:
    word: str
    description: str
    question: str
    references: list[tuple[str, str]] | None

    def __init__(
        self,
        word: str,
        description: str,
        question: str,
        references: list[tuple[str, str]] | None = None,
    ):
        self.word = word
        self.description = description
        self.question = question
        self.references = references

    def to_html(self, base_html: str) -> str:
        card_html = base_html.replace("{{WORD}}", self.word)
        card_html = card_html.replace("{{DESCRIPTION}}", self.description)
        card_html = card_html.replace("{{QUESTION}}", self.question)

        references_html = ""
        if self.references:
            for url, title in self.references:
                website = url.split("/")[2] if len(url.split("/")) > 2 else url
                references_html += f'<li><a href="{url}" target="_blank">{title}</a> ({website})</li>\n'
            card_html = card_html.replace("{{REFERENCES}}", references_html)
        else:
            card_html = card_html.replace("{{REFERENCES}}", "")

        return card_html


def read_tsv(file_path: Path) -> list[str]:
    """Reads a TSV file and returns a list of strings."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def main() -> None:
    base_html = TEMPLATE_DIR / "card.html"
    index_html = TEMPLATE_DIR / "page.html"
    words = read_tsv(WORDS_PATH)
    references_lines = read_tsv(REFERENCES_PATH)

    references: dict[str, list[tuple[str, str]]] = {}
    for line in references_lines:
        category, url, title = line.split("\t")
        if category not in references:
            references[category] = []
        references[category].append((url, title))

    cards_html = ""
    for line in words:
        word, description, question = line.split("\t")
        card_data = CardData(
            word=word,
            description=description,
            question=question,
            references=references.get(word, None),
        )
        card_html = card_data.to_html(base_html.read_text(encoding="utf-8"))
        cards_html += card_html + "\n"

    final_html = index_html.read_text(encoding="utf-8").replace("{{CARDS}}", cards_html)
    OUTPUT_PATH.write_text(final_html, encoding="utf-8")


if __name__ == "__main__":
    main()
