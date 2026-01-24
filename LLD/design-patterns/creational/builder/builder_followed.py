from abc import ABC, abstractmethod

# PRODUCT - The complex object we want to build
class Computer:
    
    def __init__(self):
        # Required components
        self.cpu = None
        self.ram = None
        self.storage = None
        
        # Optional components
        self.gpu = None
        self.wifi = False
        self.bluetooth = False
        self.cooling_system = None
        self.rgb_lighting = False
        self.operating_system = None
        self.monitor = None
        self.keyboard = None
        self.mouse = None
        self.speakers = False
        self.webcam = False
        self.case_type = "Standard"
    
    def __str__(self):
        specs = f"\n{'='*50}\nCOMPUTER SPECIFICATIONS\n{'='*50}\n"
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


# BUILDER INTERFACE
class ComputerBuilder(ABC):
    
    def __init__(self):
        self.computer = Computer()
    
    @abstractmethod
    def set_cpu(self, cpu): pass
    
    @abstractmethod
    def set_ram(self, ram): pass
    
    @abstractmethod
    def set_storage(self, storage): pass
    
    @abstractmethod
    def set_gpu(self, gpu): pass
    
    @abstractmethod
    def set_connectivity(self, wifi, bluetooth): pass
    
    @abstractmethod
    def set_cooling(self, cooling_system): pass
    
    @abstractmethod
    def set_rgb_lighting(self, enabled): pass
    
    @abstractmethod
    def set_operating_system(self, os): pass
    
    @abstractmethod
    def set_peripherals(self, monitor, keyboard, mouse): pass
    
    @abstractmethod
    def set_accessories(self, speakers, webcam): pass
    
    @abstractmethod
    def set_case(self, case_type): pass
    
    @abstractmethod
    def get_computer(self): pass


# CONCRETE BUILDERS - Different representations

class GamingComputerBuilder(ComputerBuilder):
    
    def set_cpu(self, cpu="Intel i9-13900K"):
        self.computer.cpu = cpu
        return self  # Return self for method chaining
    
    def set_ram(self, ram=32):
        if ram < 16:
            raise ValueError("Gaming PC needs at least 16GB RAM")
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage=1000):
        if storage < 500:
            raise ValueError("Gaming PC needs at least 500GB storage")
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu="NVIDIA RTX 4090"):
        self.computer.gpu = gpu
        return self
    
    def set_connectivity(self, wifi=True, bluetooth=True):
        self.computer.wifi = wifi
        self.computer.bluetooth = bluetooth
        return self
    
    def set_cooling(self, cooling_system="Liquid Cooling"):
        self.computer.cooling_system = cooling_system
        return self
    
    def set_rgb_lighting(self, enabled=True):
        self.computer.rgb_lighting = enabled
        return self
    
    def set_operating_system(self, os="Windows 11 Pro"):
        self.computer.operating_system = os
        return self
    
    def set_peripherals(self, monitor="27-inch 4K 144Hz", keyboard="Mechanical RGB", mouse="Gaming Mouse"):
        self.computer.monitor = monitor
        self.computer.keyboard = keyboard
        self.computer.mouse = mouse
        return self
    
    def set_accessories(self, speakers=True, webcam=True):
        self.computer.speakers = speakers
        self.computer.webcam = webcam
        return self
    
    def set_case(self, case_type="Gaming Tower"):
        self.computer.case_type = case_type
        return self
    
    def get_computer(self):
        """Validate and return the built computer"""
        if not self.computer.cpu or not self.computer.ram or not self.computer.storage:
            raise ValueError("CPU, RAM, and Storage are required!")
        return self.computer


class OfficeComputerBuilder(ComputerBuilder):

    def set_cpu(self, cpu="Intel i5-12400"):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram=16):
        if ram < 8:
            raise ValueError("Office PC needs at least 8GB RAM")
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage=512):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu=None):
        self.computer.gpu = gpu  # Office PC may not need GPU
        return self
    
    def set_connectivity(self, wifi=True, bluetooth=True):
        self.computer.wifi = wifi
        self.computer.bluetooth = bluetooth
        return self
    
    def set_cooling(self, cooling_system="Standard Cooling"):
        self.computer.cooling_system = cooling_system
        return self
    
    def set_rgb_lighting(self, enabled=False):
        self.computer.rgb_lighting = enabled  # No RGB for office
        return self
    
    def set_operating_system(self, os="Windows 11 Pro"):
        self.computer.operating_system = os
        return self
    
    def set_peripherals(self, monitor="24-inch Full HD", keyboard="Standard Keyboard", mouse="Standard Mouse"):
        self.computer.monitor = monitor
        self.computer.keyboard = keyboard
        self.computer.mouse = mouse
        return self
    
    def set_accessories(self, speakers=False, webcam=True):
        self.computer.speakers = speakers
        self.computer.webcam = webcam  # Webcam needed for meetings
        return self
    
    def set_case(self, case_type="Mini Tower"):
        self.computer.case_type = case_type
        return self
    
    def get_computer(self):
        if not self.computer.cpu or not self.computer.ram or not self.computer.storage:
            raise ValueError("CPU, RAM, and Storage are required!")
        return self.computer


