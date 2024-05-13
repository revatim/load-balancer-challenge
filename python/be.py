import socket

class BEServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def handle_request(self, client_conn):
        try:
            with client_conn:
                data = b""
                while chunk := client_conn.recv(1024):
                    data += chunk
                    if len(chunk) < 1024:
                        # We've received the last chunk
                        break
                print(f"Server {self.port} received:\n")
                print(data)
                response = self.process_request(data)
                client_conn.sendall(response)
                print(f"Server {self.port} sent response: {response}")
        except Exception as e:
            print(f"Server {self.port} error: {e}")
        finally:
            client_conn.close()

    def process_request(self, data):
        response_body = "Hello from backend server"
        response_headers = {
            'Content-Type': 'text/plain',
            'Content-Length': len(response_body),
            'Connection': 'close',
        }
        response_headers_raw = ''.join(f'{k}: {v}\n' for k, v in response_headers.items())

        response = (
            'HTTP/1.1 200 OK\n'
            + response_headers_raw
            + '\n'
            + response_body
        )
        return response.encode('utf-8')

    def start(self):
        print(f"Server running on {self.host}:{self.port}")
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, int(self.port)))
            self.server_socket.listen()
            while True:
                client_conn, addr = self.server_socket.accept()
                self.handle_request(client_conn)
        except KeyboardInterrupt:
            print(f"Server {self.port} shutting down")
        except Exception as e:
            print(f"Server {self.port} error: {e}")
        finally:
            self.server_socket.close()
            print(f"Server {self.port} closed")
    
    def stop(self):
        print(f"Server {self.port} shutting down")
        if self.server_socket: 
            self.server_socket.close()
            print(f"Server {self.port} closed")