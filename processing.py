import os
import pandas as pd
import json
from tqdm import tqdm

# Define a function to extract the desired information from a reaction
def extract_info(reaction):
    reactants = []
    products = []
    agents = []
    solvents = []
    
    if 'components' in reaction:
        for comp in reaction['components']:
            if 'smiles' in comp:
                if comp['role'] == 'Reactant':
                    reactants.append(comp['smiles'])
                elif comp['role'] == 'Product':
                    products.append(comp['smiles'])
                elif comp['role'] == 'Agent':
                    agents.append(comp['smiles'])
                elif comp['role'] == 'Solvent':
                    solvents.append(comp['smiles'])
    return {'Reactants': ', '.join(reactants),
            'Products': ', '.join(products),
            'Agents': ', '.join(agents),
            'Solvents': ', '.join(solvents)}

# Set the root directory for the files
root_dir = '/home/johaa/data/extract'

# Create a list of all JSON files in the root directory and its subdirectories
json_files = []
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(subdir, file))

# Initialize a progress bar
total_files = len(json_files)
with tqdm(total=total_files, desc='Processing files') as pbar:
    # Extract the information from each JSON file and store it in a list of dictionaries
    reactions_info = []
    for file in json_files:
        with open(file, 'r') as f:
            data = [json.loads(line) for line in f]
        for reaction in data:
            reactions_info.append(extract_info(reaction))
        # Update the progress bar
        pbar.update(1)

# Create a pandas DataFrame from the reactions information
df = pd.DataFrame(reactions_info)

# Save the DataFrame as a CSV file
df.to_csv('all_reactions.csv', index=False)

print('All files processed.')