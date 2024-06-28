import streamlit as st
import spacy
from spacy import displacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def analysis_page():
    st.title("Text Analysis Page")
    
    # Text input
    user_input = st.text_area("Enter text to analyze:", "")
    
    # Analyze button
    if st.button("Analyze"):
        if user_input:
            # Process text with SpaCy
            doc = nlp(user_input)
            
            # Display named entities
            st.subheader("Named Entities")
            if doc.ents:
                for ent in doc.ents:
                    st.write(f"{ent.text} ({ent.label_})")
            else:
                st.write("No named entities found.")
            
            # Display parts of speech
            st.subheader("Parts of Speech")
            pos_data = [(token.text, token.pos_, token.dep_, token.head.text) for token in doc]
            st.table(pos_data)
            
            # Display dependency parse
            st.subheader("Dependency Parse")
            html = displacy.render(doc, style="dep", jupyter=False)
            st.write(f"<div style='width: 100%; overflow-x: auto;'>{html}</div>", unsafe_allow_html=True)
        else:
            st.write("Please enter some text to analyze.")
