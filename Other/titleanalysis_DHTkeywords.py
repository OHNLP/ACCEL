#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#pip install spacy
#python -m spacy download en_core_web_sm

import pandas as pd
import spacy
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# Load the dataset
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df['Title'].dropna().tolist()

# Preprocess the text using SpaCy
def preprocess_text(texts):
    preprocessed_texts = []
    for text in texts:
        doc = nlp(text.lower())
        tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
        preprocessed_texts.append(tokens)
    return preprocessed_texts

def perform_topic_modeling(preprocessed_texts, num_topics=10, num_words=10):
    # Create a dictionary and a corpus
    dictionary = Dictionary(preprocessed_texts)
    corpus = [dictionary.doc2bow(text) for text in preprocessed_texts]

    # Train LDA model with the specified number of topics
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=10)

    # Display topics
    topics = lda_model.print_topics(num_words=num_words)
    print(f"Generated {num_topics} topics:")
    for idx, topic in topics:
        print(f"Topic {idx}: {topic}")

    return lda_model, dictionary, corpus

# Update main to pass num_topics=10
def main():
    file_path = ""
    titles = load_data(file_path)
    preprocessed_texts = preprocess_text(titles)
    lda_model, dictionary, corpus = perform_topic_modeling(preprocessed_texts, num_topics=10, num_words=10)

if __name__ == "__main__":
    main()