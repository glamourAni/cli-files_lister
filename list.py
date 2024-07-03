import os
import pwd
import grp
from termcolor import colored
from prettytable import PrettyTable
from fire import Fire
from time import ctime

def get_permissions(path):
    if os.path.isdir(path):
        access = "d"
    elif os.path.islink(path):
        access = "l"
    else:
        access = "-"

    if os.access(path, os.R_OK):
        access += "r"
    else:
        access += "-"
    if os.access(path, os.W_OK):
        access += "w"
    else:
        access += "-"
    if os.access(path, os.X_OK):
        access += "x"
    else:
        access += "-"

    return access
# pad cells if orignal colummns are of unequal length
# def fill_cells_with_spaces(*columns):
    max_len = max(len(col) for col in columns)
    for col in columns: col.extend([' '] * (max_len - len(col)))

def list_files(path=os.getcwd(), all=False, directories=False, long=False):
    """List files and directories alphabetically, in tabular form.
    
    Options:
    path - indicates the current working directory
    all - include hidden files and directories.
    directories - list directories themselves and not their contents.
    long - use a long listing format

    """
    cwd_contents = sorted(os.listdir(path))
    files = [f for f in cwd_contents if not os.path.isdir(os.path.join(path, f))]
    table = PrettyTable()
    table.field_names = ["Files/Directories"]
    
    
    if not all:
        #ignore hidden files unless specified with --all
        cwd_contents = [file for file in cwd_contents if not file.startswith(".")]

    #list files and directories together if --d isn't specified
    if not directories:   
        for file in cwd_contents:
            if os.path.isdir(os.path.join(path, file)):
                file = colored(file, 'blue', attrs=['bold'])
            table.add_row([file])

    #list directories alone
    else:
        table.field_names = ["Directories"]
        dirs = [colored(d, 'blue', attrs=['bold']) for d in cwd_contents if os.path.isdir(os.path.join(path, d))]
        for d in dirs:
            table.add_row([d])
    #long listing
    if long:
        
        permissions = []
        links = []
        size = []
        uid = []
        gid = []
        date_of_modification = []

        for file in cwd_contents:
            file_path = os.path.join(path, file)
            file_info = os.lstat(file_path)

            #store mode access
            permissions.append(get_permissions(file_path))

            #store number of links
            links.append(file_info.st_nlink)
            
            #store size in bytes
            size.append(file_info.st_size)

            #store uid
            uid.append(pwd.getpwuid(file_info.st_uid)[0])

            #store gid
            gid.append(grp.getgrgid(file_info.st_gid)[0])

            #store modification time
            date_of_modification.append(ctime(file_info.st_mtime))

        fill_cells_with_spaces(permissions, links, size, uid, gid, date_of_modification)
        columns = {"Permission": permissions, 
                   "No. of links": links, 
                   "Size": size,
                   "UID": uid, 
                   "GID": gid, 
                   "Last Modified": date_of_modification}
        for col in columns:
            table.add_column(col, columns[col])

    print(table)
if __name__ == "__main__":
        Fire(list_files)
