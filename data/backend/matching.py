from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def cosine_match(resume_text, jd_text):


    resume_embedding = model.encode(
        resume_text
    )

    jd_embedding = model.encode(
        jd_text
    )



    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )


    
    match_percentage = similarity[0][0] * 100

    if match_percentage < 0:
        match_percentage = 0

    return round(float(match_percentage), 1)