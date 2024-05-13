import json
import signal
import socket
import sys
from be import BEServer
from threading import Thread

HOST = 'localhost'
START_PORT = 8001

SERVER_SETUP = "./python/config.json"
servers = []

def get_instances_config():
    server_info = {}
    with open(SERVER_SETUP, encoding="utf-8") as f:
        server_info = json.load(f)
    return server_info


def start_server(host, port):
    be = BEServer(host, port)
    be.start()
    servers.append(be)

def stop_servers():
    print("Stopping all servers")
    for server in servers:
        server.stop()
    sys.exit(0)

if __name__ == "__main__":
    data = get_instances_config()        
    for server in data['server_list']:
        Thread(target=start_server, args=(server['host'], server['port'])).start()
    print("All servers started")

signal.signal(signal.SIGINT, lambda x, y: stop_servers())