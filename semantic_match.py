from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_score(jd_text, resume_text):
    jd_embedding = model.encode([jd_text])
    resume_embedding = model.encode([resume_text])

    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]

    return round(similarity * 100, 2)
