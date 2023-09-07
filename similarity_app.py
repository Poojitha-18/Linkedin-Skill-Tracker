"""
This script compares the similarity of terms entered by the user
using the SentenceTransformers library and Streamlit to display results.
"""

import streamlit as st
import numpy as np
from itertools import combinations
from sentence_transformers import SentenceTransformer, util

# Set page configuration
st.set_page_config(layout="wide")

# Define an empty list to store terms
terms = []

# Load the 'sentence-transformers/all-mpnet-base-v2' model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Define the terms to compare
term_insertion = st.text_input('Enter your terms separated by commas')

# Create button to trigger result
results = st.button("Result")

# Process terms when the button is clicked
if results:
    
    # if the list ends in a comma, remove it
    terms = [term.strip() for term in term_insertion.split(",") if term.strip() != ""]
   
    # Define headers for displaying terms and similarity score
    col1, col2, col3 = st.columns([0.3, 0.3, 0.3])

    # Display term1 header
    with col1:
        st.markdown("Term1")

    # Display term2 header
    with col2:
        st.markdown("Term2")

    # Display similarity score header
    with col3:
        st.markdown("Similarity Score")

    # Calculate the cosine similarity between all pairs of terms
    similarities = []
    combination = combinations(terms, 2)
    for value in combination:
        term1, term2 = value
        term1_encode = model.encode(term1)
        term2_encode = model.encode(term2)

        with col1:
            st.markdown(term1)
        with col2:
            st.markdown(term2)
        with col3:
            # Calculate cosine similarity score
            cosine_sim = util.cos_sim(term1_encode, term2_encode)[0][0]
            similar_val = float(str(cosine_sim)[7:-1])
            if similar_val > 0.6:
                st.markdown("Skills are very simillar - " +
                            str(similar_val)[:4])
            elif 0.5 < similar_val < 0.6:
                st.markdown("Skills are quite simillar - " + str(similar_val)[:4])
            elif 0.4 < similar_val <= 0.5:
                st.markdown("Skills are disparate - " + str(similar_val)[:4])
            else:
                st.markdown("Skills are highly disparate - " +
                            str(similar_val)[:4])
            similarities.append(similar_val)

    # Calculate the SSDI
    mean_similarity = np.mean(similarities)
    ssdi = np.std(similarities) / mean_similarity

    # Display the SSDI results
    if ssdi > 0.2:
        st.success("These skills are unlikely to be found in the same candidate '%s': %.2f" % (
            ", ".join(terms), ssdi))
    elif ssdi >= 0.1 and ssdi <= 0.2:
        st.success("These skills are likely to be found in the same candidate '%s': %.2f" % (
            ", ".join(terms), ssdi))
    elif ssdi < 0.15:
        st.success("Theseskills are highly likely to be found in the same candidate '%s': %.2f" % (
            ", ".join(terms), ssdi))
