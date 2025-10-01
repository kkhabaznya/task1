import socket #get pc name
import getpass #get user name
import re # regex
import argparse #arguments
import os # path
import csv # vfs
import datetime # date
import base64 # bin files

parser = argparse.ArgumentParser()
parser.add_argument('-v','--vfs_path', type=str)
parser.add_argument('-b','--boot_script_path', type=str)
args = parser.parse_args()

vfs_path = args.vfs_path
boot_script_path = args.boot_script_path

user_name = getpass.getuser()
computer_name = socket.gethostname()

data = []
active_dir = None

boot_up_time = datetime.datetime.now()

script_active = False

def command_line():
    print(f"{user_name}@{computer_name}:~$ ",end="")
    user_input = input()
    parse(user_input)
    command_line()

def script_reader(script_path):
    if (not(os.path.exists(script_path))):
        print(f"{boot_script_path}@{computer_name}:~$ ","invalid file or file does not exist")
        return 0
    with open(os.getcwd()+rf"\{script_path}") as commands:
        commands = [line.rstrip() for line in commands]
    for command in commands:
        print(f"{boot_script_path}@{computer_name}:~$ ",command)
        parse(command)

def vfs_to_memory(vfs_path):
    global data
    if (not(os.path.exists(vfs_path))):
        print(f"{vfs_path}@{computer_name}:~$ ","file does not exist")
        return 0
    file_name, file_extension = os.path.splitext(vfs_path)
    if file_extension != ".csv":
        print(f"{vfs_path}@{computer_name}:~$ ","invalid file extension")
        return 0
    with open(vfs_path,'r',encoding='UTF-8-SIG') as vfs:
        reader = csv.reader(vfs, delimiter=';')
        for row in reader:
            if len(row) >= 5:
                data.append(dict(name = row[0], id = row[1], parent = row[2], type = row[3], data = row[4]))
            else:
                print(f"{vfs_path}@{computer_name}:~$ ","invalid vfs, not enough columns to read")
                exit_application()
    for item1 in data:
        for item2 in data:
            if item1["id"]==item2["id"] and item1!=item2 or item1["parent"]==item2["parent"]=="-1" and item1!=item2:
                print(f"{vfs_path}@{computer_name}:~$ ",f"bad vfs, two items '{item1["name"]}' and '{item2["name"]}' share same id or both are root objects")
                exit_application()

def file_name(file):
    match file["type"]:
        case "dir":
            return "["+file["name"]+"] - "+file["id"]
        case _:
            return file["name"]+"."+file["type"]+" - "+file["id"]

def print_subordinates(item_id):
    if len(item_id) > 1:
        item_id = item_id[1]
    else:
        print(f"subordinates@{computer_name}:~$ error, not enough arguments")
        return 0
    for item in data:
        if item["id"] == item_id or item_id == "all":
            if item["type"] != "dir":
                print(f"subordinates@{computer_name}:~$ error, file '{file_name(item)}' type is not 'dir'")
            else:
                print(file_name(item))
                for item2 in data:
                    if item2["parent"] == item["id"]:
                        print("|---",file_name(item2))

def parse(user_input):
    user_input = re.findall(r'["][^".]+["]|[^\s]+',user_input)
    if (len(user_input) > 0):
        match user_input[0]:
            case "ls":
                ls(user_input)
            case "cd":
                cd(user_input)
            case "exit":
                exit_application()
            case "date":
                date_command()
            case "uptime":
                uptime()
            case "who":
                who()
            case "print_data":
                print_data(user_input)
            case "vfs_test":
                print_subordinates(user_input)
            case _:
                if(not(script_active)):
                    print("invalid command")

def pathfinder(user_input):
    root_object = active_dir
    
    for item in user_input:
        for item2 in data:
            if item2["parent"] == root_object and item2["name"] == item:
                root_object = item2["id"]

    return root_object

def pathmaker(user_input):
    path = []

    while user_input != "-1":
        for item in data:
            if item["id"] == user_input:
                user_input = item["parent"]
                path.append(item["name"])

    path_string = ""
    path = path[::-1]
    for item in path:
        path_string += "/"+item
        
    return path_string

def ls(user_input):
    if active_dir == None:
        print(f"ls@{computer_name}:~$ error, no vfs installed")
        return 0
    path = active_dir
    if len(user_input) > 1:
        path = user_input[1].split("/")
        for item in path:
            if item == "":
                path.remove(item)

    print_subordinates(["vfs_test",pathfinder(path)])
        
    
def cd(user_input):
    global active_dir
    if active_dir == None:
        print(f"cd@{computer_name}:~$ error, no vfs installed")
        return 0
    if (len(user_input) > 1):
        '''
        if "/" in user_input[1]:
            path = user_input[1].split("/")
            for item in path:
                if item == "":
                    path.remove(item)
            print(path)
            search_for = pathfinder(path)
            print(search_for)
            for item in data:
                if item["id"] == search_for:
                    active_dir = item["id"]
                    return 0
            print("error invalid path i guess")
            return 0
        '''
        if ".." == user_input[1]:
            for item in data:
                if item["id"] == active_dir:
                    if item["parent"] != "-1":
                        active_dir = item["parent"]
                        print(f"cd@{computer_name}:~$ success, returned to previous directory")
                        return 0
            print(f"cd@{computer_name}:~$ error, already at root directory")
            return 0
        for item in data:
            if item["parent"] == active_dir and item["name"] == user_input[1] and item["type"] == "dir":
                active_dir = item["id"]
                print(f"cd@{computer_name}:~$ success, moved to {item["name"]} directory")
                return 0
        print(f"cd@{computer_name}:~$ error, theres no directory with such name")
    else:
        print(pathmaker(active_dir))

def date_command():
    print(f"date@{computer_name}:~$",datetime.datetime.now())

def uptime():
    print(f"uptime@{computer_name}:~$",datetime.datetime.now()-boot_up_time)

def who():
    print(f"who@{computer_name}:~$ user:{user_name} computer:{computer_name}")

def print_data(user_input):
    for item in data:
        if item["id"] == user_input[1]:
            if item["type"] == "bin":
                decoded_data = base64.b64decode(item["data"]).decode("UTF-8")
                print(decoded_data)
                return 0
            print(item["data"])
            return 0
    print(f"print_data@{computer_name}:~$ error, no file was found")
    return 0

def exit_application():
    exit()

if(vfs_path != None):
    vfs_to_memory(vfs_path)
    for item in data:
        if item["parent"] == "-1":
            active_dir = item["id"]

if(boot_script_path != None):
    script_active = True
    script_reader(boot_script_path)
    script_active = False

command_line()
