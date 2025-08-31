# src/model.py

from prophet import Prophet
import pandas as pd

def forecast_skill_trend(data: pd.DataFrame, periods: int = 30):
    """
    Fits a Prophet model and returns a forecast.

    Args:
        data (pd.DataFrame): DataFrame with 'ds' and 'y' columns.
        periods (int): Number of future days to forecast.

    Returns:
        pd.DataFrame: A DataFrame containing the forecast.
    """
    if data.shape[0] < 2:
        print("Warning: Not enough data points to forecast. Skipping.")
        return None

    # Initialize and fit the Prophet model
    model = Prophet(daily_seasonality=True)
    model.fit(data)

    # Create a future dataframe for predictions
    future = model.make_future_dataframe(periods=periods)

    # Generate the forecast
    forecast = model.predict(future)

    return forecast

def plot_forecast(model: Prophet, forecast: pd.DataFrame, skill_name: str):
    """
    Generates forecast plots using Prophet's built-in plotting capabilities.
    """
    fig1 = model.plot(forecast)
    fig1.gca().set_title(f'Forecast for {skill_name.title()}', size=20)
    fig1.gca().set_xlabel('Date', size=15)
    fig1.gca().set_ylabel('Demand Count', size=15)

    fig2 = model.plot_components(forecast)

    return fig1, fig2