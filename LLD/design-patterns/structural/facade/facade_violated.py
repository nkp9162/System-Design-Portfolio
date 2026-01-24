# COMPLEX SUBSYSTEMS - Home Automation Components

class SecuritySystem:

    def arm_system(self):
        print("SecuritySystem: arming system...")
        print(" - checking all sensors")
        print(" - activating motion detectors")
        print(" - enabling door and window sensors")
        print(" - system armed successfully")
    
    def disarm_system(self):
        print("SecuritySystem: disarming system...")
        print(" - motion detectors off")
        print(" - alarm disabled")
        print(" - system disarmed")
    
    def set_panic_mode(self):
        print("SecuritySystem: PANIC MODE")
        print(" - all alarms triggered")
        print(" - security company notified")
        print(" - alerts sent to user")


class LightingSystem:
    
    def turn_on_all_lights(self):
        print("LightingSystem: turning ON all lights")
        print(" - living room ON")
        print(" - bedroom ON")
        print(" - kitchen ON")
        print(" - bathroom ON")
    
    def turn_off_all_lights(self):
        print("LightingSystem: turning OFF all lights")
        print(" - living room OFF")
        print(" - bedroom OFF")
        print(" - kitchen OFF")
        print(" - bathroom OFF")
    
    def set_mood_lighting(self, mood):
        print(f"LightingSystem: setting mood = {mood}")
        print(" - adjusting brightness")
        print(" - adjusting color temperature")
    
    def set_brightness(self, level):
        print(f"LightingSystem: brightness set to {level}%")


class ClimateControl:
    """HVAC and climate control system"""
    
    def set_temperature(self, temp):
        print(f"ClimateControl: setting temperature to {temp}C")
        print(" - thermostat adjusted")
        print(" - HVAC active")
    
    def turn_on_ac(self):
        print("ClimateControl: AC ON")
        print(" - compressor started")
        print(" - cooling mode enabled")
    
    def turn_on_heating(self):
        print("ClimateControl: heating ON")
        print(" - heater started")
        print(" - heating mode enabled")
    
    def turn_off_climate_control(self):
        print("ClimateControl: system turned OFF")


class EntertainmentSystem:
    
    def turn_on_tv(self):
        print("EntertainmentSystem: TV ON")
    
    def turn_off_tv(self):
        print("EntertainmentSystem: TV OFF")
    
    def set_volume(self, level):
        print(f"EntertainmentSystem: volume set to {level}")
    
    def start_streaming(self, service):
        print(f"EntertainmentSystem: starting {service}")
        print(" - internet connected")
        print(" - app loaded")
        print(" - ready to stream")
    
    def turn_on_sound_system(self):
        print("EntertainmentSystem: sound system ON")
        print(" - speakers initialized")
        print(" - receiver connected")
    
    def turn_off_sound_system(self):
        print("EntertainmentSystem: sound system OFF")


class WindowBlinds:
    
    def open_all_blinds(self):
        print("WindowBlinds: opening all blinds")
        print(" - living room OPEN")
        print(" - bedroom OPEN")
    
    def close_all_blinds(self):
        print("WindowBlinds: closing all blinds")
        print(" - living room CLOSED")
        print(" - bedroom CLOSED")
    
    def set_position(self, position):
        print(f"WindowBlinds: position set to {position}%")


class DoorLocks:
    
    def lock_all_doors(self):
        print("DoorLocks: locking all doors")
        print(" - front door LOCKED")
        print(" - back door LOCKED")
        print(" - garage door LOCKED")
    
    def unlock_all_doors(self):
        print("DoorLocks: unlocking all doors")
        print(" - front door UNLOCKED")
        print(" - back door UNLOCKED")


class GarageDoor:
    
    def open_garage(self):
        print("GarageDoor: opening garage")
        print(" - safety sensors checked")
        print(" - motor activated")
        print(" - garage is open")
    
    def close_garage(self):
        print("GarageDoor: closing garage")
        print(" - motor activated")
        print(" - garage is closed")


# CLIENT CODE - Must interact with all subsystems directly
def leaving_home_scenario():
    print("\n" + "="*60)
    print("LEAVING HOME - manual flow")
    print("="*60)
    
    security = SecuritySystem()
    lights = LightingSystem()
    climate = ClimateControl()
    entertainment = EntertainmentSystem()
    blinds = WindowBlinds()
    locks = DoorLocks()
    garage = GarageDoor()
    
    print("\n[1] Turning off entertainment")
    entertainment.turn_off_tv()
    entertainment.turn_off_sound_system()
    
    print("\n[2] Turning off lights")
    lights.turn_off_all_lights()
    
    print("\n[3] Turning off climate control")
    climate.turn_off_climate_control()
    
    print("\n[4] Closing blinds")
    blinds.close_all_blinds()
    
    print("\n[5] Locking doors")
    locks.lock_all_doors()
    
    print("\n[6] Arming security system")
    security.arm_system()
    
    print("\n[7] Opening garage")
    garage.open_garage()
    
    print("\nNOTE: Too many subsystems involved for a simple task")


def arriving_home_scenario():
    print("\n" + "="*60)
    print("ARRIVING HOME - manual flow")
    print("="*60)
    
    security = SecuritySystem()
    lights = LightingSystem()
    climate = ClimateControl()
    entertainment = EntertainmentSystem()
    blinds = WindowBlinds()
    locks = DoorLocks()
    garage = GarageDoor()
    
    print("\n[1] Closing garage")
    garage.close_garage()
    
    print("\n[2] Disarming security")
    security.disarm_system()
    
    print("\n[3] Unlocking doors")
    locks.unlock_all_doors()
    
    print("\n[4] Turning on lights")
    lights.turn_on_all_lights()
    lights.set_brightness(70)
    
    print("\n[5] Setting temperature")
    climate.set_temperature(22)
    
    print("\n[6] Opening blinds")
    blinds.open_all_blinds()
    
    print("\nNOTE: Client must remember full sequence")


def movie_night_scenario():
    print("\n" + "="*60)
    print("MOVIE NIGHT MODE - manual flow")
    print("="*60)
    
    lights = LightingSystem()
    climate = ClimateControl()
    entertainment = EntertainmentSystem()
    blinds = WindowBlinds()
    
    print("\n[1] Setting lighting")
    lights.set_mood_lighting("cinema")
    lights.set_brightness(20)
    
    print("\n[2] Closing blinds")
    blinds.close_all_blinds()
    
    print("\n[3] Setting temperature")
    climate.set_temperature(21)
    
    print("\n[4] Starting entertainment")
    entertainment.turn_on_tv()
    entertainment.turn_on_sound_system()
    entertainment.set_volume(60)
    entertainment.start_streaming("Netflix")
    
    print("\nNOTE: Too many calls just to watch a movie")


# USAGE
print("="*60)
print("SMART HOME SYSTEM - WITHOUT FACADE PATTERN")
print("="*60)

leaving_home_scenario()
arriving_home_scenario()
movie_night_scenario()
