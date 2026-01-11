from abc import ABC, abstractmethod
#  Subject (Observable) 
class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


#  Observer Interface 
class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity, pressure):
        pass


#  Concrete Subject 
class WeatherStation(Subject):

    def __init__(self):
        self._observers = []
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0

    def register_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(
                self._temperature,
                self._humidity,
                self._pressure
            )

    def set_measurements(self, temperature, humidity, pressure):
        print(f"\n{'='*60}")
        print("Weather Station: New measurements")
        print(f"{'='*60}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")

        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure

        self.notify_observers()
        
    # Getters for observers that want to pull data
    def get_temperature(self):
        return self._temperature
    
    def get_humidity(self):
        return self._humidity
    
    def get_pressure(self):
        return self._pressure

#  Concrete Observers 
class PhoneDisplay(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, temperature, humidity, pressure):
        print(f"\n{self.name} Phone Display")
        print(f"Temp: {temperature}°C, Humidity: {humidity}%")


class TVDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print("\nTV Display")
        print(f"Temp: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")


class WindowDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print("\nWindow Display")
        print(f"Temp: {temperature}°C | Humidity: {humidity}%")


class WebsiteDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print("\nWebsite Display")
        print(f"{temperature}°C, {humidity}% humidity")


class StatisticsDisplay(Observer):
    def __init__(self):
        self.temps = []

    def update(self, temperature, humidity, pressure):
        self.temps.append(temperature)
        avg_temp = sum(self.temps) / len(self.temps)

        print("\nStatistics Display")
        print(f"Avg: {avg_temp:.1f}°C, Max: {max(self.temps)}°C, Min: {min(self.temps)}°C")


class AlertSystem(Observer):
    def update(self, temperature, humidity, pressure):
        print("\nAlert System")

        if temperature > 35:
            print("High temperature warning")
        if humidity > 90:
            print("High humidity warning")
        if pressure < 1000:
            print("Low pressure warning")
        if temperature <= 35 and humidity <= 90 and pressure >= 1000:
            print("All conditions normal")


#  Usage 
weather_station = WeatherStation()

weather_station.register_observer(PhoneDisplay("iPhone"))
weather_station.register_observer(TVDisplay())
weather_station.register_observer(WindowDisplay())
weather_station.register_observer(StatisticsDisplay())
weather_station.register_observer(AlertSystem())

weather_station.set_measurements(25, 65, 1013)
weather_station.set_measurements(28, 70, 1012)

# Dynamically add new observer at runtime!
weather_station.register_observer(WebsiteDisplay())
weather_station.set_measurements(32, 75, 1010)

# Remove an observer at runtime
weather_station.remove_observer(WindowDisplay())
weather_station.set_measurements(36, 85, 998)
