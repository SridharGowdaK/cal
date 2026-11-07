class LoginSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        self.users[username] = password
        return True

    def login(self, username, password):
        return self.users.get(username) == password


class LoginPage:
    def __init__(self):
        self.auth = LoginSystem()

    def render(self):
        return "Login page is running"

    def process(self, username, password):
        self.auth.register_user("admin", "admin123")
        return self.auth.login(username, password)

    def run(self, username, password):
        return self.process(username, password)


if __name__ == "__main__":
    page = LoginPage()
    print(page.render())
    print(page.run("admin", "admin123"))
