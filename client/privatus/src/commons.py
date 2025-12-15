'''
This file contains commonly used functions 
'''

# Importing libraries
import platform
import os

# Functions
def call_with_args(python_file_dist, args):
    command = "python " + python_file_dist
    
    for arg in args:
       command = command + " " + arg 
    
    os.system(command)
    
def refine_path(path):
    char_count = 0
    refined_path = ""
    
    for char in path:
        char_count += 1
        
        if char_count != len(path):
            refined_path = refined_path + char
        else:
            if char != "/":
                refined_path = refined_path + char
            
    return refined_path
    
def move_back(path):
    
    path = path.split("\\")
    new_path = ""
    
    count = 0
    for directory in path:
        count += 1
        if count != len(path):
            new_path += (directory + "/")
            
    return refine_path(new_path)

def get_appdatafolder():
    currentOs = platform.system()
    
    if currentOs == "Windows":
        return os.getenv('APPDATA') + "/.privatus-client"
    if currentOs == "Linux":
        return os.path.expanduser('~') +  + "/.privatus-client"

def check_array(array, value):
    for i in array:
        if i == value:
            return True
        
    return False

def check_dict(dict, key, value):
    for x, y in dict.items():
        if x == key:
            if y == value:
                return True
            
            
    return False