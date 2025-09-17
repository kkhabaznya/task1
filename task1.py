import socket #get pc name
import getpass #get user name
import re # regex
import argparse #arguments
import os # path

parser = argparse.ArgumentParser()
parser.add_argument('-v','--vfs_path', type=str)
parser.add_argument('-b','--boot_script_path', type=str)
args = parser.parse_args()

vfs_path = args.vfs_path
boot_script_path = args.boot_script_path

user_name = getpass.getuser()
computer_name = socket.gethostname()


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
            case _:
                if(not(script_active)):
                    print("invalid command")

def ls(user_input):
    print(user_input)
    
def cd(user_input):
    print(user_input)
    
def exit_application():
    exit()

print(f"vfs_path = {vfs_path}, boot_script_path = {boot_script_path}")

if(boot_script_path != None):
    script_active = True
    script_reader(boot_script_path)
    script_active = False

command_line()
