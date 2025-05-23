import pandas as pd
from prophet import Prophet
from query_data import fetch_tourism_data

def forecast_tourism(state):
    df = fetch_tourism_data(state)
    # Prepare for Prophet
    print(df.columns)

    df['ds'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-01')
    df['y'] = df['VISITORS_DOMESTIC']
    df = df[['ds', 'y']]

    model = Prophet(yearly_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=24, freq='M')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == "__main__":
    state = "Rajasthan"
    forecast_df = forecast_tourism(state)
    print(forecast_df.tail(12))
