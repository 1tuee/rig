# Custom web framework for Magnolia
import socket
from threading import Thread
import os
from urllib.parse import parse_qs

class customwebframework:
    def __init__(self, host='127.0.0.1', port=8080, static_dir="static"):
        self.host = host
        self.port = port
        self.routes = {}
        self.middlewares = []
        self.static_dir = static_dir

    def route(self, path, methods=["GET"]):
        """Decorator to register a route."""
        def decorator(func):
            self.routes[path] = {"func": func, "methods": methods}
            return func
        return decorator

    def use(self, middleware):
        """Register a middleware function."""
        self.middlewares.append(middleware)

    def start(self):
        """Start the server."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on http://{self.host}:{self.port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            Thread(target=self.handle_request, args=(client_socket,)).start()

    def handle_request(self, client_socket):
        """Handle incoming HTTP requests."""
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                client_socket.close()
                return

            # Parse the request
            request_line = request.splitlines()[0]
            method, path, _ = request_line.split()
            headers = self.parse_headers(request)
            body = self.parse_body(request, headers)

            # Middleware processing
            for middleware in self.middlewares:
                middleware(method, path, headers, body)

            # Static file handling
            if path.startswith(f"/{self.static_dir}/"):
                response = self.serve_static(path)
            # Route handling
            elif path in self.routes:
                route = self.routes[path]
                if method in route["methods"]:
                    response = route["func"](method, headers, body)
                else:
                    response = self.method_not_allowed()
            else:
                response = self.default_response()

            client_socket.sendall(response)
        except Exception as e:
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e).encode())
        finally:
            client_socket.close()

    def parse_headers(self, request):
        """Parse HTTP headers."""
        headers = {}
        lines = request.splitlines()
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return headers

    def parse_body(self, request, headers):
        """Parse HTTP body (for POST requests)."""
        if "Content-Length" in headers:
            content_length = int(headers["Content-Length"])
            body = request.split("\r\n\r\n", 1)[1][:content_length]
            return parse_qs(body)
        return {}

    def serve_static(self, path):
        """Serve static files."""
        file_path = path.lstrip("/")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            return b"HTTP/1.1 200 OK\r\n\r\n" + content
        else:
            return self.default_response()

    def default_response(self):
        """Default 404 response."""
        return b"HTTP/1.1 404 Not Found\r\n\r\nPage not found"

    def method_not_allowed(self):
        """405 Method Not Allowed response."""
        return b"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not allowed"

# Helper classes for UI elements
class UIElement:
    """Base class for UI elements."""
    def render(self):
        raise NotImplementedError("Subclasses must implement render()")

class Button(UIElement):
    def __init__(self, text, onclick=""):
        self.text = text
        self.onclick = onclick

    def render(self):
        return f'<button onclick="{self.onclick}">{self.text}</button>'

class TextBox(UIElement):
    def __init__(self, name, placeholder=""):
        self.name = name
        self.placeholder = placeholder

    def render(self):
        return f'<input type="text" name="{self.name}" placeholder="{self.placeholder}">'

class Form(UIElement):
    def __init__(self, action, method="GET", content=""):
        self.action = action
        self.method = method
        self.content = content

    def render(self):
        return f'<form action="{self.action}" method="{self.method}">{self.content}</form>'

# Example usage of the framework
app = customwebframework()

# Middleware example
def logger(method, path, headers, body):
    print(f"{method} {path}")
app.use(logger)

@app.route("/", methods=["GET"])
def home(method, headers, body):
    """Home route."""
    button = Button("Click Me", "alert('Hello!')").render()
    textbox = TextBox("username", "Enter your name").render()
    form = Form("/submit", "POST", f"{textbox}<br>{button}").render()

    return f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <html>
        <head><title>Home</title></head>
        <body>
            <h1>Welcome to the Custom Web Framework!</h1>
            {form}
        </body>
    </html>
    """.encode("utf-8")

@app.route("/submit", methods=["POST"])
def submit(method, headers, body):
    """Submit route."""
    username = body.get("username", [""])[0]
    return f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <html>
        <head><title>Submit</title></head>
        <body>
            <h1>Form Submitted!</h1>
            <p>Thank you, {username}!</p>
        </body>
    </html>
    """.encode("utf-8")

if __name__ == "__main__":
    app.start()