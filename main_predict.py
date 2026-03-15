from src.predict import predict_next_month

if __name__ == "__main__":
    forecast = predict_next_month()
    print("\nNext Month Budget Forecast:\n")
    print(forecast)