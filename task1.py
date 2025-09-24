import socket #get pc name
import getpass #get user name
import re # regex
import argparse #arguments
import os # path
import csv # vfs

parser = argparse.ArgumentParser()
parser.add_argument('-v','--vfs_path', type=str)
parser.add_argument('-b','--boot_script_path', type=str)
args = parser.parse_args()

vfs_path = args.vfs_path
boot_script_path = args.boot_script_path

user_name = getpass.getuser()
computer_name = socket.gethostname()

data = []

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
            if item1["id"]==item2["id"] and item1!=item2:
                print(f"{vfs_path}@{computer_name}:~$ ",f"bad vfs, two items '{item1["name"]}' and '{item2["name"]}' share same id")
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
            case "vfs_test":
                print_subordinates(user_input)
            case _:
                if(not(script_active)):
                    print("invalid command")

def ls(user_input):
    print(user_input)
    
def cd(user_input):
    print(user_input)
    
def exit_application():
    exit()

if(vfs_path != None):
    vfs_to_memory(vfs_path)

if(boot_script_path != None):
    script_active = True
    script_reader(boot_script_path)
    script_active = False

command_line()
