from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_plot_embeddings(movie_plot):
    plot_embeddings = model.encode(movie_plot)
    return plot_embeddings
