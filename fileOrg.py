import os
import shutil

# ask the user for directory 
# Define the target folders 
# Create them 
# Search through the directory
# move them in their respective folders

# Ask the user for the directory to organize
directory = input("Enter the directory path to organize: ")

if not os.path.exists(directory):
    print(f"Error: Directory '{directory}' not found.")
    exit()

os.chdir(directory)


# Target Folders
target_folders = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Videos': ['.mp4', '.avi', '.mov'],
    'Audios': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar', '.tar']
}

# Create target folders (skip existing)
for folder in target_folders.keys():
    os.makedirs(folder, exist_ok=True)

for file in os.listdir(directory):
    file_path = os.path.join(directory, file) #complete file path
    if os.path.isfile(file_path):#if it is file
        _, extension = os.path.splitext(file)#take out the extension
        extension = extension.lower()
        moved = False
        for folder, extensions in target_folders.items():
            if extension in extensions:
                destination = os.path.join(directory, folder)
                shutil.copy2(file_path, destination)
                print(f"{file} moved to {folder}.")
                moved = True
                break
        if not moved:
            print(f"Ignored {file}. No matching folder for {extension}.")