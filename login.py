from abc import ABC, abstractmethod
import builtins


class print(ABC):
    @abstractmethod
    def render(self):
        """Return the page content to display."""
        raise NotImplementedError

    @abstractmethod
    def process(self):
        """Run the login-page behavior."""
        raise NotImplementedError

    def run(self):
        """Execute the page logic and return a useful result."""
        return self.process()


class LoginPage(print):
    def render(self):
        return "login page is running"

    def process(self):
        return self.render()


if __name__ == "__main__":
    builtins.print(LoginPage().run())
