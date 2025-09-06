# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 17:50:40 2025

@author: CsArOs

To Aphra:
Thank you for devoting so much of your time to helping me with my project. 
"""



# Get the folder where the EXE or script is actually running from
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

#Find Objects.txt and EdObjctx.txt using a tkinter menu. 

objects = os.path.join(script_dir, "Objects.txt")
edobjects = os.path.join(script_dir, "EdObjts.txt")

#default lists    
default_terrains = ("Wasteland", "Highlands", "Rock", "Water", "Lava", "Subterranean", "Rough", "Swamp", "Snow", "Grass", "Sand", "Dirt")
default_categories = ("If you see this text, an error type 1 has occured!", "Towns", "Monsters", "Heroes", "Artifacts", "Treasures", "External dwellings", "Portals and Monoliths", "Garrisons", "Special terrains", "Miscallenous decorations", "IF YOU SEE THIS MESSAGE, AN ERROR TYPE 2 HAS OCURRED!")
#read selected file, line by line, creating text based on that. 

def analyse_file():
    all_lines = []
    with open(file, "r") as f:
        for line in f:
            line = line.strip()  # remove leading/trailing spaces/newlines

            #skip fake lines
            if not line or line.startswith("//"):
                continue

            #split by spaces
            sections = line.split()

            #all 9?
            if len(sections) != 9:
                print(f"Warning: Expected 9 elements, got {len(sections)} in line: {sections}")
                continue

            #assign to variables
            defname, passability, accessibility, restriction, rmg, object_id, object_sub_id, category, overground = sections

#            print(restriction)
            restricted_terrains = []

            for i in range(len(restriction)):
                if int(restriction[i]) == 0:
                    restricted_terrains.append(default_terrains[i])

            restricted_terrains_string = restricted_terrains[0]
            if len(restricted_terrains) >= 2:
                for i in range(len(restricted_terrains)-1):
                    restricted_terrains_string = restricted_terrains_string + ', '
                    restricted_terrains_string = restricted_terrains_string + restricted_terrains[i+1]
                    
#            print(restricted_terrains)
#            print(rmg)
            rmg_terrains = []

            for i in range(len(rmg)):
#                print("rmg for:")
#                print(i)
#                print(rmg[i])
#                print(default_terrains[i])
                if int(rmg[i]) == 1:
                    rmg_terrains.append(default_terrains[i])

#            print(rmg_terrains)

            if len(rmg_terrains) > 0:
                rmg_terrains_string = rmg_terrains[0]
                if len(rmg_terrains) >= 2:
                    for i in range(len(rmg_terrains)-1):
                        rmg_terrains_string = rmg_terrains_string + ', '
                        rmg_terrains_string = rmg_terrains_string + rmg_terrains[i+1]
            else:
                rmg_terrains_string = "-"

#            print(rmg_terrains) 

            name = defname[:-4]

            if int(overground) == 1:
                overground_string = "Above usual terrain"
            else:
                overground_string = "-"
            
            description = find_description(default_objects, int(object_id), int(object_sub_id))
            name, description = split_description(description)
            
            if int(category) == 0:
                category_string = rmg_terrains_string
            else:
                category_string = default_categories[int(category)]
            
            if rmg_terrains_string in ["Wasteland, Highlands, Lava, Subterranean, Rough, Swamp, Snow, Grass, Sand, Dirt"]:
                rmg_terrains_string = "All except Rock and Water"
            elif rmg_terrains_string in ["Wasteland, Highlands, Water, Lava, Subterranean, Rough, Swamp, Snow, Grass, Sand, Dirt"]:
                rmg_terrains_string = "All except Rock"
            
            if restricted_terrains_string in ["Wasteland, Highlands, Rock, Lava, Subterranean, Rough, Swamp, Snow, Grass, Sand, Dirt"]:
                restricted_terrains_string = "All except Water"

            line_string = "{{ " + name + " | " + defname + " | " + category_string + " | " + rmg_terrains_string + " | " + restricted_terrains_string + " | " + object_id + " | " + object_sub_id + " | " + overground_string + " | " + description + " }}" + "\n"

            all_lines.append(line_string)

            print(line_string)
            
            
#            with open(output_filename, "a") as f:
#                f.write(line_string)
   
#    print("Files saved into", output_filename)
    choice2 = input("Exit?")
    if choice2:
        return



def load_objects(filepath):
    objects = []
    with open(filepath, "r", encoding="utf-8") as f:
        # keep empty lines only if inside descriptions
        lines = [line.rstrip("\n") for line in f]

    i = 0
    while i < len(lines):
        # Skip empty lines outside of description blocks
        if not lines[i].strip():
            i += 1
            continue

        # Read Object_ID
        object_id = int(lines[i].strip())
        i += 1

        # Skip possible blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1

        # Read Object_sub_ID
        object_sub_id = int(lines[i].strip())
        i += 1

        # Skip possible blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1

        # Read description (starts with a quote, spans multiple lines)
        desc_lines = []
        if i < len(lines) and lines[i].startswith('"'):
            desc_lines.append(lines[i][1:])  # drop opening quote
            i += 1
            while i < len(lines) and not lines[i].endswith('"'):
                desc_lines.append(lines[i])
                i += 1
            if i < len(lines):
                desc_lines.append(lines[i][:-1])  # drop closing quote
                i += 1
        else:
            i += 1  # if description is missing, just skip

        description = "\n".join(desc_lines)
        objects.append({
            "id": object_id,
            "sub_id": object_sub_id,
            "description": description
        })

    return objects

def find_description(objects, object_id, object_sub_id):
    for obj in objects:
        if obj["id"] == object_id and (obj["sub_id"] == object_sub_id or obj["sub_id"] == -1):
            description = obj["description"]
            return description
    description = "No description"
    return description

def split_description(description):

    lines = description.split("\n")
    name = lines[0] if lines else ""
    desc = "\n".join(lines[1:]) if len(lines) > 1 else ""
    return name, desc

#print(all_lines)

#select which file to read now. 

choice = input("Input first letter of the file you want to edit: \nObjects (o) or EdObjts (e)\n")

if choice.lower() == "o":
    file = objects
else:
    file = edobjects

#output_filename = file + ".csv"

default_objects = load_objects(os.path.join(script_dir, "Object_Names.txt"))

analyse_file()


