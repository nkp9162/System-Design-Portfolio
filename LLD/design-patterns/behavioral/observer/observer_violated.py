class WeatherStation:

    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        # Direct references to displays (tight coupling)
        # Subject knows about all observers
        self.phone_display = None
        self.tv_display = None
        self.window_display = None

    def register_displays(self, phone, tv, window):
        self.phone_display = phone
        self.tv_display = tv
        self.window_display = window
    
    #  Updates weather data and manually notifies each display.
    def set_measurements(self, temperature, humidity, pressure):
        print(f"\n{'='*60}")
        print("Weather Station: New measurements received")
        print(f"{'='*60}")

        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

        if self.phone_display:
            self.phone_display.update(temperature, humidity, pressure)

        if self.tv_display:
            self.tv_display.update(temperature, humidity, pressure)

        if self.window_display:
            self.window_display.update(temperature, humidity, pressure)


class PhoneDisplay:
    def update(self, temperature, humidity, pressure):
        print("\nPhone Display Updated:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")


class TVDisplay:
    def update(self, temperature, humidity, pressure):
        print("\nTV Display Updated:")
        print(f"Temp: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")


class WindowDisplay:
    def update(self, temperature, humidity, pressure):
        print("\nWindow Display Updated:")
        print(f"Temperature: {temperature}°C | Humidity: {humidity}%")


print("="*60)
print("WEATHER MONITORING SYSTEM - WITHOUT OBSERVER PATTERN")
print("="*60)

phone = PhoneDisplay()
tv = TVDisplay()
window = WindowDisplay()

weather_station = WeatherStation()
weather_station.register_displays(phone, tv, window)

weather_station.set_measurements(25, 65, 1013)
weather_station.set_measurements(28, 70, 1012)


print("\n" + "="*60)
print("TRYING TO ADD NEW DISPLAY")
print("="*60)


class WebsiteDisplay:
    def update(self, temperature, humidity, pressure):
        print("\nWebsite Display Updated:")
        print(f"Current Weather: {temperature}°C, {humidity}% humidity")


website = WebsiteDisplay()
print("ERROR: Cannot add website display without modifying WeatherStation")
print("Must change set_measurements() method")
print("Must add new display reference inside WeatherStation")
