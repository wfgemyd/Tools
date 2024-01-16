#extracts files, if a compressed file has more inside, with a recurcive apprach it is solved, but before each step, cleans the name of the file so thr OS will not rise errors

import os
import tarfile
import zipfile
#import rarfile
import tkinter as tk
from tkinter import filedialog

def select_directory():
    """UI for choosing where to extract"""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select a Folder where to extract the unzip")

def select_file():
    """UI for the compressed files"""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select a Folder with /.tar /.bz2 /.zip /.rar")

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*@~`!#$%^&*()+=;,\''
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def extract_archive(file_path, target_folder):
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                sanitized_name = sanitize_filename(member)
                target = os.path.join(target_folder, sanitized_name)
                
                if member.endswith('/'):# Check if the member is a directory
                    os.makedirs(target, exist_ok=True)
                else:
                    with open(target, "wb") as target_file:
                        with zip_ref.open(member) as source_file:
                            target_file.write(source_file.read())
                        
    elif file_path.endswith('.tar.bz2'):
        with tarfile.open(file_path, 'r:bz2') as tar_ref:
            for member in tar_ref.getmembers():
                member.name = sanitize_filename(member.name)
                tar_ref.extract(member, target_folder)
    # ADD HERE OTHER TYPES IN THE SAME STRUCTURE(.rar, etc.)
    else:
        print(f"Unsupported file format for {file_path}")



def recursive_extraction(file_path, target_folder): #here it make the rucursive extraction
    extract_archive(file_path, target_folder)
    for root, dirs, files in os.walk(target_folder):
        for name in files:
            filepath = os.path.join(root, name)
            if any(filepath.endswith(ext) for ext in ['.zip', '.tar.bz2', '.rar']):
                nested_target_folder = os.path.join(root, sanitize_filename(os.path.splitext(name)[0]))
                os.makedirs(nested_target_folder, exist_ok=True)
                recursive_extraction(filepath, nested_target_folder)

def main():
    hledane_slovo = input("source folder with zip tar bz2")
    zakazane_slovo = input("target folder")
    sucesfullextraction = 0

    source_folder= select_file()
    target_folder = select_directory()
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)
        if (not (zakazane_slovo in file_path and hledane_slovo in file_path)) or (hledane_slovo == "" or zakazane_slovo == ""):
            if os.path.isfile(file_path) and (file.endswith('.tar.bz2') or file.endswith('.zip') or file.endswith('.rar') ):
                folder_name = sanitize_filename(os.path.splitext(file)[0])
                extracted_folder = os.path.join(target_folder, folder_name)
                os.makedirs(extracted_folder, exist_ok=True)
                recursive_extraction(file_path, extracted_folder)
                sucesfullextraction += 1

    print("Amount of successful exports: " + str(sucesfullextraction))

main()

