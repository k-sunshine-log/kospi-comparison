# KOSPI Comparison

[한국어 버전 (Korean Version)](README.md)

This is a project that compares and visualizes the current KOSPI index with the KOSPI index during the "Three Lows" boom of the 1980s (June 1983 ~ December 1987).

Through daily automatically updated charts, you can compare past market trends with current index movements.

👉 **Check Real-time Chart**:
- [Korean Version](https://k-sunshine-log.github.io/kospi-comparison/)
- [English Version](https://k-sunshine-log.github.io/kospi-comparison/index_en.html)

## Features

*   **Automated Data Collection**: Retrieves KOSPI index data in real-time using the `FinanceDataReader` library.
*   **Index Comparison Analysis**:
    *   **Data Scaling**: Converts the 1980s index data to the current index level. (Based on the 5-day moving average at the starting point)
    *   **Time Shift**: Maps data from the past boom period to the current time to compare patterns. (Current time scale ratio: 0.88)
*   **Visualization**:
    *   Generates dark mode style charts using `Matplotlib`.
    *   Supports both Korean and English charts.
*   **Automated Deployment (CI/CD)**:
    *   The script runs every weekday at 4 PM (KST) via GitHub Actions.
    *   The generated charts are automatically deployed to GitHub Pages along with `index.html` and `index_en.html`.

## Requirements

*   Python 3.9+
*   `finance-datareader`
*   `pandas`
*   `matplotlib`

## Installation & Usage

1.  **Clone the repository**

    ```bash
    git clone https://github.com/k-sunshine-log/kospi-comparison.git
    cd kospi-comparison
    ```

2.  **Set up a virtual environment (Optional)**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate  # Windows
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the script**

    ```bash
    python main.py
    ```
    After execution, the chart images will be generated.

## Structure

*   `main.py`: The main script responsible for data collection, processing, and chart generation.
*   `index.html` / `index_en.html`: HTML files to display the generated chart images on a web page.
*   `.github/workflows/deploy.yml`: GitHub Actions workflow configuration file. (Daily automatic execution and deployment)
*   `requirements.txt`: List of Python packages required to run the project.

## Automation

This project uses GitHub Actions to perform the following tasks:

1.  **Scheduling**: Runs every weekday at 07:00 UTC (16:00 KST).
2.  **Environment Setup**: Installs Python 3.9 on an Ubuntu environment.
3.  **Chart Generation**: Runs `main.py` to generate chart images reflecting the latest data.
4.  **Deployment**: Pushes the generated images and HTML files to the `gh-pages` branch, updating GitHub Pages.

---
**Note**: This project is for reference purposes to compare past market patterns with the present and does not constitute advice for actual investments.
