# python pdf_to_archival_glossary.py
# ==========================================================
# PDF → JSON converter
# Dicionário Brasileiro de Terminologia Arquivística
# Método ATGN
# ==========================================================
import json
import spacy
from tqdm import tqdm

INPUT_JSON = "glossario_arquivistico.json"
OUTPUT_JSON = "glossario_arquivistico_canonico.json"

# carregar modelo português
nlp = spacy.load("pt_core_news_sm")


def canonicalize(term):

    doc = nlp(term)

    lemmas = []

    for token in doc:
        if token.is_punct:
            continue
        lemmas.append(token.lemma_)

    return " ".join(lemmas)


def main():

    print("Carregando glossário...")

    with open(INPUT_JSON, encoding="utf-8") as f:
        glossary = json.load(f)

    canonical_map = {}

    print("Gerando formas canônicas...")

    for term in tqdm(glossary.keys()):

        canonical = canonicalize(term)

        canonical_map[term] = canonical

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(canonical_map, f, ensure_ascii=False, indent=2)

    print("Glossário canônico salvo em:", OUTPUT_JSON)


if __name__ == "__main__":
    main()