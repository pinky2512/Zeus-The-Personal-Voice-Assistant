import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import pvporcupine
from pvrecorder import PvRecorder
import openai
import os
import datetime
import requests
from AppOpener import open, close
from PIL import Image, ImageTk

# Initialize recognizer and engine objects
r = sr.Recognizer()
engine = pyttsx3.init()

openai.api_key = os.environ.get("OPENAI")

def get_ai_response(input_text):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": input_text}
      ]
    )
    return completion.choices[0].message.content

# Function to speak the text
def speak(app, text):
    app.change_image('speaking.png')
    engine.say(text)
    engine.runAndWait()
    app.change_image('listening.png')

# Function to display text and speak the text
def display_and_speak(app, text):
    app.display_message("Zeus: " + text, style="answer")
    speak(app, text)

def open_apps(app, name):
    display_and_speak(app, "Opening " + name)
    open(name)
    display_and_speak(app, "Opened " + name)
    
    
# Start the assistant
def start(app):
    app.display_message("Zeus: Hello! How can I help you", style="answer")
    engine.say("Hello! How can I help you")
    engine.runAndWait()
    while True:
        try:
            # Listen for user commands
            with sr.Microphone() as source:
                speak(app, "Listening")
                audio = r.listen(source)

            # Convert voice commands to text
            command = r.recognize_google(audio)
            app.display_message(f"You: {command}", style="question")

            # Execute the command
            if "exit" in command or "bye" in command:
                display_and_speak(app,"Goodbye!")
                app.quit()
            elif "open" in command and "steps" not in command:
                if "vscode" in command.lower() or "visual studio code" in command.lower():
                    open_apps(app,"Visual Studio Code")
                elif "chrome" in command.lower():
                    open_apps(app,"Google Chrome")
                elif "jupyter-notebook" in command.lower() or "jupyter notebook" in command.lower() or "jupiter notebook" in command.lower():
                    open_apps(app, "Jupyter Notebook")
                elif "notepad" in command.lower():
                    open_apps(app, 'Notepad')
                elif "edge" in command.lower():
                    open_apps(app, "Microsoft Edge")
                elif "excel" in command.lower():
                    open_apps(app, "Excel")
                elif "powerpoint" in  command.lower():
                    open_apps(app, "Powerpoint")
                elif "word" in command.lower():
                    open_apps(app, "Word")
                elif "settings" in command.lower():
                    open_apps(app, "Settings")
                elif "terminal" in command.lower() or "power shell" in command.lower() or ("power" in command.lower() and "shell" in command.lower()):
                    open_apps(app, "Terminal")
                elif "command prompt" in command.lower():
                    open_apps(app, "Command Prompt")
                elif "control panel" in command.lower():
                    open_apps(app, "Control Panel")
                elif "files" in command.lower():
                    open_apps(app, "File Explorer")
                elif "whatsapp" in command.lower():
                    open_apps(app, "WhatsApp")
                elif "calculator" in command.lower():
                    open_apps(app, "Calculator")
                elif "calendar" in command.lower():
                    open_apps(app, "Calendar")
                elif "clock" in command.lower():
                    open_apps(app, "Clock")
                elif "discord" in command.lower():
                    open_apps(app, "Discord")
                elif "gmail" in command.lower():
                    open_apps(app, "Gmail")
                elif "drive" in command.lower() or "google drive" in command.lower():
                    open_apps(app, "Google Drive")
                elif "instagram" in command.lower():
                    open_apps(app, "Instagram")
                elif "maps" in command.lower():
                    open_apps(app, "Maps")
                elif "ms office" in command.lower() or "microsoft office" in command.lower():
                    open_apps(app, "Microsoft Office")
                elif "store" in command.lower() or "ms store" in command.lower() or "microsoft store" in command.lower():
                    open_apps(app, "Microsoft Store")
                elif "whiteboard" in command.lower() or "microsoft whiteboard" in command.lower():
                    open_apps(app, "Microsoft Whiteboard")
                elif "paint" in command.lower():
                    open_apps(app, "Paint")
                elif "photos" in command.lower():
                    open_apps(app, "Photos")
                elif "quick assist" in command.lower():
                    open_apps(app, "Quick Assist")
                elif "system information" in command.lower():
                    open_apps(app, "System Information")
                elif "task manager" in command.lower():
                    open_apps(app, "Task Manager")
                elif "youtube" in command.lower():
                    open_apps(app, "Youtube")
            elif "who" in command and "you" in command:
                display_and_speak(app, "I'm Zeus, your personal assistant.")
            elif "date" in command and "time" in command:
                date_time_response = get_current_date_time()
                display_and_speak(app, f"Now the date and time are {date_time_response}")
            elif "date" in command:
                date_response = get_current_date_time().date()
                display_and_speak(app, f"Today's Date is {date_response}")
            elif "time" in command:
                time_response = get_current_date_time().time()
                display_and_speak(app, f"Now the time is {time_response}")
            elif "where" in command and ("i" in command or "I" in command):
                l = get_location()
                city = l["city"]
                region = l["region"]
                country_name = l["country"]
                display_and_speak(app, f"You are in {city}, {region}, {country_name}")
            elif "weather" in command:
                d = get_weather()
                city = d["city"]
                region = d["region"]
                country_name = d["country_name"]
                desc = d["description"]
                temp = d["temperature"]
                hum = d["humidity"]
                display_and_speak(app, f"The weather in {city}, {region}, {country_name} is {desc}. The temperature is {temp}. The humidity is {hum}")
            elif "news" in command:
                news = get_news()
                for idx, article in enumerate(news, start=1):
                    app.display_message("Zeus:", style="answer")
                    app.display_message(f"Article {idx}:",style="answer")
                    app.display_message(f"Title: {article['title']}", style="answer")
                    app.display_message(f"Source: {article['source']}", style="answer")
                    app.display_message(f"URL: {article['url']}", style="answer")
                    speak(app, f"Article {idx}:")
                    speak(app, f"Title: {article['title']}")
                    speak(app, f"Source: {article['source']}")
            else:
                ai_response = get_ai_response(command)
                display_and_speak(app, ai_response)

        except sr.UnknownValueError:
            display_and_speak(app, "I'm sorry, I didn't catch that.")
        except sr.RequestError:
            display_and_speak(app, "Sorry, could not connect to the internet. Please try again later.")

