# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:07:01 2026

@author: CsArOs
"""

import csv, json, os, sys

def fix_numbers(value):
    if len(str(value)) > 0:# and value.startswith("$"):
        new_value = value#.replace("$", "").strip()
        try:
            new_value = int(new_value)
        except Exception:
            try:
                new_value = float(new_value)
            except Exception:
                pass
        value = new_value
    return value

def try_parse_embedded_json(value):
    # (Kept identical to your working version)
    if not isinstance(value, str):
        return value    
    value = value.replace("|",",")
    new_value = value.strip()
    if not (new_value.startswith('{') or new_value.startswith('[')):
        return new_value
    normalized_value = new_value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
    try:
        return json.loads(normalized_value)
    except json.JSONDecodeError:
        try:
            if normalized_value.startswith('{') and not normalized_value.endswith('}'):
                return json.loads(normalized_value + '}')
        except json.JSONDecodeError:
            pass
        try:
            if normalized_value.endswith('{') and not normalized_value.startswith('}'):
                return json.loads('{' + normalized_value)
        except json.JSONDecodeError:
            pass
        return new_value


#Key function
def csv_reader(headers, row):
    root = {}
    stack = [root]

    i = 0
    while i < len(headers):
        header = headers[i].strip()
        value = row[i] if i < len(row) else ""
        value = str(value).strip()
        value = try_parse_embedded_json(value)
        value = fix_numbers(value)
        #First two columns are irrelevant
        if i < 2:
            i += 1
            continue

        #Skip empty dynamic blocks
        if header.startswith("_") and value == "":
            while i < len(headers):
                h_check = headers[i].strip()
                if h_check.endswith(">") or h_check.endswith("]"):
                    break
                i += 1
            i += 1
            continue

        #DYNAMIC KEYS
        if header.startswith("_"):
            if i + 1 < len(headers):
                next_header = headers[i + 1].strip()
                #A: The dynamic key opens a nested object (e.g., _BONUS1 followed by <type)
                if next_header.startswith("<"):
                    new_obj = {}
                    if isinstance(stack[-1], list):
                        stack[-1].append(new_obj)
                    else:
                        stack[-1][value] = new_obj
                    stack.append(new_obj)
                    i += 1
                    continue
                #B: The dynamic key opens an array (f.e., _KEY followed by [items)
                elif next_header.startswith("["):
                    new_arr = []
                    if isinstance(stack[-1], list):
                        stack[-1].append(new_arr)
                    else:
                        stack[-1][value] = new_arr
                    stack.append(new_arr)
                    i += 1
                    continue
                #C: Standard dynamic key-value pair, (such as _BONUS1 bonus_1_content)
                else:
                    next_val = row[i + 1] if i + 1 < len(row) else ""
                    next_val = fix_numbers(str(next_val).strip())
                    next_val = try_parse_embedded_json(next_val)
                    
                    if value != "" and next_val != "":
                        if isinstance(stack[-1], dict):
                            stack[-1][value] = next_val
                        elif isinstance(stack[-1], list):
                            stack[-1].append({value: next_val})
                    i += 2
                    continue
        
        #Bracket start Closed
        if header.startswith(">") or header.startswith("]"):
            if len(stack) > 1:
                stack.pop()
            header = header[1:].strip()

        if header == "":
            i += 1
            continue

        #Bracket start Open
        if header.startswith("<"):
            if isinstance(stack[-1], list):
                new_obj = {}
                stack[-1].append(new_obj)
                stack.append(new_obj)
            header = header[1:].strip()
        elif header.startswith("["):
            if isinstance(stack[-1], list):
                new_arr = []
                stack[-1].append(new_arr)
                stack.append(new_arr)
            header = header[1:].strip()

        should_pop_after = False
        
        #Bracket end Open
        if header.endswith("<"):
            key = header[:-1].strip()
            new_obj = {}
            if isinstance(stack[-1], list):
                stack[-1].append(new_obj)
            else:
                stack[-1][key] = new_obj
            stack.append(new_obj)
            header = key
            
        elif header.endswith("["):
            key = header[:-1].strip()
            new_arr = []
            if isinstance(stack[-1], list):
                stack[-1].append(new_arr)
            else:
                stack[-1][key] = new_arr
            stack.append(new_arr)
            header = key
            
        #Bracket end closed
        elif header.endswith(">") or header.endswith("]"):
            header = header[:-1].strip()
            should_pop_after = True

        #Write data
        if value != "" and header != "":
            if isinstance(stack[-1], dict):
                stack[-1][header] = value
            elif isinstance(stack[-1], list):
                stack[-1].append(value)

        #Pop and clean
        if should_pop_after:
            if len(stack) > 1:
                popped = stack.pop()
                if not popped:  #Clean up empty containers if no data was used
                    parent = stack[-1]
                    if isinstance(parent, list):
                        parent.pop()
                    elif isinstance(parent, dict):
                        keys_to_delete = [k for k, v in parent.items() if v is popped]
                        for k in keys_to_delete:
                            del parent[k]

        i += 1

    return root



def _initiate_CSV_TO_JSON(file_path):
    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
    
        headers = next(reader)
    
        for row in reader:
            json_name = row[0]
            
            if len(str(json_name)) > 2 and not json_name in [""]:                
                json_name = json_name + ".json"
                root_header = row[1]
                content = csv_reader(headers, row)
    
                final_json = {
                    root_header: content
                }
        
                json_path = os.path.join(os.path.dirname(file_path), json_name)
        
                with open(json_path, "w", encoding="utf-8") as out:
                    json.dump(final_json, out, indent=4)
                    print("succesfully saved the JSON file: ", json_name)
                
                
def JSON_reader():
    return

def _initiate_JSON_to_CSV(file_path):
    return
    

#Opening the file
from tkinter import filedialog, messagebox


def main():
    if len(sys.argv) < 2:
        file_path = filedialog.askopenfilename(
            title="Select the data file",
            filetypes=[("CSV files", "*.csv"),("JSON files", "*.json")]
        )
        if not file_path:
            messagebox.showerror("ERROR", "Incorrect path. No file selected.")
            sys.exit()
    
    else: 
        file_path = sys.argv[1]
    
    print(file_path)
    
    if file_path.lower().endswith(".csv"):
        _initiate_CSV_TO_JSON(file_path)
    elif file_path.lower().endswith(".json"):
        _initiate_JSON_to_CSV(file_path)
    else:
        messagebox.showerror("ERROR", "Selected file is neither a CSV, nor a JSON file.")
        sys.exit()

if __name__ == "__main__":
    main()











