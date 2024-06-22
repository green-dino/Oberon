import json
import pandas as pd

# Step 1: Read the JSON file
with open('nice.json', 'r') as f:
    data = json.load(f)

# Step 2: Flatten the nested structure (recursive function)
def flatten_json(nested_json, prefix=''):
    flat_dict = {}
    for key, value in nested_json.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_json(value, prefix + key + '_'))
        else:
            flat_dict[prefix + key] = value
    return flat_dict

# Flatten the JSON
flattened_data = flatten_json(data)

# Step 3: Create a DataFrame
df = pd.DataFrame([flattened_data])

# Print the DataFrame
print(df)
