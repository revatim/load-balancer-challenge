import signal
import socket
from threading import Thread
from be import BEServer
from start_be_servers import get_instances_config

HOST = 'localhost'
PORT = 5432

# Get List of Servers from start_be_servers.py
servers = []

def get_servers_list():
    instances_data = get_instances_config()
    global servers
    servers = [BEServer(HOST, server['port']) for server in instances_data['server_list']]
    print(f"LB: {len(servers)} backend servers setup")

def forward_request(client_conn, be):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as be_sock:
            print(f"LB: Sending request to {be.port}")
            be_sock.connect((be.host, int(be.port)))

            # Forward the client's request to the backend server
            while chunk := client_conn.recv(1024):
                be_sock.sendall(chunk)
                if len(chunk) < 1024:
                    # We've received the last chunk
                    break

            while chunk := be_sock.recv(1024):
                client_conn.sendall(chunk)
                if len(chunk) < 1024:
                    # We've received the last chunk
                    break
            
            print(f"LB: Response forwarded from {be.port}")
    except Exception as e:
        print(f"LB: Error forwarding request to {be.port}: {e}")


def main():
    get_servers_list()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(100)
        print(f"LB: Listening on port {PORT}")

        try:
            while True:
                client_conn, client_addr = sock.accept()
                print(f"LB: Received Request From {client_addr}")

                # Round-robin scheduling
                be = servers.pop(0)
                servers.append(be)
                
                lb_thread = Thread(target=forward_request, args=(client_conn, be))
                lb_thread.start()
        except KeyboardInterrupt:
            print("LB: Shutting down")
        except Exception as e:
            print(f"LB: Error: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    main()

# signal.signal(signal.SIGINT, lambda x, y: ())