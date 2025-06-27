# Kivy Global Info Dashboard

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

A modern desktop application built with Python and Kivy that displays live weather data and top news headlines from around the world. The app features a dynamic world clock and an autocomplete search for cities.

## Features

-   **Live Weather Data:** Fetches current weather, temperature, conditions, and a descriptive icon for any city, powered by the OpenWeatherMap API.
-   **Top News Headlines:** Displays the latest top news headlines relevant to the selected location, powered by the NewsAPI.org.
-   **Dynamic World Clock:** A real-time clock that automatically adjusts to the timezone of the searched city, complete with AM/PM format.
-   **Autocomplete Search:** Start typing a city name, and a list of suggestions will appear in real-time, powered by the Geopy library.
-   **Modern & Responsive UI:** Built with a dark theme, smooth animations for loading, and an interactive interface that fetches data in the background without freezing.

## Prerequisites

To run this application, you will need personal API keys from the following free services:

-   **OpenWeatherMap:** For weather data. Get your key at [openweathermap.org/api](https://openweathermap.org/api).
-   **NewsAPI.org:** For news headlines. Get your key at [newsapi.org](https://newsapi.org/).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/kivy-info-dashboard.git](https://github.com/YOUR_USERNAME/kivy-info-dashboard.git)
    cd kivy-info-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Add Your API Keys:**
    Open the `main.py` file and insert your personal API keys into the designated variables at the top of the script:
    ```python
    OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY_HERE"
    NEWSAPI_API_KEY = "YOUR_NEWSAPI_API_KEY_HERE"
    ```

## Usage

Run the application from your activated virtual environment:
```bash
python main.py
```
The application will launch, displaying initial data for Jakarta. Start typing in the search box to find information for other cities.

---
*Created by M Mishbahul M*
