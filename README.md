Job Skill Demand Forecasting Engine
===================================

This project analyzes job postings to identify and forecast the demand for various technical skills over time. It uses Python, pandas for data manipulation, and Meta's Prophet forecasting library to model trends. The results are presented in an interactive web application built with Streamlit.

This project was developed as part of the "Minor in AI" program at IIT Ropar.

Features
--------

*   **Data Processing**: Cleans and processes thousands of job listings from a raw CSV file.
    
*   **Skill Extraction**: Uses NLTK to parse job descriptions and identify mentions of pre-defined technical skills.
    
*   **Time-Series Forecasting**: Models the historical demand for each skill and forecasts future trends using Prophet.
    
*   **Interactive Dashboard**: A user-friendly web interface built with Streamlit to visualize and compare skill demand forecasts.
    
*   **Automated Testing**: Includes unit tests with pytest to ensure code quality and reliability.

Setup and Installation
----------------------

Follow these steps to set up the project environment locally.

### Prerequisites

*   Python 3.9+
    
*   pip and venv
    

### 1\. Clone the Repository

`git clone   cd Market_trend_AI`

### 2\. Create and Activate a Virtual Environment

*   python3 -m venv venvsource venv/bin/activate
    
*   python -m venv venv.\\venv\\Scripts\\activate
    

### 3\. Install Dependencies

Install all the required libraries from the requirements.txt file.
`pip install -r requirements.txt`

How to Run the Project
----------------------

Execute the following steps in order from the main project directory.

### 1\. Place Your Data

Ensure your raw dataset (e.g., linkedin-jobs-usa.csv) is placed inside the data/raw/ directory.

### 2\. Preprocess the Data

Run the preprocessing script to clean the data and extract skills. This will generate a jobs\_with\_skills.csv file in data/processed/.
`python src/data_preprocessing.py`

### 3\. Run the Forecasting Pipeline

Execute the main training script. This will analyze the processed data, train a model for each skill, and save the forecasts in the results/ folder.

`python src/train.py`

### 4\. Launch the Interactive Dashboard

Start the Streamlit application to view the results.

`streamlit run app.py`

Navigate to the local URL provided in your terminal (usually http://localhost:8501) to interact with the dashboard.

### 5\. Run Tests (Optional)

To verify the code's integrity, run the automated tests.

`pytest`

Technology Stack
----------------

*   **Programming Language**: Python
    
*   **Data Manipulation**: Pandas, NLTK
    
*   **Time-Series Forecasting**: Prophet (by Meta)
    
*   **Web Framework**: Streamlit
    
*   **Plotting**: Plotly
    
*   **Testing**: Pytest