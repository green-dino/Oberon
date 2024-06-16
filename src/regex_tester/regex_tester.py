import re
import json

# Load patterns from an external configuration file (patterns.json)
with open('patterns.json', 'r') as f:
    patterns_config = json.load(f)

# Define REGEX patterns with descriptions
patterns = {k: (re.compile(bytes(v['pattern'], 'utf-8')), v['description']) for k, v in patterns_config.items()}

# Test data
test_strings = [
    b'ThisIsGood',
    b'http://www.example.com',
    b'myemail@example.com',
    b'123-456-7890',
    b'192.168.0.1',
    b'/folder/subfolder/file.txt',
    b'user@example.com; user2@example.com',
    b'Password@123',
    b'my_username#1234',
    b'https://www.example.com',
    b'01:23:45:67:89:ab',
    b'   leading whitespace',
    b'trailing whitespace   ',
    b'consecutive    whitespace'
]

# Function to match patterns
def match_patterns(string):
    matches = {}
    for pattern_type, (pattern, description) in patterns.items():
        match_list = [match.group().decode('utf-8') for match in re.finditer(pattern, string)]
        matches[pattern_type] = match_list if match_list else None
    return matches

# Test the patterns
for test_string in test_strings:
    print(f"Testing string: {test_string.decode('utf-8')}")
    matches = match_patterns(test_string)
    for pattern_type, match_list in matches.items():
        match_output = ', '.join(match_list) if match_list else 'None'
        print(f"{pattern_type}: {'Matched' if match_list else 'Not Matched'} | {match_output}")
    print()
