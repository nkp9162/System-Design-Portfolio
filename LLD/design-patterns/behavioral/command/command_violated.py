# RECEIVERS

class Light:

    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light turned ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light turned OFF")


class Fan:
    
    def __init__(self, location):
        self.location = location
        self.speed = 0  # 0 = off, 1-5 = speed
    
    def turn_on(self, speed=3):
        self.speed = speed
        print(f"{self.location} fan ON at speed {speed}")
    
    def turn_off(self):
        self.speed = 0
        print(f"{self.location} fan OFF")
    
    def increase_speed(self):
        if self.speed < 5:
            self.speed += 1
            print(f"{self.location} fan speed increased to {self.speed}")
        else:
            print(f"{self.location} fan already at max speed")
    
    def decrease_speed(self):
        if self.speed > 0:
            self.speed -= 1
            print(f"{self.location} fan speed decreased to {self.speed}")
        else:
            print(f"{self.location} fan already OFF")


class AirConditioner:
    
    def __init__(self, location):
        self.location = location
        self.is_on = False
        self.temperature = 24
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} AC ON at {self.temperature}C")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} AC OFF")
    
    def set_temperature(self, temp):
        old_temp = self.temperature
        self.temperature = temp
        if self.is_on:
            print(f"{self.location} AC temperature changed {old_temp}C -> {temp}C")
        else:
            print(f"{self.location} AC temperature preset to {temp}C (AC OFF)")


class Television:
    
    def __init__(self, location):
        self.location = location
        self.is_on = False
        self.volume = 10
        self.channel = 1
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} TV ON (Channel {self.channel}, Volume {self.volume})")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} TV OFF")
    
    def set_volume(self, volume):
        old_volume = self.volume
        self.volume = volume
        print(f"{self.location} TV volume {old_volume} -> {volume}")
    
    def set_channel(self, channel):
        old_channel = self.channel
        self.channel = channel
        print(f"{self.location} TV channel {old_channel} -> {channel}")


# INVOKER - Remote Control (tightly coupled)

class RemoteControl:
    
    def __init__(self):
        self.devices = {}
        self.last_operation = None
    
    def add_device(self, name, device):
        self.devices[name] = device
    
    def execute_operation(self, device_name, operation, *args):
        if device_name not in self.devices:
            print(f"Device '{device_name}' not found")
            return
        
        device = self.devices[device_name]
        
        if isinstance(device, Light):
            if operation == "on":
                device.turn_on()
                self.last_operation = (device_name, "off")
            elif operation == "off":
                device.turn_off()
                self.last_operation = (device_name, "on")
            else:
                print("Invalid operation for Light")
        
        elif isinstance(device, Fan):
            if operation == "on":
                speed = args[0] if args else 3
                device.turn_on(speed)
                self.last_operation = (device_name, "off")
            elif operation == "off":
                device.turn_off()
                self.last_operation = (device_name, "on")
            elif operation == "speed_up":
                old_speed = device.speed
                device.increase_speed()
                self.last_operation = (device_name, "speed_down", old_speed)
            elif operation == "speed_down":
                old_speed = device.speed
                device.decrease_speed()
                self.last_operation = (device_name, "speed_up", old_speed)
            else:
                print("Invalid operation for Fan")
        
        elif isinstance(device, AirConditioner):
            if operation == "on":
                device.turn_on()
                self.last_operation = (device_name, "off")
            elif operation == "off":
                device.turn_off()
                self.last_operation = (device_name, "on")
            elif operation == "set_temp":
                old_temp = device.temperature
                device.set_temperature(args[0])
                self.last_operation = (device_name, "set_temp", old_temp)
            else:
                print("Invalid operation for AC")
        
        elif isinstance(device, Television):
            if operation == "on":
                device.turn_on()
                self.last_operation = (device_name, "off")
            elif operation == "off":
                device.turn_off()
                self.last_operation = (device_name, "on")
            elif operation == "volume":
                old_volume = device.volume
                device.set_volume(args[0])
                self.last_operation = (device_name, "volume", old_volume)
            elif operation == "channel":
                old_channel = device.channel
                device.set_channel(args[0])
                self.last_operation = (device_name, "channel", old_channel)
            else:
                print("Invalid operation for TV")
        
        else:
            print("Unknown device type")
    
    def undo(self):
        if not self.last_operation:
            print("Nothing to undo")
            return
        
        print("\n[Undo] Attempting last operation")
        device_name = self.last_operation[0]
        operation = self.last_operation[1]
        args = self.last_operation[2:] if len(self.last_operation) > 2 else []
        
        self.execute_operation(device_name, operation, *args)
        self.last_operation = None


# USAGE

print("=" * 60)
print("SMART HOME REMOTE - WITHOUT COMMAND PATTERN")
print("=" * 60)

living_room_light = Light("Living Room")
bedroom_light = Light("Bedroom")
living_room_fan = Fan("Living Room")
bedroom_ac = AirConditioner("Bedroom")
living_room_tv = Television("Living Room")

remote = RemoteControl()
remote.add_device("living_light", living_room_light)
remote.add_device("bedroom_light", bedroom_light)
remote.add_device("living_fan", living_room_fan)
remote.add_device("bedroom_ac", bedroom_ac)
remote.add_device("living_tv", living_room_tv)

print("\nSCENARIO 1: Basic operations")
remote.execute_operation("living_light", "on")
remote.execute_operation("living_fan", "on", 4)
remote.execute_operation("bedroom_ac", "on")
remote.execute_operation("bedroom_ac", "set_temp", 22)

print("\nSCENARIO 2: Undo (fragile)")
remote.execute_operation("living_tv", "on")
remote.execute_operation("living_tv", "volume", 25)
remote.undo()

print("\nSCENARIO 3: Multiple operations")
remote.execute_operation("living_fan", "speed_up")
remote.execute_operation("living_fan", "speed_up")
remote.execute_operation("living_tv", "channel", 5)
