from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import requests
from prophet import Prophet
from collections import Counter
from datetime import datetime
from collections import defaultdict

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
        return []


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
        return []


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

    # Count occurrences of each rating of user using Counter
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


def get_blog_entries(handle):
    url = f"https://codeforces.com/api/user.blogEntries?handle={handle}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])
    else:
        print(f"Error: {response.status_code}")
        return []


def get_codeforces_submissions(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    data = response.json()
    data = data["result"]

    calendar_data = defaultdict(int)

    for submission in data:
        timestamp = submission["creationTimeSeconds"]
        date = datetime.utcfromtimestamp(timestamp).date()
        calendar_data[str(date)] += 1  # Convert date to string

    return calendar_data


def get_user_tags(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    response = response.json()
    result = response["result"]
    tags_count = {}

    for submission in result:
        problem = submission.get("problem", {})
        tags = problem.get("tags", [])
        for tag in tags:
            tags_count[tag] = tags_count.get(tag, 0) + 1
    tags_list = [[tag, count] for tag, count in tags_count.items()]

    return tags_list


def get_user_stats(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    response = response.json()

    unique_problem_names = set()
    successful_attempts = set()

    total_attempts = len(response["result"])

    for submission in response["result"]:
        problem_name = submission["problem"]["name"]
        unique_problem_names.add(problem_name)

        if submission["verdict"] == "OK":
            successful_attempts.add(problem_name)

    total_tried = len(unique_problem_names)
    successful_attempts_count = len(successful_attempts)
    unsolved = total_tried - successful_attempts_count
    accuracy = successful_attempts_count / total_attempts if total_attempts > 0 else 0
    total_time_spent = sum(
        submission["timeConsumedMillis"] for submission in response["result"]
    )
    total_memory_consumed = sum(
        submission["memoryConsumedBytes"] for submission in response["result"]
    )

    # Convert time to minutes
    total_time_spent_minutes = total_time_spent / (1000 * 60)

    # Convert memory to megabytes
    total_memory_consumed_mb = total_memory_consumed / (1024 * 1024 * 1024)

    result_list = [
        str(total_tried),
        str(successful_attempts_count),
        f"{accuracy * 100:.2f}%",
        str(unsolved),
        f"{total_time_spent_minutes:.2f} minutes",
        f"{total_memory_consumed_mb:.2f} GB",
    ]

    return result_list


def get_contest_stats(handle):
    api_url = f"https://codeforces.com/api/user.rating?handle={handle}"

    # Make API call and get JSON response
    response = requests.get(api_url)
    data = response.json()

    # Check if the API call was successful
    contests = data["result"]

    unique_contests = len(contests)

    # Extract other required stats
    best_rank = min(contest["rank"] for contest in contests)
    worst_rank = max(contest["rank"] for contest in contests)
    max_increase_in_rating = max(
        contest["newRating"] - contest["oldRating"] for contest in contests
    )
    max_decrease_in_rating = min(
        contest["newRating"] - contest["oldRating"] for contest in contests
    )

    # Compile the stats into a list
    result_list = [
        unique_contests,
        best_rank,
        worst_rank,
        max_increase_in_rating,
        max_decrease_in_rating,
    ]

    return result_list


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
        blog_entries = get_blog_entries(username)
        submissionData = get_codeforces_submissions(username)
        tags_list = get_user_tags(username)
        user_stats = get_user_stats(username)
        contest_stats = get_contest_stats(username)

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
                blog_entries=blog_entries,
                submissionData=submissionData,
                tags_list=tags_list,
                user_stats=user_stats,
                contest_stats=contest_stats,
            )

    # Render the template without data if it's a GET request
    return render_template(
        "index.html",
        all_ratings=[],
    )


if __name__ == "__main__":
    app.run(debug=True)
