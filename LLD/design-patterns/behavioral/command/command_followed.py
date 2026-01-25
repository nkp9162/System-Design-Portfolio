from abc import ABC, abstractmethod
from typing import List

# RECEIVERS

class Light:
    
    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light OFF")


class Fan:
    
    def __init__(self, location):
        self.location = location
        self.speed = 0
    
    def turn_on(self, speed=3):
        self.speed = speed
        print(f"{self.location} fan ON (speed {speed})")
    
    def turn_off(self):
        self.speed = 0
        print(f"{self.location} fan OFF")
    
    def set_speed(self, speed):
        old_speed = self.speed
        self.speed = speed
        print(f"{self.location} fan speed {old_speed} -> {speed}")
        return old_speed


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
            print(f"{self.location} AC temperature {old_temp}C -> {temp}C")
        return old_temp


class Television:
    
    def __init__(self, location):
        self.location = location
        self.is_on = False
        self.volume = 10
        self.channel = 1
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} TV ON (Ch {self.channel}, Vol {self.volume})")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} TV OFF")
    
    def set_volume(self, volume):
        old_volume = self.volume
        self.volume = volume
        print(f"{self.location} TV volume {old_volume} -> {volume}")
        return old_volume
    
    def set_channel(self, channel):
        old_channel = self.channel
        self.channel = channel
        print(f"{self.location} TV channel {old_channel} -> {channel}")
        return old_channel


# COMMAND INTERFACE
class Command(ABC):
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


# CONCRETE COMMANDS - Light

class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()


# CONCRETE COMMANDS - Fan

class FanOnCommand(Command):
    def __init__(self, fan: Fan, speed=3):
        self.fan = fan
        self.speed = speed
        self.previous_speed = 0
    
    def execute(self):
        self.previous_speed = self.fan.speed
        self.fan.turn_on(self.speed)
    
    def undo(self):
        if self.previous_speed == 0:
            self.fan.turn_off()
        else:
            self.fan.set_speed(self.previous_speed)


class FanOffCommand(Command):
    def __init__(self, fan: Fan):
        self.fan = fan
        self.previous_speed = 0
    
    def execute(self):
        self.previous_speed = self.fan.speed
        self.fan.turn_off()
    
    def undo(self):
        self.fan.turn_on(self.previous_speed)


class FanSpeedCommand(Command):
    def __init__(self, fan: Fan, speed: int):
        self.fan = fan
        self.speed = speed
        self.previous_speed = 0
    
    def execute(self):
        self.previous_speed = self.fan.set_speed(self.speed)
    
    def undo(self):
        self.fan.set_speed(self.previous_speed)


# CONCRETE COMMANDS - Air Conditioner

class ACOnCommand(Command):
    def __init__(self, ac: AirConditioner):
        self.ac = ac
    
    def execute(self):
        self.ac.turn_on()
    
    def undo(self):
        self.ac.turn_off()


class ACOffCommand(Command):
    def __init__(self, ac: AirConditioner):
        self.ac = ac
    
    def execute(self):
        self.ac.turn_off()
    
    def undo(self):
        self.ac.turn_on()


class ACTemperatureCommand(Command):
    def __init__(self, ac: AirConditioner, temperature: int):
        self.ac = ac
        self.temperature = temperature
        self.previous_temperature = 0
    
    def execute(self):
        self.previous_temperature = self.ac.set_temperature(self.temperature)
    
    def undo(self):
        self.ac.set_temperature(self.previous_temperature)


# CONCRETE COMMANDS - Television

class TVOnCommand(Command):
    def __init__(self, tv: Television):
        self.tv = tv
    
    def execute(self):
        self.tv.turn_on()
    
    def undo(self):
        self.tv.turn_off()


class TVOffCommand(Command):
    def __init__(self, tv: Television):
        self.tv = tv
    
    def execute(self):
        self.tv.turn_off()
    
    def undo(self):
        self.tv.turn_on()


class TVVolumeCommand(Command):
    def __init__(self, tv: Television, volume: int):
        self.tv = tv
        self.volume = volume
        self.previous_volume = 0
    
    def execute(self):
        self.previous_volume = self.tv.set_volume(self.volume)
    
    def undo(self):
        self.tv.set_volume(self.previous_volume)


class TVChannelCommand(Command):
    def __init__(self, tv: Television, channel: int):
        self.tv = tv
        self.channel = channel
        self.previous_channel = 0
    
    def execute(self):
        self.previous_channel = self.tv.set_channel(self.channel)
    
    def undo(self):
        self.tv.set_channel(self.previous_channel)


# MACRO COMMAND execute multiple commands as a single command
class MacroCommand(Command):
    
    def __init__(self, commands: List[Command]):
        self.commands = commands
    
    def execute(self):
        for command in self.commands:
            command.execute()
    
    def undo(self):
        for command in reversed(self.commands):
            command.undo()


# INVOKER
class RemoteControl:
    
    def __init__(self):
        self.command_history: List[Command] = []
        self.undo_history: List[Command] = []
    
    def execute_command(self, command: Command):
        command.execute()
        self.command_history.append(command)
        self.undo_history.clear() # Clear redo history on new command
    
    def undo(self):
        if not self.command_history:
            print("Nothing to undo")
            return
        
        print("\n[Undo]")
        command = self.command_history.pop()
        command.undo()
        self.undo_history.append(command)
    
    def redo(self):
        if not self.undo_history:
            print("Nothing to redo")
            return
        
        print("\n[Redo]")
        command = self.undo_history.pop()
        command.execute()
        self.command_history.append(command)
    
    def show_history(self):
        print("\n[Command History]")
        if not self.command_history:
            print("(empty)")
        else:
            for i, cmd in enumerate(self.command_history, 1):
                print(f"{i}. {cmd.__class__.__name__}")


# USAGE

print("=" * 60)
print("SMART HOME REMOTE - WITH COMMAND PATTERN")
print("=" * 60)

living_room_light = Light("Living Room")
bedroom_light = Light("Bedroom")
living_room_fan = Fan("Living Room")
bedroom_ac = AirConditioner("Bedroom")
living_room_tv = Television("Living Room")

remote = RemoteControl()

print("\nSCENARIO 1: Basic commands")
remote.execute_command(LightOnCommand(living_room_light))
remote.execute_command(FanOnCommand(living_room_fan, speed=4))
remote.execute_command(ACOnCommand(bedroom_ac))
remote.execute_command(ACTemperatureCommand(bedroom_ac, 22))

print("\nSCENARIO 2: Undo and redo")
remote.execute_command(TVOnCommand(living_room_tv))
remote.execute_command(TVVolumeCommand(living_room_tv, 25))
remote.execute_command(TVChannelCommand(living_room_tv, 5))

remote.show_history()
remote.undo()
remote.undo()
remote.redo()
remote.show_history()

print("\nSCENARIO 3: Macro command - Movie mode")
movie_mode = MacroCommand([
    LightOffCommand(living_room_light),
    FanSpeedCommand(living_room_fan, 2),
    TVOnCommand(living_room_tv),
    TVVolumeCommand(living_room_tv, 30),
    TVChannelCommand(living_room_tv, 10)
])

remote.execute_command(movie_mode)
remote.undo()

print("\nSCENARIO 4: Macro command - Good night mode")
good_night_mode = MacroCommand([
    LightOffCommand(living_room_light),
    LightOffCommand(bedroom_light),
    FanOffCommand(living_room_fan),
    TVOffCommand(living_room_tv),
    ACOnCommand(bedroom_ac),
    ACTemperatureCommand(bedroom_ac, 24)
])

remote.execute_command(good_night_mode)
remote.show_history()
