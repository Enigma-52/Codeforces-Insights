from flask import Flask, render_template, request
import pandas as pd
from prophet import Prophet
import numpy as np
import requests
from collections import Counter

app = Flask(__name__, static_url_path="/static")


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


def get_user_ranks(handle):
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    data = response.json()

    if "result" in data:
        ratings_data = data["result"]
        # Use the newRating data for predictions
        ratings = [entry["rank"] for entry in ratings_data]
        return ratings
    else:
        return None


def get_submission_data(handle):
    api_url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(api_url)
    json_data = response.json()
    json_data = json_data["result"]

    verdict_data = [entry["verdict"] for entry in json_data]
    verdict_count = {}
    for verdict in verdict_data:
        if verdict in verdict_count:
            verdict_count[verdict] += 1
        else:
            verdict_count[verdict] = 1

    verdictData = [["Verdict", "Count"]] + [
        [verdict, count] for verdict, count in verdict_count.items()
    ]

    for item in verdictData:
        if "TIME_LIMIT_EXCEEDED" in item:
            item[item.index("TIME_LIMIT_EXCEEDED")] = "TLE"
        if "WRONG_ANSWER" in item:
            item[item.index("WRONG_ANSWER")] = "WA"
        if "MEMORY_LIMIT_EXCEEDED" in item:
            item[item.index("MEMORY_LIMIT_EXCEEDED")] = "MLE"
        if "OK" in item:
            item[item.index("OK")] = "AC"
        if "COMPILATION_ERROR" in item:
            item[item.index("COMPILATION_ERROR")] = "CE"
        if "RUNTIME_ERROR" in item:
            item[item.index("RUNTIME_ERROR")] = "RE"

    verdictData = [item for item in verdictData if "SKIPPED" not in item]

    return verdictData


def get_language_data(handle):
    api_url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(api_url)
    json_data = response.json()
    json_data = json_data["result"]

    lang_data = [entry["programmingLanguage"] for entry in json_data]
    language_count = {}
    for language in lang_data:
        if language in language_count:
            language_count[language] += 1
        else:
            language_count[language] = 1

    # Convert the language counts to a list of lists
    langData = [["Language", "Count"]] + [
        [lang, count] for lang, count in language_count.items()
    ]

    return langData


def get_ratings_data(handle):
    api_url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(api_url)
    json_data = response.json()
    json_data = json_data["result"]

    # Extract the ratings from the JSON data, excluding None values
    ratings = [
        entry["problem"].get("rating")
        for entry in json_data
        if entry["problem"].get("rating") is not None
    ]

    # Count occurrences of each rating using Counter
    rating_count = Counter(ratings)

    # Create a list for the final output, excluding entries with None values
    ratingData = [[rating, count] for rating, count in rating_count.items()]

    ratingData = sorted(ratingData)
    ratingData = [["Rating", "Count"]] + ratingData
    return ratingData


def get_problems_data(handle):
    api_url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(api_url)
    json_data = response.json()
    json_data = json_data["result"]

    # Extract the ratings from the JSON data, excluding None values
    ratings = [
        entry["problem"].get("index")
        for entry in json_data
        if entry["problem"].get("index") is not None
    ]

    # Count occurrences of each rating using Counter
    rating_count = Counter(ratings)

    # Create a list for the final output, excluding entries with None values
    ratingData = [
        [rating, count] for rating, count in rating_count.items() if rating is not None
    ]

    merged_data = {}
    for rating, count in ratingData:
        prefix = rating.rstrip("1234567890")  # Extract the non-numeric prefix
        merged_data.setdefault(prefix, 0)
        merged_data[prefix] += count

    # Create the final output list
    final_rating_data = [[key, value] for key, value in merged_data.items()]

    # Sort the final output list
    final_rating_data = sorted(final_rating_data)
    final_rating_data = [["Problem", "Count"]] + final_rating_data

    return final_rating_data


@app.route("/", methods=["GET", "POST"])
def index():
    langData = []
    if request.method == "POST":
        # Get username and number of predictions from the form
        username = request.form["username"]
        num_predictions = 5

        # Get user ratings from Codeforces API
        user_ratings = get_user_ratings(username)
        user_ranks = get_user_ranks(username)
        langData = get_language_data(username)
        verdictData = get_submission_data(username)
        ratingData = get_ratings_data(username)
        problemData = get_problems_data(username)

        if True:
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
            all_ratings = [int(x) for x in all_ratings]
            return render_template(
                "index.html",
                all_ratings=all_ratings,
                user_ranks=user_ranks,
                langData=langData,
                verdictData=verdictData,
                ratingData=ratingData,
                problemData=problemData,
            )

    # Render the template without data if it's a GET request
    return render_template(
        "index.html",
        all_ratings=[],
    )


if __name__ == "__main__":
    app.run(debug=True)
