import logging
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Visualizer:
    def display_keyword_frequency(self, keywords: list):
        """
        Displays a bar chart of keyword frequency.

        Args:
            keywords (list): A list of keywords.
        """
        logging.info("Displaying keyword frequency")
        try:
            fig, ax = plt.subplots()
            ax.barh(keywords, [1] * len(keywords), color='skyblue')
            ax.set_xlabel('Keyword Frequency')
            ax.set_title('Top 5 Keywords')
            plt.show()
            logging.info("Keyword frequency displayed")
        except Exception as e:
            logging.error(f"Error displaying keyword frequency: {e}")
            raise

    def generate_word_cloud(self, text: str):
        """
        Generates and displays a word cloud from the provided text.

        Args:
            text (str): The input text.
        """
        logging.info("Generating word cloud")
        try:
            wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(str(text))
            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            plt.show()
            logging.info("Word cloud generated")
        except Exception as e:
            logging.error(f"Error generating word cloud: {e}")
            raise

    def display_entity_distribution(self, ents):
        """
        Displays a pie chart of entity distribution.

        Args:
            ents: The entities detected by Spacy.
        """
        logging.info("Displaying entity distribution")
        try:
            labels = [ent.label_ for ent in ents]
            counts = {label: labels.count(label) for label in labels}
            fig, ax = plt.subplots()
            ax.pie(counts.values(), labels=list(counts.keys()), autopct='%1.1f%%')
            ax.axis('equal')
            plt.show()
            logging.info("Entity distribution displayed")
        except Exception as e:
            logging.error(f"Error displaying entity distribution: {e}")
            raise

    def display_dependency_graph(self, doc):
        """
        Displays a dependency graph for the provided Spacy doc.

        Args:
            doc: The Spacy doc object.
        """
        logging.info("Displaying dependency graph")
        try:
            edges = []
            for token in doc:
                for child in token.children:
                    edges.append(('{0}-{1}'.format(token.lower_, token.i), '{0}-{1}'.format(child.lower_, child.i)))
            graph = nx.Graph(edges)
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", alpha=0.6, edge_color="gray", font_size=10, font_color="black", font_weight="bold")
            plt.show()
            logging.info("Dependency graph displayed")
        except Exception as e:
            logging.error(f"Error displaying dependency graph: {e}")
            raise

    def display_heatmap(self, doc):
        """
        Displays a heatmap of token frequencies in the provided Spacy doc.

        Args:
            doc: The Spacy doc object.
        """
        logging.info("Displaying heatmap")
        try:
            tokens = [token.text for token in doc]
            token_freq = {token: tokens.count(token) for token in tokens}
            data = list(token_freq.values())
            heatmap_data = [data[i:i+10] for i in range(0, len(data), 10)]
            plt.figure(figsize=(10, 8))
            sns.heatmap(heatmap_data, annot=True, cmap='Blues')
            plt.show()
            logging.info("Heatmap displayed")
        except Exception as e:
            logging.error(f"Error displaying heatmap: {e}")
            raise
