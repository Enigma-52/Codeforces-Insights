# Codeforces Insights

Codeforces Insights is a web application built using Flask that provides visualizations and insights into a Codeforces user's performance. It utilizes various Codeforces API endpoints to gather data on a user's ratings, submissions, blog entries, and more. The data is then visualized through interactive charts and graphs.

## Live Website

The application is live at [Codeforces Insights](https://cf-insights.onrender.com). Feel free to visit and explore the insights it provides.

## Getting Started

To deploy Codeforces Insights locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/codeforces-insights.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask application:**

    ```bash
    python app.py
    ```

    The application will be accessible at `http://127.0.0.1:5000/` in your web browser.

## Features

### 1. Rating Prediction

- Predicts the Codeforces user's ratings using the Prophet forecasting model.
- Provides a visual representation of the predicted ratings over time.

### 2. Submission Analysis

- Visualizes the distribution of verdicts (e.g., AC, TLE, WA) for the user's submissions.
- Displays a pie chart showcasing the user's preferred programming languages.

### 3. Problem Analysis

- Illustrates the distribution of problems solved based on their difficulty levels.
- Presents a donut chart indicating the user's engagement with various problem tags.

### 4. User Statistics

- Highlights key statistics such as total problems tried, problems solved, accuracy, and more.
- Provides contest-related statistics, including the number of contests participated in and best/worst ranks.

### 5. Blog Entries

- Lists the latest blog entries of the Codeforces user.
- Allows users to view more entries with a "Show More/Less" button.

### 6. Submissions Calendar

- Displays a calendar heatmap showing the user's submission activity over time.
- Allows users to specify the maximum number of submissions to display.

## Screenshots

![BE45A4C2-AD92-4933-ACE9-32447FE79A92](https://github.com/Enigma-52/Codeforces-Insights/assets/95529619/e5b6cc5a-a4c2-49da-90ef-3d983d8f98d4)

![477775AD-2C63-4396-8A69-F65754B62396](https://github.com/Enigma-52/Codeforces-Insights/assets/95529619/ca180c11-b0ec-4e74-9ee8-c912f3973838)


## Technologies Used

- **Flask:** Web framework for building the application.
- **Pandas:** Data manipulation library for handling and processing data.
- **Prophet:** Time series forecasting library for predicting ratings.
- **Plotly:** Interactive plotting library for creating charts and graphs.
- **Chart.js:** JavaScript charting library for creating dynamic charts.
- **HTML/CSS:** Front-end technologies for structuring and styling the user interface.

## Contributing

If you'd like to contribute to Codeforces Insights, please follow these guidelines:

1. Fork the repository on GitHub.
2. Clone your forked repository locally.
3. Create a new branch for your changes: `git checkout -b feature-new-feature`.
4. Make your modifications and commit: `git commit -am 'Add new feature'`.
5. Push the changes to your fork: `git push origin feature-new-feature`.
6. Open a pull request on the original repository.

## Acknowledgments

- Codeforces API for providing the data used in this project.
- The open-source community for developing and maintaining the libraries and tools used in this project.


