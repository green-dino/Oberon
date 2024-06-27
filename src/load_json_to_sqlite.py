import json
import sqlite3

# Your JSON data
with open('src/nice.json') as file:
    data = file.read()

# Parse JSON data
json_data = json.loads(data)

# Connect to SQLite database (or create it)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    doc_identifier TEXT PRIMARY KEY,
    name TEXT,
    version TEXT,
    website TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS relationship_types (
    relationship_identifier TEXT PRIMARY KEY,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS elements (
    element_identifier TEXT PRIMARY KEY,
    element_type TEXT,
    title TEXT,
    text TEXT,
    doc_identifier TEXT,
    FOREIGN KEY (doc_identifier) REFERENCES documents(doc_identifier)
)
''')

# Insert documents
for doc in json_data['response']['elements']['documents']:
    cursor.execute('''
    INSERT OR IGNORE INTO documents (doc_identifier, name, version, website)
    VALUES (?, ?, ?, ?)
    ''', (doc['doc_identifier'], doc['name'], doc['version'], doc['website']))

# Insert relationship_types
for rel in json_data['response']['elements']['relationship_types']:
    cursor.execute('''
    INSERT OR IGNORE INTO relationship_types (relationship_identifier, description)
    VALUES (?, ?)
    ''', (rel['relationship_identifier'], rel['description']))

# Insert elements
for elem in json_data['response']['elements']['elements']:
    cursor.execute('''
    INSERT OR IGNORE INTO elements (element_identifier, element_type, title, text, doc_identifier)
    VALUES (?, ?, ?, ?, ?)
    ''', (elem['element_identifier'], elem['element_type'], elem['title'], elem['text'], elem['doc_identifier']))

# Commit and close
conn.commit()
conn.close()
