# Importing libraries
import os

# Importing scripts
from src import backupSystem

# Import services here
from src.services import diary

services = [
    diary.directors
]

# Classes
class ClientInterpreter:
    
    def __init__(self, database, user, connection):
        
        # Declare class variables
        self.database = database
        self.user = user
        self.connection = connection
        
        # Track user commands
        self.user_session_commands = []
    
    def check_message(self, message):
        '''
        Filters passed parameters and executes actions based on parameters given.
        
        Status codes:
        0 for OK
        1 for Error
        '''
        
        # Check if valid format
        if message['status'] == 0:
            message = message['message'] # Reassign it to make it make more sense
            params = message['params']
            
            for service in services:
                
                for director in service:
                    if message['action'] == director[0]:
                        return director[1](params, self)

            if message['action'] == "checkStatus":
                return "OK"
            if message['action'] == "checkBackupStatus":
                # Get the data
                usedStorage = backupSystem.getUserUS(self.user)
            
            if message['action'] == "backupFile":
                # Checks
                if not 'filename' in message['params'] or not 'filesize' in message['params']:
                    return "Required parameter not given"
                
                # Values
                filename = message['params']['filename']
                filesize = message['params']['filesize']
                
                filename = os.path.basename(filename)
                # convert to integer
                filesize = int(filesize)
                # start receiving the file from the socket
                with open(filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = self.connection.recv()
                        if not bytes_read:    
                            # nothing is received file transmitting is done
                            break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        
                        # Compress the files
                        self.compressFile(filename)
                        
                        return "Backed up"
                
                return "Message error"
            
            return "Unknown action given"
        elif message['status'] == 1:
            self.connection.close()
            return "EXITED"
            
            
        return "Unknown status code"