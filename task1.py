import socket #get pc name
import getpass #get user name
import re # regex

user_name = getpass.getuser()
computer_name = socket.gethostname()

def command_line():
    print(f"{user_name}@{computer_name}:~$ ",end="")
    user_input = input()
    parce(user_input)
    command_line()

def parce(user_input):
    user_input = re.findall(r'[a-z]+|["][^".]+["]|[^\s]+',user_input)
    match user_input[0]:
        case "ls":
            ls(user_input)
        case "cd":
            cd(user_input)
        case "exit":
            exit_application()
        case _:
            print("invalid command")

def ls(user_input):
    print(user_input)
    
def cd(user_input):
    print(user_input)
    
def exit_application():
    exit()
    
command_line()
