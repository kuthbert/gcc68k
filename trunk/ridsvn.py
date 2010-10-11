# Removes SVN directories in a recursive fashion
# Hekar Khani 2008

import os

def delete_folder (folder):
    print "deleting .svn folder " + folder
    if os.name == 'nt':
        command = "rmdir /Q /S \"" + folder + "\""
        os.system (command)
    else:
        # do posix delete
		pass

def check_folder (folder):
    files = os.listdir (folder)

    if not files:
        return

    for file in files:
        if os.path.isdir (folder + os.path.sep + file):
            if file == ".svn":
                delete_folder (folder + os.path.sep + file)
            else:
                check_folder (folder + os.path.sep + file)

def main ():
    check_folder (os.getcwd ())

main ()
