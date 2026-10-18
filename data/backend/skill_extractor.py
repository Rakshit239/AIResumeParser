
import os
import pandas as pd
import spacy

from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

matcher = PhraseMatcher(
    nlp.vocab,
    attr="LOWER"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKILL_FILE = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "skills",
        "skills.csv"
    )
)
print(SKILL_FILE)
df = pd.read_csv(SKILL_FILE)

skills = (
    df["skill"]
    .dropna()
    .astype(str)
    .tolist()
)

patterns = [
    nlp.make_doc(skill)
    for skill in skills
]

matcher.add(
    "SKILLS",
    patterns
)


def extract_skills(text):

    doc = nlp(text)

    matches = matcher(doc)

    found = set()

    for _, start, end in matches:

        found.add(
            doc[start:end].text
        )

    return sorted(found)