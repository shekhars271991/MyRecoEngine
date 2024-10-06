# text_embedding_service.py

from sentence_transformers import SentenceTransformer

# Initialize the pre-trained model for text embeddings
text_model = SentenceTransformer('all-MiniLM-L6-v2')  # Choose an appropriate model

def get_text_embedding(text):
    if text:
        embedding = text_model.encode(text)
        return embedding
    else:
        # Return a zero vector if text is empty
        return [0] * text_model.get_sentence_embedding_dimension()
