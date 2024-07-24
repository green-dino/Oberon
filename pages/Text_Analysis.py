import streamlit as st
import spacy
from spacy import displacy
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import seaborn as sns

nltk.download('punkt')
nltk.download('stopwords')

entity_types = ['PERSON', 'ORG', 'GPE', 'LOC']
selected_entities = st.sidebar.multiselect("Select Entity Types", entity_types, default=entity_types)

visualization_styles = {'dep': 'Dependency Parse', 'ent': 'Entity Recognition'}

# Initialize session state for selected_style
if 'selected_style' not in st.session_state:
    st.session_state.selected_style = list(visualization_styles.keys())[0]

selected_style = st.sidebar.selectbox(
    "Choose Visualization Style", list(visualization_styles.keys()), index=0,
    on_change=lambda: setattr(st.session_state, 'selected_style', selected_style)
)

class TextAnalysisApp:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.entity_types = ['PERSON', 'ORG', 'GPE', 'LOC']
        self.visualization_styles = {'dep': 'Dependency Parse', 'ent': 'Entity Recognition'}

    def extract_keywords(self, text):
        word_tokens = word_tokenize(text)
        filtered_text = [w for w in word_tokens if w not in self.stop_words]
        return filtered_text[:5]

    def get_sentiment_score(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def display_keyword_frequency(self, keywords):
        fig, ax = plt.subplots()
        ax.barh(keywords, [1]*len(keywords), color='skyblue')
        ax.set_xlabel('Keyword Frequency')
        ax.set_title('Top 5 Keywords')
        st.pyplot(fig)

    def generate_word_cloud(self, text):
        wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(str(text))
        plt.figure(figsize=(10, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        st.pyplot(plt.gcf())

    def display_analysis_results(self, doc, selected_entities, selected_style):
        self.generate_word_cloud(doc.text)
        self.display_keyword_frequency(self.extract_keywords(doc.text))
        self.display_dependency_graph(doc)

    def display_entity_distribution(self, ents):
        labels = [ent.label_ for ent in ents]
        counts = {label: labels.count(label) for label in labels}
        fig, ax = plt.subplots()
        ax.pie(counts.values(), labels=list(counts.keys()), autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)

    def display_dependency_graph(self, doc):
        edges = []
        for token in doc:
            for child in token.children:
                edges.append(('{0}-{1}'.format(token.lower_, token.i), '{0}-{1}'.format(child.lower_, child.i)))

        graph = nx.Graph(edges)
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", alpha=0.6, edge_color="gray", font_size=10, font_color="black", font_weight="bold")
        st.pyplot(plt.gcf())

    def display_heatmap(self, doc):
        tokens = [token.text for token in doc]
        token_freq = {token: tokens.count(token) for token in tokens}
        data = list(token_freq.values())
        heatmap_data = [data[i:i+10] for i in range(0, len(data), 10)]
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, cmap='Blues')
        st.pyplot(plt.gcf())

    def save_results_to_file(self, results, filename="analysis_results.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Result Type", "Value"])
            for result in results:
                writer.writerow(result)

    def display_analysis_page(self):
        st.header("Text Analysis Page")
        
        uploaded_file = st.file_uploader("Upload a text file to analyze:", type=['txt'])
        if uploaded_file is not None:
            text = uploaded_file.getvalue().decode("utf-8")
        else:
            text = st.text_area("Enter text to analyze:", "")

        if st.button("Analyze"):
            if text:
                try:
                    doc = self.nlp(text)
                    st.subheader("Parts of Speech")
                    pos_data = [(token.text, token.pos_, token.dep_, token.head.text) for token in doc]
                    st.table(pos_data)
                    
                    if st.session_state.selected_style == 'dep':
                        html = displacy.render(doc, style="dep", jupyter=False)
                        st.write(f"<div style='width: 100%; overflow-x: auto;'>{html}</div>", unsafe_allow_html=True)
                    elif st.session_state.selected_style == 'ent':
                        html = displacy.render(doc, style="ent", jupyter=False)
                        st.write(f"<div style='width: 100%; overflow-x: auto;'>{html}</div>", unsafe_allow_html=True)
                    
                    if doc.ents:
                        self.display_entity_distribution(doc.ents)
                    
                    self.display_analysis_results(doc, self.entity_types, st.session_state.selected_style)
                    self.display_heatmap(doc)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please upload a file or enter some text to analyze.")
        else:
            st.info("Click the Analyze button to start the analysis.")

    def main(self):
        st.title("Text Analysis Application")
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", ["Text Analysis"])
        if selection == "Text Analysis":
            self.display_analysis_page()

if __name__ == "__main__":
    app = TextAnalysisApp()
    app.main()
