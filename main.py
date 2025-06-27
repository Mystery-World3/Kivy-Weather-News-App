import os
import json
import requests
from datetime import datetime, timezone, timedelta 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
import threading
import webbrowser

KV_STRING = """
#:set background_color (0.1, 0.1, 0.12, 1)
#:set card_color (0.18, 0.18, 0.2, 1)
#:set text_color (0.95, 0.95, 0.95, 1)
#:set primary_color (0.12, 0.59, 0.95, 1)

<ArticlePopup>:
    orientation: 'vertical'
    padding: 15
    spacing: 10
    canvas.before:
        Color:
            rgba: background_color
        Rectangle:
            pos: self.pos
            size: self.size
            
    AsyncImage:
        id: article_image
        source: root.image_url or ''
        size_hint_y: 0.4
        fit_mode: 'contain'
        
    Label:
        id: article_title
        text: root.title
        font_size: '20sp'
        bold: True
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
        
    Label:
        id: article_meta
        text: f"{root.source} - {root.published_at}"
        font_size: '14sp'
        color: (0.7, 0.7, 0.7, 1)
        size_hint_y: None
        height: self.texture_size[1]
        
    ScrollView:
        Label:
            id: article_description
            text: root.description
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
    
    Button:
        text: "Read Full Story"
        size_hint_y: None
        height: 50
        background_color: primary_color
        on_release: app.open_link(root.url)

<WeatherNewsLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: background_color
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10
        Label:
            id: clock_label
            text: "00:00:00"
            font_size: '28sp'
            bold: True
        TextInput:
            id: city_input
            hint_text: 'Enter City Name (e.g., London)'
            font_size: '18sp'
            multiline: False
            padding: 10
        Button:
            id: search_button
            text: 'Search'
            size_hint_x: 0.3
            font_size: '18sp'
            background_color: primary_color
            on_press: app.fetch_data()

    FloatLayout:
        GridLayout:
            id: content_grid
            cols: 2
            spacing: 20
            padding: 10
            opacity: 1

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.4
                Label:
                    text: "Current Weather"
                    font_size: '22sp'
                    bold: True
                    size_hint_y: None
                    height: 40
                AsyncImage:
                    id: weather_icon
                    source: ''
                Label:
                    id: weather_location
                    text: "City, Country"
                    font_size: '20sp'
                Label:
                    id: weather_temp
                    text: "-°C"
                    font_size: '32sp'
                    bold: True
                Label:
                    id: weather_desc
                    text: "Condition"
                    font_size: '18sp'
            
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: "Top Headlines (Tech)"
                    font_size: '22sp'
                    bold: True
                    size_hint_y: None
                    height: 40
                ScrollView:
                    GridLayout:
                        id: news_list
                        cols: 1
                        spacing: 10
                        size_hint_y: None
                        height: self.minimum_height

        Label:
            id: loading_icon
            text: "⚙"
            font_name: 'seguiemj.ttf'
            font_size: '80sp'
            size_hint: None, None
            size: self.texture_size
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            opacity: 0
            canvas.before:
                PushMatrix
                Rotate:
                    angle: root.loading_angle
                    origin: self.center
            canvas.after:
                PopMatrix

<NewsListItem>:
    background_color: (0,0,0,0)
    background_normal: ''
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1] + dp(10)
    padding: 10, 10
    markup: True
    halign: 'left'
    valign: 'top'
    on_release: app.show_news_popup(self.article_data)
"""


Builder.load_string(KV_STRING)

class WeatherNewsLayout(BoxLayout):
    loading_angle = NumericProperty(0)

class NewsListItem(Button):
    article_data = ObjectProperty(None)

class ArticlePopup(BoxLayout):
    title = StringProperty('')
    source = StringProperty('')
    published_at = StringProperty('')
    description = StringProperty('')
    image_url = StringProperty('')
    url = StringProperty('')

