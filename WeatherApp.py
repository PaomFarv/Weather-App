import requests
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WeatherApp():
    def __init__(self):
        app = ctk.CTk()
        app.title("Minimal Weather App")
        app.geometry("500x620")

        frame_4_text = ctk.CTkFrame(master=app, fg_color="#1F6AA5", height=30)
        frame_4_text.pack(fill="x", pady=10, padx=10)

        header = ctk.CTkLabel(master=frame_4_text, text="WeatherNow", font=("Impact", 50))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(master=app, border_width=1)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.user_input = ctk.CTkEntry(master=main_frame, placeholder_text="City Name", width=400, height=30, font=("Helvetica", 18), text_color="white")
        self.user_input.pack(pady=30)

        self.req_weather_button = ctk.CTkButton(master=main_frame, text="Request Weather", width=120, height=40, font=("Helvetica", 15, "bold"), command=self.get_weather)
        self.req_weather_button.pack()

        self.weather_info = ctk.CTkLabel(master=main_frame, text="", font=("Helvetica", 18, "bold"))
        self.weather_info.pack(pady=20)

        self.exmp_icon = ctk.CTkLabel(master=main_frame, text="Update will appear here!")
        self.exmp_icon.pack(pady=10)

        self.weather_icons = {
            "thunder": ctk.CTkImage(light_image=Image.open("thunder.png"), dark_image=Image.open("thunder.png"), size=(200, 200)),
            "rain": ctk.CTkImage(light_image=Image.open("rain.png"), dark_image=Image.open("rain.png"), size=(200, 200)),
            "drizzle": ctk.CTkImage(light_image=Image.open("drizzle.png"), dark_image=Image.open("drizzle.png"), size=(200, 200)),
            "snow": ctk.CTkImage(light_image=Image.open("snow.png"), dark_image=Image.open("snow.png"), size=(200, 200)),
            "clearsky": ctk.CTkImage(light_image=Image.open("clearsky.png"), dark_image=Image.open("clearsky.png"), size=(200, 200)),
            "clouds": ctk.CTkImage(light_image=Image.open("clouds.png"), dark_image=Image.open("clouds.png"), size=(200, 200)),
            "badweather": ctk.CTkImage(light_image=Image.open("badweather.png"), dark_image=Image.open("badweather.png"), size=(200, 200)),
        }

        app.mainloop()

    def get_weather(self):
        city_name = self.user_input.get().strip().title()
        
        if not city_name or not city_name.replace(" ", "").isalpha():
            self.weather_info.configure(text="Please enter a valid city name.")
            self.exmp_icon.configure(text="❌")
            return

        try:
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=81583a9fe50fae0a55c6d33d0d139bf6"
            response = requests.get(url).json()
            
            if response.get("cod") != 200:
                self.weather_info.configure(text="City not found. Please try again.")
                self.exmp_icon.configure(text="❌")
                return

            temp = response['main']['temp'] - 273.15
            feels_like = response['main']['feels_like'] - 273.15
            desc = response['weather'][0]['description'].capitalize()
            humidity = response['main']['humidity']
            pressure = response['main']['pressure'] / 1013.25
            condition_id = response['weather'][0]['id']

            self.weather_info.configure(
                text=f"Temperature: {temp:.2f}°C | Feels Like: {feels_like:.2f}°C\n"
                     f"Humidity: {humidity}% | Pressure: {pressure:.2f} atm\n"
                     f"Weather Condition: {desc}"
            )

            if 200 <= condition_id <= 232:
                self.exmp_icon.configure(image=self.weather_icons["thunder"], text="")
            elif 500 <= condition_id <= 531:
                self.exmp_icon.configure(image=self.weather_icons["rain"], text="")
            elif 300 <= condition_id <= 321:
                self.exmp_icon.configure(image=self.weather_icons["drizzle"], text="")
            elif 600 <= condition_id <= 622:
                self.exmp_icon.configure(image=self.weather_icons["snow"], text="")
            elif condition_id == 800:
                self.exmp_icon.configure(image=self.weather_icons["clearsky"], text="")
            elif 801 <= condition_id <= 804:
                self.exmp_icon.configure(image=self.weather_icons["clouds"], text="")
            elif 701 <= condition_id <= 781:
                self.exmp_icon.configure(image=self.weather_icons["badweather"], text="")

        except Exception as e:
            self.weather_info.configure(text=f"Error: {str(e)}")

if __name__ == "__main__":
    WeatherApp()
