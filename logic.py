import nltk
import numpy as np
import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download('punkt_tab')


def extractive_summarization(text, num_sentences):
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return "The text is too short for summarization!"

    # Convert sentences to numerical vectors using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    sentence_vectors = vectorizer.fit_transform(sentences)

    # Compute similarity matrix
    similarity_matrix = np.dot(sentence_vectors, sentence_vectors.T).toarray()

    # Apply TextRank algorithm (PageRank)
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Rank sentences based on importance
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Extract top N sentences
    summary_sentences = [ranked_sentences[i][1]
                         for i in range(min(num_sentences, len(sentences)))]
    return " ".join(summary_sentences)


# Example text
# text = """Artificial Intelligence (AI) is transforming industries worldwide.
#           It enables machines to learn from experience, adjust to new inputs,
#           and perform tasks that typically require human intelligence.
#           AI is widely used in healthcare, finance, and robotics.
#           Companies are investing heavily in AI-driven automation
#           to improve efficiency and reduce human effort.
#           The future of AI looks promising with continuous advancements in deep learning and NLP."""

# Get user input for number of sentences in summary
# num_sentences = int(input("Enter the number of sentences for the summary: "))

# summary = extractive_summarization(text, num_sentences)

# print("\n🔹 Original Text:\n", text)
# print("\n🔹 Summary:\n", summary)
