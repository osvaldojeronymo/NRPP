# python clean_archival_glossary.py
import json
import re
from tqdm import tqdm

INPUT_JSON = "glossario_arquivistico_canonico.json"
OUTPUT_JSON = "glossario_arquivistico_limpo.json"


def is_valid_term(term):

    term = term.strip().lower()

    # remover termos muito curtos
    if len(term) < 3:
        return False

    # remover termos muito longos
    if len(term) > 40:
        return False

    # remover termos com muitas palavras
    if len(term.split()) > 3:
        return False

    # remover letras repetidas (ex: cccccóóóópppppiaaaa)
    if re.search(r'(.)\1{3,}', term):
        return False

    # remover termos com muitos caracteres estranhos
    if re.search(r'[^\w\s\-áéíóúãõâêôç]', term):
        return False

    # remover linhas que são apenas letras isoladas
    if re.fullmatch(r'[a-z]', term):
        return False

    return True


def main():

    print("Carregando glossário...")

    with open(INPUT_JSON, encoding="utf-8") as f:
        glossary = json.load(f)

    cleaned = {}

    print("Limpando termos...")

    for term, canonical in tqdm(glossary.items()):

        if is_valid_term(term):

            cleaned[term] = canonical

    print("Termos antes:", len(glossary))
    print("Termos depois:", len(cleaned))

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("Glossário limpo salvo em:", OUTPUT_JSON)


if __name__ == "__main__":
    main()