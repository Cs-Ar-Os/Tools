# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:14:07 2026

@author: CsArOs
"""

import sys, os, time
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.withdraw()

def get_file_list(directory = None): #copied from install_PP
    if directory == None:    
        directory = folder_path
    
    file_list = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            file_list.append(os.path.join(dirpath, f))
    return file_list

def find_input(path, key, encoding = 'ascii'):
    key_bytes = key.encode(encoding)
    instances = []
    with open(path, 'rb') as f:
        data = f.read()
        index = data.find(key_bytes)
        while index != -1:
            instances.append(index)
            index = data.find(key_bytes, index + 1)
    return instances

folder_path = filedialog.askdirectory(
    title="Select the folder with desired json files",
)
if not folder_path:
    messagebox.showerror("ERROR", "Incorrect path. No file selected.")
    sys.exit()
    
file_list = get_file_list(folder_path)



def main():
    phrase = input("What phrase are we looking for?\n")
    
    print("\n")
    
    for file_path in file_list:
        instances = find_input(file_path, phrase, encoding = 'utf-8')
        if (not (instances is None)) and len(instances) > 0:
            for case in instances:
                print(f"Phrase exists in file {file_path} at offset {case}")
            print("\n")
    
    print("That's all she wrote")


while True:
    if file_list == None:
        folder_path = filedialog.askdirectory(
            title="Select the folder with desired files",
        )
        file_list = get_file_list(folder_path)
    main()
    exit_choice = input("Do you want to use the tool again? Y/N  ")
    if not exit_choice.lower() in ["y", "yes", "true", "tak"]:
        time.sleep(3)
        exit()
        break
    repeat_choice = input("Do you want to edit the same files again? Y/N  ")
    if repeat_choice.lower() in ["n", "no", "false", "nope"]:
        file_list == None
        continue        

exit()