class WindowsButton:
    def render(self):
        print("Rendering Windows-style button")
        print("[  Submit  ]  (Windows Look)")
    
    def on_click(self):
        print("Windows button clicked!")


class MacButton:
    def render(self):
        print("Rendering Mac-style button")
        print("(  Submit  )  (Mac Look)")
    
    def on_click(self):
        print("Mac button clicked!")


class LinuxButton:
    def render(self):
        print("Rendering Linux-style button")
        print("|  Submit  |  (Linux Look)")
    
    def on_click(self):
        print("Linux button clicked!")


class WindowsCheckbox:
    def render(self):
        print("Rendering Windows-style checkbox")
        print("[ ] Accept Terms (Windows Look)")
    
    def toggle(self):
        print("Windows checkbox toggled!")


class MacCheckbox:
    def render(self):
        print("Rendering Mac-style checkbox")
        print("() Accept Terms (Mac Look)")
    
    def toggle(self):
        print("Mac checkbox toggled!")


class LinuxCheckbox:
    def render(self):
        print("Rendering Linux-style checkbox")
        print("[ ] Accept Terms (Linux Look)")
    
    def toggle(self):
        print("Linux checkbox toggled!")


class Application:
    
    def __init__(self, os_type):
        self.os_type = os_type
        self.button = None
        self.checkbox = None
    
    def create_ui(self):
        print(f"\n{'='*50}")
        print(f"Creating UI for: {self.os_type}")
        print(f"{'='*50}")
        
        if self.os_type == "Windows":
            self.button = WindowsButton()
            self.checkbox = WindowsCheckbox()
        
        elif self.os_type == "Mac":
            self.button = MacButton()
            self.checkbox = MacCheckbox()
        
        elif self.os_type == "Linux":
            self.button = LinuxButton()
            self.checkbox = LinuxCheckbox()
        
        else:
            raise ValueError(f"Unsupported OS: {self.os_type}")
    
    def render(self):
        if self.button and self.checkbox:
            self.button.render()
            self.checkbox.render()
        else:
            print("ERROR: UI not created!")
    
    def interact(self):
        if self.button and self.checkbox:
            self.button.on_click()
            self.checkbox.toggle()
        else:
            print("ERROR: UI not created!")


print("="*60)
print("UI FRAMEWORK - WITHOUT FACTORY PATTERN")
print("="*60)

windows_app = Application("Windows")
windows_app.create_ui()
windows_app.render()
windows_app.interact()

mac_app = Application("Mac")
mac_app.create_ui()
mac_app.render()
mac_app.interact()

linux_app = Application("Linux")
linux_app.create_ui()
linux_app.render()
linux_app.interact()
