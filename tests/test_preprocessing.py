# tests/test_preprocessing.py

# Import the function you want to test
from src.data_preprocessing import extract_skills

def test_extract_skills_found():
    """
    Tests if the function correctly finds skills that are present in the text.
    """
    # 1. Setup: Define your inputs and expected output
    skill_set = {'python', 'sql', 'tableau', 'aws'}
    job_description = "We are looking for a data analyst with strong python and sql skills. Experience with tableau is a plus."
    expected_skills = ['python', 'sql', 'tableau']
    
    # 2. Action: Call the function with the test data
    actual_skills = extract_skills(job_description, skill_set)
    
    # 3. Assert: Check if the actual output matches the expected output
    # We sort both lists to ensure the comparison is not affected by order
    assert sorted(actual_skills) == sorted(expected_skills)

def test_extract_skills_not_found():
    """
    Tests if the function correctly returns an empty list when no skills are found.
    """
    # 1. Setup
    skill_set = {'python', 'sql', 'tableau', 'aws'}
    job_description = "This is a role for a project manager. Looking for great communication skills."
    expected_skills = []
    
    # 2. Action
    actual_skills = extract_skills(job_description, skill_set)
    
    # 3. Assert
    assert actual_skills == expected_skills