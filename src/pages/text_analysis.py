import streamlit as st
import spacy
from spacy import displacy
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('stopwords')

entity_types = ['PERSON', 'ORG', 'GPE', 'LOC']
selected_entities = st.sidebar.multiselect("Select Entity Types", entity_types, default=entity_types)

visualization_styles = {'dep': 'Dependency Parse', 'ent': 'Entity Recognition'}
selected_style = st.sidebar.selectbox("Choose Visualization Style", list(visualization_styles.keys()), index=0)

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]
    return filtered_text[:5]

def get_sentiment_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def main():
    st.title("Text Analysis Application")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Text Analysis"])

    if selection == "Text Analysis":
        analysis_page(selected_entities, selected_style)

def analysis_page(selected_entities, selected_style):
    st.header("Text Analysis Page")
    
    user_input = st.text_area("Enter text to analyze:", "")
    
    if st.button("Analyze"):
        if user_input:
            doc = nlp(user_input)
            
            # Filter entities based on user selection
            filtered_ents = [ent for ent in doc.ents if ent.label_ in selected_entities]
            
            st.subheader("Named Entities")
            if filtered_ents:
                for ent in filtered_ents:
                    st.write(f"{ent.text} ({ent.label_})")
            else:
                st.write("No named entities found.")
            
            # Display parts of speech
            st.subheader("Parts of Speech")
            pos_data = [(token.text, token.pos_, token.dep_, token.head.text) for token in doc]
            st.table(pos_data)
            
            # Display dependency parse or entity recognition based on user choice
            if selected_style == 'dep':
                html = displacy.render(doc, style="dep", jupyter=False)
                st.write(f"<div style='width: 100%; overflow-x: auto;'>{html}</div>", unsafe_allow_html=True)
            elif selected_style == 'ent':
                html = displacy.render(doc, style="ent", jupyter=False)
                st.write(f"<div style='width: 100%; overflow-x: auto;'>{html}</div>", unsafe_allow_html=True)
            
            # Additional text processing features
            sentiment_score = get_sentiment_score(user_input)
            st.subheader("Sentiment Score")
            st.write(f"Sentiment score: {sentiment_score}")
            
            keywords = extract_keywords(user_input)
            st.subheader("Keywords")
            st.write(f"Top 5 keywords: {', '.join(keywords)}")
        else:
            st.write("Please enter some text to analyze.")
    else:
        st.write("Click the Analyze button to start the analysis.")

if __name__ == "__main__":
    main()
