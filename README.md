# Global Info Dashboard

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg) ![Kivy 2.3+](https://img.shields.io/badge/Kivy-2.3+-purple.svg)

A modern and responsive desktop application built with Python and Kivy that serves as a global information hub. It provides live weather data, top news headlines, and a dynamic world clock based on user-selected cities.

![Project Screenshot](https://i.imgur.com/7w8w2dZ.png) 
*(Ganti link di atas dengan link screenshot Anda sendiri setelah diunggah ke GitHub)*

## ✨ Features

-   **Live Weather Data:** Get current weather conditions, temperature, and a descriptive icon for any city, powered by the OpenWeatherMap API.
-   **Clickable Top News:** Displays the latest top news headlines. Click any headline to open a popup with a summary and a link to the full article.
-   **Dynamic World Clock:** A real-time clock that automatically adjusts to the timezone of the searched city, complete with an AM/PM format.
-   **Autocomplete City Search:** A smart search bar that provides location suggestions as you type, powered by the Geopy library.
-   **Modern & Responsive UI:** Built with a dark theme and smooth animations for a professional user experience. All network requests are handled in the background using threading to keep the UI from freezing.

## 🛠️ Prerequisites

To run this application, you will need personal API keys from the following free services:

-   **OpenWeatherMap:** For weather data. Get your key at [openweathermap.org/api](https://openweathermap.org/api).
-   **NewsAPI.org:** For news headlines. Get your key at [newsapi.org](https://newsapi.org/).

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/global-info-dashboard.git](https://github.com/YOUR_USERNAME/global-info-dashboard.git)
    cd global-info-dashboard
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
5.  **(Windows Only) Add Emoji Font:**
    To display icons correctly, copy the `seguiemj.ttf` file from `C:\Windows\Fonts` into your project directory.

## 🏃 Usage

Run the application from your activated virtual environment:
```bash
python main.py
```
The application will launch, displaying initial data for Jakarta. Start typing in the search box to find information for other cities around the world.

---
*Created by Mystery-World3*
