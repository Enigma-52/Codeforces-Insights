from flask import Flask, render_template, request
import pandas as pd
from prophet import Prophet
import numpy as np
import requests

app = Flask(__name__)


def get_user_ratings(handle):
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    data = response.json()

    if "result" in data:
        ratings_data = data["result"]
        # Use the newRating data for predictions
        ratings = [entry["newRating"] for entry in ratings_data]
        return ratings
    else:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get username and number of predictions from the form
        username = request.form["username"]
        num_predictions = int(request.form["num_predictions"])

        # Get user ratings from Codeforces API
        user_ratings = get_user_ratings(username)

        if user_ratings:
            # Create a new DataFrame with the user's ratings
            user_df = pd.DataFrame(
                {
                    "ds": pd.date_range(
                        start="2023-01-01", periods=len(user_ratings), freq="D"
                    ),
                    "y": user_ratings,
                }
            )

            # Create Prophet model with user data
            model = Prophet(
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
            )
            model.add_seasonality(name="custom", period=7, fourier_order=5)
            model.fit(user_df)

            # Predict the ratings for the specified number of contests
            future = model.make_future_dataframe(periods=num_predictions)
            forecast = model.predict(future)
            predicted_ratings = forecast["yhat"].tail(num_predictions).tolist()

            # Combine user ratings and predicted ratings
            all_ratings = user_ratings + predicted_ratings

            # Render the template with data
            return render_template(
                "index.html", num_predictions=num_predictions, all_ratings=all_ratings
            )

    # Render the template without data if it's a GET request
    return render_template("index.html", all_ratings=[])


if __name__ == "__main__":
    app.run(debug=True)