class ServerBuilder(ComputerBuilder):
    
    def set_cpu(self, cpu="AMD EPYC 7763"):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram=128):
        if ram < 32:
            raise ValueError("Server needs at least 32GB RAM")
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage=2000):
        if storage < 1000:
            raise ValueError("Server needs at least 1TB storage")
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu=None):
        self.computer.gpu = gpu  # Servers typically don't need GPU
        return self
    
    def set_connectivity(self, wifi=True, bluetooth=False):
        self.computer.wifi = wifi
        self.computer.bluetooth = bluetooth 
        return self
    
    def set_cooling(self, cooling_system="Server-grade Cooling"):
        self.computer.cooling_system = cooling_system
        return self
    
    def set_rgb_lighting(self, enabled=False):
        self.computer.rgb_lighting = enabled  
        return self
    
    def set_operating_system(self, os="Ubuntu Server 22.04"):
        self.computer.operating_system = os
        return self
    
    def set_peripherals(self, monitor=None, keyboard=None, mouse=None):
        # Servers typically don't need peripherals (headless)
        self.computer.monitor = monitor
        self.computer.keyboard = keyboard
        self.computer.mouse = mouse
        return self
    
    def set_accessories(self, speakers=False, webcam=False):
        self.computer.speakers = speakers
        self.computer.webcam = webcam
        return self
    
    def set_case(self, case_type="Server Rack"):
        self.computer.case_type = case_type
        return self
    
    def get_computer(self):
        if not self.computer.cpu or not self.computer.ram or not self.computer.storage:
            raise ValueError("CPU, RAM, and Storage are required!")
        return self.computer


# DIRECTOR (Optional) - Director knows how to build specific computer configurations

class ComputerDirector:
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_budget_gaming_pc(self):
        return (self.builder
                .set_cpu("Intel i5-12400F")
                .set_ram(16)
                .set_storage(500)
                .set_gpu("NVIDIA RTX 3060")
                .set_connectivity(True, True)
                .set_cooling("Air Cooling")
                .set_rgb_lighting(True)
                .set_operating_system("Windows 11 Home")
                .set_peripherals("24-inch 1080p 144Hz", "Basic Mechanical", "Budget Gaming Mouse")
                .set_accessories(False, True)
                .set_case("Mid Tower")
                .get_computer())
    
    def build_high_end_gaming_pc(self):
        return (self.builder
                .set_cpu("Intel i9-13900K")
                .set_ram(64)
                .set_storage(2000)
                .set_gpu("NVIDIA RTX 4090")
                .set_connectivity(True, True)
                .set_cooling("Custom Liquid Cooling")
                .set_rgb_lighting(True)
                .set_operating_system("Windows 11 Pro")
                .set_peripherals("32-inch 4K 240Hz", "Premium Mechanical RGB", "Pro Gaming Mouse")
                .set_accessories(True, True)
                .set_case("Full Tower RGB")
                .get_computer())
    
    def build_basic_office_pc(self):
        """Build a basic office computer"""
        return (self.builder
                .set_cpu("Intel i3-12100")
                .set_ram(8)
                .set_storage(256)
                .set_connectivity(True, True)
                .set_operating_system("Windows 11 Pro")
                .set_peripherals("22-inch Full HD", "Standard Keyboard", "Standard Mouse")
                .set_accessories(False, True)
                .get_computer())


# USAGE DEMONSTRATION
print("="*60)
print("COMPUTER BUILDER - WITH BUILDER PATTERN")
print("="*60)

# Method 1: Using Builder directly with method chaining
print("\n--- Building Gaming Computer ---")
gaming_builder = GamingComputerBuilder()
gaming_pc = (gaming_builder
             .set_cpu("Intel i9-13900K")
             .set_ram(32)
             .set_storage(1000)
             .set_gpu("NVIDIA RTX 4090")
             .set_connectivity(True, True)
             .set_cooling("Liquid Cooling")
             .set_rgb_lighting(True)
             .set_operating_system("Windows 11 Pro")
             .set_peripherals("27-inch 4K", "Mechanical RGB", "Gaming Mouse")
             .set_accessories(True, True)
             .set_case("Gaming Tower")
             .get_computer())

print(gaming_pc)

# Method 2: Building step-by-step (more readable)
print("\n--- Building Office Computer (Step-by-Step) ---")
office_builder = OfficeComputerBuilder()
office_builder.set_cpu("Intel i5-12400")
office_builder.set_ram(16)
office_builder.set_storage(512)
office_builder.set_connectivity(True, True)
office_builder.set_operating_system("Windows 11 Pro")
office_builder.set_peripherals("24-inch Full HD", "Standard Keyboard", "Standard Mouse")
office_builder.set_accessories(False, True)

office_pc = office_builder.get_computer()
print(office_pc)

# Method 3: Using Director for predefined configurations
print("\n--- Using Director for Predefined Builds ---")

print("\n Budget Gaming PC:")
director = ComputerDirector(GamingComputerBuilder())
budget_gaming = director.build_budget_gaming_pc()
print(budget_gaming)

print("\n High-End Gaming PC:")
director = ComputerDirector(GamingComputerBuilder())
high_end_gaming = director.build_high_end_gaming_pc()
print(high_end_gaming)

print("\n Basic Office PC:")
director = ComputerDirector(OfficeComputerBuilder())
basic_office = director.build_basic_office_pc()
print(basic_office)

# Method 4: Building Server
print("\n--- Building Server ---")
server_builder = ServerBuilder()
server = (server_builder
          .set_cpu("AMD EPYC 7763")
          .set_ram(128)
          .set_storage(4000)
          .set_connectivity(True, False)
          .set_cooling("Server-grade Cooling")
          .set_operating_system("Ubuntu Server 22.04")
          .set_case("Server Rack")
          .get_computer())

print(server)

# Validation example
print("\n--- Validation Example ---")
try:
    invalid_gaming = GamingComputerBuilder()
    invalid_gaming.set_cpu("Intel i5")
    # invalid_gaming.set_ram(16)
    invalid_gaming.set_ram(8)  # Too low for gaming 
    # invalid_gaming.set_storage(1000)
    computer = invalid_gaming.get_computer()
    print(computer)
except ValueError as e:
    print(f" Validation caught error: {e}")
