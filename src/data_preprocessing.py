import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import json
import re

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK 'punkt' resource not found. Downloading...")
    nltk.download('punkt')

# Function to load skills from your config file
def load_skills(path='configs/skills.json'):
    with open(path, 'r') as f:
        skills_data = json.load(f)
    # Flatten the list of skills into a single set for efficient lookup
    all_skills = set()
    for category in skills_data.values():
        all_skills.update([skill.lower() for skill in category])
    return all_skills

# Function to extract skills from a text
def extract_skills(text, skill_set):
    # Normalize text: lowercase and tokenize
    text = str(text).lower()
    words = set(word_tokenize(text))

    # Find intersection between words in text and our skill set
    found_skills = words.intersection(skill_set)

    # Use regex for multi-word skills or variations (e.g., "node.js")
    # This can be expanded for more complex cases
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)

    return list(found_skills)

if __name__ == "__main__":
    # Load the specific USA jobs CSV
    try:
        df = pd.read_csv('data/raw/linkedin-jobs-usa.csv')
    except FileNotFoundError:
        print("Error: 'linkedin-jobs-usa.csv' not found in data/raw/. Please add it.")
        exit()

    # Load the skills from your config file
    skills_to_find = load_skills()
    
    # --- IMPORTANT: MAKE SURE THESE COLUMN NAMES ARE CORRECT ---
    # Use 'description' for skill extraction and 'posted_date' for the timestamp.
    # These should match the columns you saw in your EDA.
    description_col = 'description'
    date_col = 'posted_date'
    
    # Clean the dataframe
    df.dropna(subset=[description_col], inplace=True)
    df.drop_duplicates(subset=['title', 'company', description_col], inplace=True)
    
    # Apply the skill extraction function
    print("Extracting skills from job descriptions...")
    df['skills'] = df[description_col].apply(lambda x: extract_skills(x, skills_to_find))
    
    # Filter out jobs where no skills were found
    df = df[df['skills'].apply(len) > 0]
    
    # Convert the date column to datetime objects
    df['timestamp'] = pd.to_datetime(df[date_col])
    
    # Save the processed data
    df.to_csv('data/processed/jobs_with_skills.csv', index=False)
    print("Processing complete. Processed data saved to data/processed/jobs_with_skills.csv")