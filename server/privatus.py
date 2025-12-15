# Importing libraries
import platform
import socket
import threading, yaml

# Import scripts
from src import server, backupSystem, init, commons

# Variables
init_functions = [
    init.init,
    backupSystem.init
]

valid_os = [
    "Windows",
    "Linux"
]

# Functions
def main():
    # Check if os is valid
    if valid_os.index(platform.system()):
       return
    
    # Initialization
    for fnc in init_functions:
        fnc = fnc()
        
        if fnc.check_init():
            fnc.run() # Will return any potential errors
        else:
            continue
            
    print("Program initialized")
    
    with open(commons.get_appdatafolder() + "/data/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    configured = False
    if config != None:
        if 'server' in config:
            if 'ip' in config["server"] and 'port' in ["server"]:
                address = config["server"]["ip"]
                port = config["server"]["port"]
                configured = True
                
    if configured == False:
        address = socket.gethostbyname(socket.getfqdn())
        port = 2222 # Default port
    
    serverObject = server.Server(address, port)
    threading.Thread(target=serverObject.run).start()
    
# Main
if __name__ == "__main__":
    main()