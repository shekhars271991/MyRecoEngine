from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(input):
    embeddings = model.encode(input)
    return embeddings
