import http.server
import socketserver

PORT = 8000
handler = http.server.SimpleHTTPRequestHandler

# Files will be served placing in the same folder
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("server started at localhost:" + str(PORT))
    httpd.serve_forever()
