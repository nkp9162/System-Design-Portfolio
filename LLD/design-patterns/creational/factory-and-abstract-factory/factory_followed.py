from abc import ABC, abstractmethod

#  Product Interfaces 
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def on_click(self):
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def toggle(self):
        pass


#  Windows UI Components 
class WindowsButton(Button):
    def render(self):
        print("Rendering Windows-style button")
        print("[ Submit ] (Windows Look)")

    def on_click(self):
        print("Windows button clicked!")


class WindowsCheckbox(Checkbox):
    def render(self):
        print("Rendering Windows-style checkbox")
        print("[ ] Accept Terms (Windows Look)")

    def toggle(self):
        print("Windows checkbox toggled!")


#  Mac UI Components 
class MacButton(Button):
    def render(self):
        print("Rendering Mac-style button")
        print("( Submit ) (Mac Look)")

    def on_click(self):
        print("Mac button clicked!")


class MacCheckbox(Checkbox):
    def render(self):
        print("Rendering Mac-style checkbox")
        print("( ) Accept Terms (Mac Look)")

    def toggle(self):
        print("Mac checkbox toggled!")


#  Linux UI Components 
class LinuxButton(Button):
    def render(self):
        print("Rendering Linux-style button")
        print("| Submit | (Linux Look)")

    def on_click(self):
        print("Linux button clicked!")


class LinuxCheckbox(Checkbox):
    def render(self):
        print("Rendering Linux-style checkbox")
        print("[ ] Accept Terms (Linux Look)")

    def toggle(self):
        print("Linux checkbox toggled!")


#  Abstract Factory 
class GUIFactory(ABC):

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


#  Concrete Factories 
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


class LinuxFactory(GUIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()


#  Client Code 
class Application:
    """
    Application depends only on GUIFactory,
    not on concrete UI classes
    """

    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = None
        self.checkbox = None

    def create_ui(self):
        print(f"\n{'='*50}")
        print(f"Creating UI using {self.factory.__class__.__name__}")
        print(f"{'='*50}")

        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()

    def render(self):
        self.button.render()
        self.checkbox.render()

    def interact(self):
        self.button.on_click()
        self.checkbox.toggle()


#  Factory Method (Factory of Factories) 
class GUIFactoryCreator:
    @staticmethod
    def get_factory(os_type: str) -> GUIFactory:
        factories = {
            "Windows": WindowsFactory(),
            "Mac": MacFactory(),
            "Linux": LinuxFactory()
        }

        factory = factories.get(os_type)
        if not factory:
            raise ValueError(f"Unsupported OS: {os_type}")

        return factory


# Usage
print("="*60)
print("UI FRAMEWORK - WITH FACTORY PATTERNS")
print("="*60)

# Using Abstract Factory to get UI components
windows_app = Application(WindowsFactory())
windows_app.create_ui()
windows_app.render()
windows_app.interact()

mac_app = Application(MacFactory())
mac_app.create_ui()
mac_app.render()
mac_app.interact()

# Using Factory Method to get factories
linux_factory = GUIFactoryCreator.get_factory("Linux")
linux_app = Application(linux_factory)
linux_app.create_ui()
linux_app.render()
linux_app.interact()


#  Adding New OS (Android) 

class AndroidButton(Button):
    def render(self):
        print("Rendering Android-style button")
        print("{ Submit } (Material Design)")

    def on_click(self):
        print("Android button clicked!")


class AndroidCheckbox(Checkbox):
    def render(self):
        print("Rendering Android-style checkbox")
        print("( ) Accept Terms (Material Design)")

    def toggle(self):
        print("Android checkbox toggled!")


class AndroidFactory(GUIFactory):
    def create_button(self) -> Button:
        return AndroidButton()

    def create_checkbox(self) -> Checkbox:
        return AndroidCheckbox()


android_app = Application(AndroidFactory())
android_app.create_ui()
android_app.render()
android_app.interact()

print("\nAndroid support added without touching Application class")
