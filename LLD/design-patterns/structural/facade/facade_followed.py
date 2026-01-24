class SecuritySystem:
    
    def arm_system(self):
        print("SecuritySystem: arming system")
        print(" - checking sensors")
        print(" - activating motion detectors")
        print(" - enabling door and window sensors")
        print(" - system armed")
    
    def disarm_system(self):
        print("SecuritySystem: disarming system")
        print(" - motion detectors off")
        print(" - alarm disabled")
        print(" - system disarmed")
    
    def set_panic_mode(self):
        print("SecuritySystem: PANIC MODE activated")


class LightingSystem:
    
    def turn_on_all_lights(self):
        print("LightingSystem: turning ON all lights")
        print(" - all rooms ON")
    
    def turn_off_all_lights(self):
        print("LightingSystem: turning OFF all lights")
        print(" - all rooms OFF")
    
    def set_mood_lighting(self, mood):
        print(f"LightingSystem: setting mood = {mood}")
        print(" - brightness and color adjusted")
    
    def set_brightness(self, level):
        print(f"LightingSystem: brightness set to {level}%")


class ClimateControl:
    
    def set_temperature(self, temp):
        print(f"ClimateControl: temperature set to {temp}C")
        print(" - thermostat adjusted")
    
    def turn_on_ac(self):
        print("ClimateControl: AC ON")
    
    def turn_on_heating(self):
        print("ClimateControl: heating ON")
    
    def turn_off_climate_control(self):
        print("ClimateControl: system OFF")
    
    def set_eco_mode(self):
        print("ClimateControl: eco mode enabled")


class EntertainmentSystem:
    
    def turn_on_tv(self):
        print("EntertainmentSystem: TV ON")
    
    def turn_off_tv(self):
        print("EntertainmentSystem: TV OFF")
    
    def set_volume(self, level):
        print(f"EntertainmentSystem: volume set to {level}")
    
    def start_streaming(self, service):
        print(f"EntertainmentSystem: starting {service}")
        print(" - ready to stream")
    
    def turn_on_sound_system(self):
        print("EntertainmentSystem: sound system ON")
    
    def turn_off_sound_system(self):
        print("EntertainmentSystem: sound system OFF")


class WindowBlinds:
    
    def open_all_blinds(self):
        print("WindowBlinds: opening all blinds")
    
    def close_all_blinds(self):
        print("WindowBlinds: closing all blinds")
    
    def set_position(self, position):
        print(f"WindowBlinds: position set to {position}%")


class DoorLocks:
    
    def lock_all_doors(self):
        print("DoorLocks: locking all doors")
        print(" - all doors LOCKED")
    
    def unlock_all_doors(self):
        print("DoorLocks: unlocking all doors")
        print(" - all doors UNLOCKED")


class GarageDoor:
    
    def open_garage(self):
        print("GarageDoor: opening garage")
        print(" - garage open")
    
    def close_garage(self):
        print("GarageDoor: closing garage")
        print(" - garage closed")


# Facade providing simplified interface for smart home operations
class SmartHomeFacade:
    
    def __init__(self):
        self._security = SecuritySystem()
        self._lights = LightingSystem()
        self._climate = ClimateControl()
        self._entertainment = EntertainmentSystem()
        self._blinds = WindowBlinds()
        self._locks = DoorLocks()
        self._garage = GarageDoor()
    
    # High-level operations    

    def leave_home(self):
        print("\n[Facade] Leaving home sequence started")
        print("-" * 50)
        
        self._entertainment.turn_off_tv()
        self._entertainment.turn_off_sound_system()
        self._lights.turn_off_all_lights()
        self._climate.turn_off_climate_control()
        self._blinds.close_all_blinds()
        self._locks.lock_all_doors()
        self._security.arm_system()
        self._garage.open_garage()
        
        print("-" * 50)
        print("[Facade] Home ready for departure")
    
    def arrive_home(self):
        print("\n[Facade] Arriving home sequence started")
        print("-" * 50)
        
        self._garage.close_garage()
        self._security.disarm_system()
        self._locks.unlock_all_doors()
        self._lights.turn_on_all_lights()
        self._lights.set_brightness(70)
        self._climate.set_temperature(22)
        self._blinds.open_all_blinds()
        
        print("-" * 50)
        print("[Facade] Home ready for use")
    
    def movie_night(self):
        print("\n[Facade] Movie night setup started")
        print("-" * 50)
        
        self._lights.set_mood_lighting("cinema")
        self._lights.set_brightness(20)
        self._blinds.close_all_blinds()
        self._climate.set_temperature(21)
        self._entertainment.turn_on_tv()
        self._entertainment.turn_on_sound_system()
        self._entertainment.set_volume(60)
        self._entertainment.start_streaming("Netflix")
        
        print("-" * 50)
        print("[Facade] Movie night ready")
    
    def sleep_mode(self):
        print("\n[Facade] Sleep mode started")
        print("-" * 50)
        
        self._entertainment.turn_off_tv()
        self._entertainment.turn_off_sound_system()
        self._lights.turn_off_all_lights()
        self._climate.set_temperature(20)
        self._blinds.close_all_blinds()
        self._locks.lock_all_doors()
        self._security.arm_system()
        
        print("-" * 50)
        print("[Facade] Sleep mode active")
    
    def party_mode(self):
        print("\n[Facade] Party mode started")
        print("-" * 50)
        
        self._lights.set_mood_lighting("party")
        self._lights.set_brightness(80)
        self._climate.set_temperature(21)
        self._entertainment.turn_on_sound_system()
        self._entertainment.set_volume(75)
        self._security.disarm_system()
        
        print("-" * 50)
        print("[Facade] Party mode active")
    
    def vacation_mode(self):
        print("\n[Facade] Vacation mode started")
        print("-" * 50)
        
        self._lights.turn_off_all_lights()
        self._entertainment.turn_off_tv()
        self._entertainment.turn_off_sound_system()
        self._climate.set_eco_mode()
        self._blinds.close_all_blinds()
        self._locks.lock_all_doors()
        self._security.arm_system()
        
        print("-" * 50)
        print("[Facade] Home secured for vacation")
    
    def emergency_mode(self):
        print("\n[Facade] EMERGENCY mode started")
        print("-" * 50)
        
        self._security.set_panic_mode()
        self._lights.turn_on_all_lights()
        self._locks.unlock_all_doors()
        
        print("-" * 50)
        print("[Facade] Emergency handling active")
    
    # Optional direct access
    
    def get_lighting_system(self):
        return self._lights
    
    def get_climate_control(self):
        return self._climate
    
    def get_security_system(self):
        return self._security


# CLIENT CODE

print("=" * 60)
print("SMART HOME SYSTEM - WITH FACADE PATTERN")
print("=" * 60)

smart_home = SmartHomeFacade()

print("\nSCENARIO: Leaving home")
smart_home.leave_home()

print("\nSCENARIO: Arriving home")
smart_home.arrive_home()

print("\nSCENARIO: Movie night")
smart_home.movie_night()

print("\nSCENARIO: Sleep mode")
smart_home.sleep_mode()

print("\nSCENARIO: Party mode")
smart_home.party_mode()

print("\nSCENARIO: Vacation mode")
smart_home.vacation_mode()

print("\nSCENARIO: Emergency")
smart_home.emergency_mode()

print("\nAdvanced usage: direct lighting access")
lights = smart_home.get_lighting_system()
lights.set_brightness(50)
