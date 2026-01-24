# computer class Constructor with many optional parameters
class Computer:

    def __init__(
        self,
        cpu,
        ram,
        storage,
        gpu=None,
        wifi=False,
        bluetooth=False,
        cooling_system=None,
        rgb_lighting=False,
        operating_system=None,
        monitor=None,
        keyboard=None,
        mouse=None,
        speakers=False,
        webcam=False,
        case_type="Standard"
    ):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.wifi = wifi
        self.bluetooth = bluetooth
        self.cooling_system = cooling_system
        self.rgb_lighting = rgb_lighting
        self.operating_system = operating_system
        self.monitor = monitor
        self.keyboard = keyboard
        self.mouse = mouse
        self.speakers = speakers
        self.webcam = webcam
        self.case_type = case_type
    
    def __str__(self):
        specs = f"\n{'='*50}\n COMPUTER SPECIFICATIONS\n{'='*50}\n"
        specs += f"CPU: {self.cpu}\n"
        specs += f"RAM: {self.ram}GB\n"
        specs += f"Storage: {self.storage}GB SSD\n"
        
        if self.gpu:
            specs += f"GPU: {self.gpu}\n"
        if self.wifi:
            specs += f"WiFi: Enabled\n"
        if self.bluetooth:
            specs += f"Bluetooth: Enabled\n"
        if self.cooling_system:
            specs += f"Cooling: {self.cooling_system}\n"
        if self.rgb_lighting:
            specs += f"RGB Lighting: Yes\n"
        if self.operating_system:
            specs += f"OS: {self.operating_system}\n"
        if self.monitor:
            specs += f"Monitor: {self.monitor}\n"
        if self.keyboard:
            specs += f"Keyboard: {self.keyboard}\n"
        if self.mouse:
            specs += f"Mouse: {self.mouse}\n"
        if self.speakers:
            specs += f"Speakers: Included\n"
        if self.webcam:
            specs += f"Webcam: Included\n"
        
        specs += f"Case: {self.case_type}\n"
        specs += f"{'='*50}"
        
        return specs


# Usage
print("="*60)
print("COMPUTER BUILDER - WITHOUT BUILDER PATTERN")
print("="*60)

# Problem 1 : to many parameters make it hard to read and maintain
print("\n--- Creating Gaming Computer ---")
gaming_pc = Computer(
    "Intel i9-13900K",           # cpu
    32,                          # ram
    1000,                        # storage
    "NVIDIA RTX 4090",           # gpu
    True,                        # wifi
    True,                        # bluetooth
    "Liquid Cooling",            # cooling_system
    True,                        # rgb_lighting
    "Windows 11 Pro",            # operating_system
    "27-inch 4K",                # monitor
    "Mechanical RGB",            # keyboard
    "Gaming Mouse",              # mouse
    True,                        # speakers
    True,                        # webcam
    "Gaming Tower"               # case_type
)
print(gaming_pc)

# Problem 2: Easy to make mistakes with parameter order
print("\n--- Creating Office Computer (Wrong Order!) ---")
office_pc = Computer(
    "Intel i5-12400",
    16,
    512,
    None,
    True,
    "Standard Cooling",          # Should be cooling_system but passed to bluetooth!
    False,                       # Parameters are misaligned!
    False,
    "Windows 11",
    None,
    "Standard Keyboard",
    "Standard Mouse",
    False,
    False,
    "Mini Tower"
)
print(office_pc)
print("\nERROR: Parameters got mixed up! Bluetooth got cooling system value!")

# Problem 3: Must provide all parameters even for simple build
print("\n--- Creating Basic Computer ---")
basic_pc = Computer(
    "Intel i3-12100",
    8,
    256,
    None,                        # No GPU
    False,                       # No WiFi
    False,                       # No Bluetooth
    None,                        # No special cooling
    False,                       # No RGB
    "Windows 11 Home",
    None,                        # No monitor
    None,                        # No keyboard
    None,                        # No mouse
    False,                       # No speakers
    False,                       # No webcam
    "Standard"                   # case_type
)
print(basic_pc)

# Problem 4: Cannot validate during construction
print("\n--- Creating Invalid Computer ---")
try:
    invalid_pc = Computer(
        "",                      # Empty CPU - should be invalid!
        0,                       # 0 RAM - should be invalid!
        -100,                    # Negative storage - should be invalid!
        "Invalid GPU",
        True,
        True,
        "Cooling",
        True,
        "OS",
        "Monitor",
        "Keyboard",
        "Mouse",
        True,
        True,
        "Case"
    )
    print(invalid_pc)
    print("\nERROR: Invalid computer created! No validation during construction!")
except Exception as e:
    print(f"Error: {e}")

# Problem 5: Different computer types require different parameter combinations
print("\n--- Creating Server Computer (Messy!) ---")
server = Computer(
    "AMD EPYC 7763",
    128,                         # Lots of RAM for server
    2000,                        # Lots of storage
    None,                        # Servers don't need GPU usually
    True,                        # WiFi
    False,                       # No Bluetooth for server
    "Server-grade Cooling",
    False,                       # No RGB for server
    "Ubuntu Server 22.04",
    None,                        # No monitor
    None,                        # No keyboard
    None,                        # No mouse
    False,                       # No speakers
    False,                       # No webcam
    "Server Rack"
)
print(server)