def get_current_date_time():
    current_date_time = datetime.datetime.now()
    return current_date_time

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def get_weather():
    base_url = "https://api.openweathermap.org/data/2.5/weather?"

    api_key = os.environ.get("WEATHERAPI")
    
    l = get_location()
    
    city_name = l["city"]
    
    query_params = f"q={city_name}"
    
    # Add your API key to the query parameters
    query_params += f"&appid={api_key}"

    # Send a GET request to the OpenWeatherMap API
    response = requests.get(base_url + query_params)

    # Parse the JSON response
    data = response.json()
    # Extract the relevant weather information
    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    return {
        "city": l["city"],
        "region": l["region"],
        "country_name": l["country"],
        "description": weather_description,
        "temperature": temperature,
        "humidity": humidity
    }

def get_news():
    # Define the base URL for the News API
    base_url = "https://newsapi.org/v2/everything"

    api_key = os.environ.get("NEWSAPI")

    location = get_location()["city"]

    # Specify the parameters for the API request
    params = {
        "apiKey": api_key,
        "q": "news",  # You can specify keywords for specific types of news
        "sortBy": "publishedAt",
        "language": "en",  # Language of the news articles (English in this example)
        "pageSize": 3,  # Number of articles to retrieve
        "location": location  # The location parameter (e.g., "New York")
    }

    news_data = []

    try:
        # Send the API request
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            # Create a list of news articles
            for article in articles:
                news_article = {
                    "title": article['title'],
                    "source": article['source']['name'],
                    "url": article['url']
                }
                news_data.append(news_article)
        else:
            print("Error fetching news:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

    return news_data

def wake_word(app):
    pico_access_key = os.environ.get("PICOVOICE")
    porcupine = pvporcupine.create(access_key=pico_access_key,keyword_paths=['hey_zeus.ppn','hi_zeus.ppn'])
    recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

    try:
        recoder.start()
        while True:
            keyword_index = porcupine.process(recoder.read())
            if keyword_index >= 0:
                app.change_image('wake.png')
                start(app)
                recoder.stop()
                break
    except KeyboardInterrupt:
        recoder.stop()
    finally:
        porcupine.delete()
        recoder.delete()

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root        
        self.root.title("Zeus")
        self.root.configure(bg="#FFFFFF")

        # Load initial image
        self.current_image_path = "sleeping.png"  # Change this to the path of your image
        self.load_image()

        self.root.configure(bg="#000000")

        # Create a label for displaying the image
        self.image_label = tk.Label(root, image=self.tk_image, background="#000000")
        self.image_label.pack(pady=20)

        # Create a text box to display messages
        self.text_box = tk.Text(root, height=20, width=100, background="#000000")
        self.text_box.pack(padx=10,pady=20)
    
        # Configure the style of the text in the text box
        self.text_box.tag_configure("question", font=("Sans Serif", 14, "bold"), foreground="#FF0000")
        self.text_box.tag_configure("answer", font=("Sans Serif", 14, "bold"), foreground="#FFD700")

        # Bind the window closing event to the quit method
        self.root.protocol("WM_DELETE_WINDOW", self.quit)


    def load_image(self):
        # Open and resize the image to fit the label
        image = Image.open(self.current_image_path)
        image = image.resize((300, 300), Image.ANTIALIAS)  # Adjust the size as needed

        # Convert the image to a Tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(image)

    def display_message(self, message, style=None):
        if style:
            self.text_box.insert(tk.END, message + "\n", style)
        else:
            self.text_box.insert(tk.END, message + "\n")
        self.text_box.see(tk.END)

    def change_image(self, new_image_path):
        self.current_image_path = new_image_path
        self.load_image()
        self.image_label.configure(image=self.tk_image)

    def quit(self):
        self.root.destroy()

# Function to handle window closing event
def on_closing(root):
    # Clean up any resources if needed
    root.destroy()
    exit()

def main():
    root = tk.Tk()
    app = ImageDisplayApp(root)

    # Create a thread for the voice assistant and pass the app object
    assistant_thread = threading.Thread(target=wake_word, args=(app,))

    # Start the assistant thread
    assistant_thread.start()
    
    # Set a function to handle window closing event
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()

if __name__ == "__main__":
    main()