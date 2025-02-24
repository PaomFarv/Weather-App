import requests
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WeatherApp():
    def __init__(self):
        app = ctk.CTk()
        app.title("Minimal Weather App")
        app.geometry("500x600")

        frame_4_text = ctk.CTkFrame(master=app,fg_color="#1F6AA5",height=30)
        frame_4_text.pack(fill="x",pady=10,padx=10)

        header = ctk.CTkLabel(master=frame_4_text,text="WeatherNow",font=("Impact",60))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(master=app,border_width=1)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.user_input = ctk.CTkEntry(master=main_frame,placeholder_text="City Name",width=400,height=30,font=("Helvetica",18),text_color="white")
        self.user_input.pack(pady=30)

        self.req_weather_button = ctk.CTkButton(master=main_frame,text="Request Weather",width=100,font=("Helvetica",15,"bold"),command=self.get_weather)
        self.req_weather_button.pack()

        self.weather_info = ctk.CTkLabel(master=main_frame,text="",font=("Helvetica",18,"bold"))
        self.weather_info.pack(pady=20)

        self.exmp_icon = ctk.CTkLabel(master=main_frame,text="")
        self.exmp_icon.pack(pady=50)

        app.mainloop()

    def get_weather(self):
        city_name = self.user_input.get().strip().capitalize()
        url = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=81583a9fe50fae0a55c6d33d0d139bf6")
        response = url.json()

        
        temp = response['main']['temp']
        feels_like = response['main']['feels_like']
        desc = response['weather'][0]['description']
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']

        self.weather_info.configure(text=f"Temperature : {temp-273.15:.2f}°C  |  Feels Like    : {feels_like-273.15:.2f}°C\nHumidity : {humidity}     |    Pressure    : {pressure/1013.25:.2f} atm\nDesc.   : {desc.capitalize()}")

        condition_id = response['weather'][0]['id']
        print(condition_id)
        if 200 <= int(condition_id) <= 232:
            png = ctk.CTkImage(light_image=Image.open("thunder.png"),dark_image=Image.open("thunder.png"),size=(150,150))
            self.exmp_icon.configure(image=png)

        elif 500 <= int(condition_id) <= 531:
            png = ctk.CTkImage(light_image=Image.open("rain.png"),dark_image=Image.open("rain.png"),size=(150,150))
            self.exmp_icon.configure(image=png)

if __name__ == "__main__":
    WeatherApp()