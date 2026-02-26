import os

#pwd - os.getcwd()
current_path = os.getcwd()
print(f"\nCurrent working directory:\n{current_path}")

#mkdir "lab_files" - os.mkdir()
folder_name = "lab_files"
try:
    if not os.path.exists(f"{current_path}/{folder_name}"):
        os.mkdir(folder_name)
        print(f"\nNew directory created: {folder_name}")
except FileExistsError:
    print(f"Directory '{folder_name}' already exist.")

#cd - os.chdir(path)
os.chdir(folder_name)
print(f"\nMoved to new directory: {folder_name}")
current_path = os.getcwd()
print(f"\nCurrent working directory:\n{current_path}")

#touch file1.txt file2.txt file3.txt 
files_to_create = ["file1.txt", "file2.txt", "file3.txt"]
print("\nCreating files...")
for file in files_to_create:
    # os.open() has to be given an access flag (O_RDONLY, O_WRONLY, O_RDWR)
    # os.O_CREAT -> if file doesn't exist yet, create it
    # os.O_WRONLY -> specifies access mode. 
    # "write only" is the most efficient permission to request, for an empty file. 
    
    # this logic mimics "touch" command. 
    fd = os.open(file, os.O_CREAT | os.O_WRONLY) #-> "create a file so I could write to it."
    os.close(fd)
    print(f"- {file} created.")

#ls lab_files - os.listdir(path)
print(f"\nContents of '{folder_name}':")
print(os.listdir("."))

#mv file1.txt file_1.txt
if os.path.exists("file1.txt"):
    os.rename("file1.txt", "file_1.txt")
    print("\nRenamed file1.txt to file_1.txt.")

#rm -R lab_files - os.removedirs() for recursive
print(f"\nAttempting to delete files in '{folder_name}'.")
for file in os.listdir("."):
    os.remove(file) #delete each file
    print(f"- '{file}' deleted.")

os.chdir("..") 
print("\nMoving back to upper directory...")
current_path = os.getcwd()
print(f"Current working directory:\n{current_path}")

os.rmdir(folder_name) #Delete the now_empty directory
print(f"\nCleaned up: Directory '{folder_name}' and its contents have been removed.\n")