class WeatherNewsApp(App):
    OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
    NEWSAPI_API_KEY = "YOUR_NEWSAPI_API_KEY"
    
    active_timezone_offset = NumericProperty(None)

    def build(self):
        self.title = "Global Info Dashboard v2.0"
        return WeatherNewsLayout()

    def on_start(self):
        """Memulai jam digital dan mengambil data awal."""
        Clock.schedule_interval(self.update_clock, 1)
        self.root.ids.city_input.text = "Jakarta"
        self.fetch_data()

    def update_clock(self, *args):
        """Memperbarui label jam setiap detik berdasarkan zona waktu aktif."""
        if self.active_timezone_offset is None:
            self.root.ids.clock_label.text = datetime.now().strftime("%I:%M:%S %p")
            return

        utc_now = datetime.now(timezone.utc)
        city_offset = timedelta(seconds=self.active_timezone_offset)
        city_time = utc_now + city_offset
        self.root.ids.clock_label.text = city_time.strftime("%I:%M:%S %p")

    def fetch_data(self):
        search_button = self.root.ids.search_button
        loading_icon = self.root.ids.loading_icon
        content_grid = self.root.ids.content_grid
        Animation(opacity=0, duration=0.2).start(content_grid)
        loading_icon.opacity = 1
        anim = Animation(loading_angle = -360, duration=1)
        anim.repeat = True
        anim.start(self.root)
        search_button.disabled = True
        search_button.text = "Searching..."
        threading.Thread(target=self.get_data_thread).start()

    def get_data_thread(self):
        city = self.root.ids.city_input.text
        if not city:
            Clock.schedule_once(lambda dt: self.update_ui_error("City name cannot be empty."))
            return
        weather_data = self._get_weather(city)
        news_data = self._get_news('technology')
        Clock.schedule_once(lambda dt: self.update_ui(weather_data, news_data))

    def update_ui(self, weather_data, news_data):
        Animation.cancel_all(self.root)
        self.root.loading_angle = 0
        self.root.ids.loading_icon.opacity = 0

        if isinstance(weather_data, dict):
            self.active_timezone_offset = weather_data.get('timezone_offset')
            self.update_clock() 

            self.root.ids.weather_location.text = f"{weather_data['city']}, {weather_data['country']}"
            self.root.ids.weather_temp.text = f"{weather_data['temp']:.1f}°C"
            self.root.ids.weather_desc.text = weather_data['description']
            icon_code = weather_data['icon']
            self.root.ids.weather_icon.source = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        else:
            self.update_ui_error("Could not fetch weather data.")

        news_list_widget = self.root.ids.news_list
        news_list_widget.clear_widgets()
        if isinstance(news_data, list) and news_data:
            for article in news_data:
                item = NewsListItem(text=f"[b]{article['source']}[/b]\n{article['title']}", article_data=article)
                news_list_widget.add_widget(item)
        else:
             news_list_widget.add_widget(NewsListItem(text="Could not fetch news data."))
        
        Animation(opacity=1, duration=0.5).start(self.root.ids.content_grid)

        self.root.ids.search_button.disabled = False
        self.root.ids.search_button.text = "Search"

    def open_link(self, url):
        if url: webbrowser.open(url)

    def show_news_popup(self, article_data):
        try:
            date_obj = datetime.fromisoformat(article_data['publishedAt'].replace("Z", "+00:00"))
            formatted_date = date_obj.strftime('%d %B %Y, %H:%M')
        except:
            formatted_date = "N/A"
        content = ArticlePopup(
            title=article_data['title'], source=article_data['source'],
            published_at=formatted_date, description=article_data['description'] or "No description available.",
            image_url=article_data['urlToImage'] or '', url=article_data['url']
        )
        self.popup = Popup(title="Article Details", content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def update_ui_error(self, error_message):
        self.root.ids.weather_location.text = error_message
        search_button = self.root.ids.search_button
        search_button.disabled = False
        search_button.text = "Search"
        Animation.cancel_all(self.root)
        self.root.loading_angle = 0
        self.root.ids.loading_icon.opacity = 0
        self.root.ids.content_grid.opacity = 1

    def _get_weather(self, city):
        """Metode ini sekarang juga mengambil 'timezone'."""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': self.OPENWEATHER_API_KEY, 'units': 'metric', 'lang': 'en'}
        try:
            response = requests.get(base_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data['name'], "country": data['sys']['country'],
                    "temp": data['main']['temp'], "description": data['weather'][0]['description'].capitalize(),
                    "icon": data['weather'][0]['icon'],
                    "timezone_offset": data['timezone'] 
                }
            return None
        except requests.exceptions.RequestException:
            return None

    def _get_news(self, topic):
        base_url = "https://newsapi.org/v2/everything"
        params = {'q': topic, 'language': 'en', 'pageSize': 10, 'sortBy': 'publishedAt'}
        headers = {'X-Api-Key': self.NEWSAPI_API_KEY}
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [{"source": a.get('source', {}).get('name', 'N/A'), "title": a.get('title'), "url": a.get('url'), "description": a.get('description'), "urlToImage": a.get('urlToImage'), "publishedAt": a.get('publishedAt')} for a in data.get('articles', [])]
            return None
        except requests.exceptions.RequestException:
            return None

if __name__ == '__main__':
    WeatherNewsApp().run()