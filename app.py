import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- App Configuration ---
st.set_page_config(page_title="Job Skill Demand Forecaster", layout="wide")
st.title("📊 Job Skill Demand Forecasting Engine")
st.write("This app visualizes the historical demand for various job skills and forecasts future trends using Prophet.")

# --- Data Loading (with caching for performance) ---
@st.cache_data
def load_data(results_dir='results', history_dir='data/processed/timeseries'):
    """
    Loads all forecast and historical data from the specified directories.
    """
    all_files = os.listdir(results_dir)
    skill_files = [f for f in all_files if f.endswith('_forecast.csv')]
    
    forecasts = {}
    histories = {}
    
    for f in skill_files:
        skill_name = f.replace('_forecast.csv', '')
        
        # Load forecast
        forecast_path = os.path.join(results_dir, f)
        forecast_df = pd.read_csv(forecast_path)
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        forecasts[skill_name] = forecast_df
        
        # Load corresponding history
        history_path = os.path.join(history_dir, f'{skill_name}_timeseries.csv')
        if os.path.exists(history_path):
            history_df = pd.read_csv(history_path)
            history_df['ds'] = pd.to_datetime(history_df['ds'])
            histories[skill_name] = history_df
            
    return forecasts, histories

# --- Plotting Function ---
def create_forecast_plot(forecast_df, history_df, skill_name):
    """
    Creates an interactive Plotly chart for the selected skill's forecast.
    """
    merged_df = forecast_df.merge(history_df, on='ds', how='left')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=merged_df['ds'], y=merged_df['yhat_upper'], mode='lines', line=dict(width=0), fillcolor='rgba(68, 137, 238, 0.2)', hoverinfo='none', showlegend=False))
    fig.add_trace(go.Scatter(name='Uncertainty', x=merged_df['ds'], y=merged_df['yhat_lower'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(68, 137, 238, 0.2)', hoverinfo='none', showlegend=True))
    fig.add_trace(go.Scatter(name='Forecast', x=merged_df['ds'], y=merged_df['yhat'], mode='lines', line=dict(color='rgb(68, 137, 238)', width=3)))
    fig.add_trace(go.Scatter(name='Actual Data', x=merged_df['ds'], y=merged_df['y'], mode='markers', marker=dict(color='black', size=4)))
    
    fig.update_layout(title=f'Forecast for "{skill_name.title()}" Skill Demand', xaxis_title='Date', yaxis_title='Daily Mentions in Job Postings', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

# --- Main App Logic ---
all_forecasts, all_histories = load_data()

if not all_forecasts:
    st.error("No forecast data found. Please run `python src/train.py` first.")
else:
    skill_list = sorted(all_forecasts.keys())
    
    # Create a dropdown menu in the sidebar
    st.sidebar.header("Select a Skill")
    selected_skill = st.sidebar.selectbox("Choose a skill to visualize:", skill_list)
    
    if selected_skill:
        # Retrieve the data for the selected skill
        forecast_data = all_forecasts[selected_skill]
        history_data = all_histories.get(selected_skill, pd.DataFrame(columns=['ds', 'y'])) # Handle case where history might be missing
        
        # Create and display the plot
        st.header(f"Analysis for: {selected_skill.title()}")
        forecast_fig = create_forecast_plot(forecast_data, history_data, selected_skill)
        st.plotly_chart(forecast_fig, use_container_width=True)