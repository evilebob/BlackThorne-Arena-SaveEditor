import json
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys
import copy

# Define SkillSet options as a dictionary
skill_set_options = {
    0: "none",
    1: "fighter",
    2: "commander",
    3: "defender",
    4: "duelist",
    5: "rogue",
    6: "ranger",
    7: "berserker",
    8: "marksman",
    9: "battlemonk",
    10: "ronin",
    11: "shapeshifter",
    12: "bard",
    13: "yanguansword",
    101: "fire",
    102: "ice",
    103: "lightning",
    104: "white",
    105: "black",
    106: "air",
    107: "spirit",
    108: "necromancy",
    109: "blood",
    110: "forest",
    111: "earth",
    200: "unarmed",
    201: "onehand",
    202: "twohand",
    203: "shield",
    204: "range",
    205: "dual",
    206: "polearms"
}

# Hard-coded neutral state (from the provided savegame for 1duke)
NEUTRAL_STATE = {
    "currCmd": {
        "cmdName": 4,
        "targetID": -1,
        "targetName": "street3",
        "targetPosition": {"x": 0.0, "y": 0.0, "z": 0.0},
        "bsd": {
            "name": None,
            "type": 0,
            "id": 0,
            "during": {"Max": 60.0, "Min": 15.0, "Base": 0.0, "Type": 1},
            "canLoop": False,
            "randomRate": 0,
            "nextBehavior": None,
            "idlePointName": None,
            "wanderStyle": 1,
            "wanderRange": 0.0,
            "wanderPointName": None,
            "trainPointName": None,
            "trainTargetName": None,
            "workStreetName": None,
            "stackNum": 0,
            "destoryItem": False,
            "destoryTime": 0.0,
            "workStreetIndex": 0,
            "attraction": 0,
            "peddlePointName": None,
            "attractionPoints": [],
            "staytime": None,
            "patrolStyle": 0,
            "patrolStreetName": None,
            "patrolStreetIndex": 0,
            "patrolRandomStreet": False,
            "exploreStartPointName": None,
            "exploreEndPointName": None,
            "prepareClip": None,
            "clips": [],
            "gaptime": None,
            "loopGapTime": None,
            "isHideWeapon": False,
            "randomPlay": False,
            "onlyOneAction": False,
            "interactPointName": None,
            "interactTargetName": None
        },
        "spellInfoId": -1,
        "stringParam": None,
        "intParam": 0,
        "floatParam": 0.0,
        "isUnitTarget": False
    },
    "tempCmd": {
        "cmdName": 10,
        "targetID": -1,
        "targetName": "street3",
        "targetPosition": {"x": 0.0, "y": 0.0, "z": 0.0},
        "bsd": {
            "name": None,
            "type": 0,
            "id": 0,
            "during": {"Max": 60.0, "Min": 15.0, "Base": 0.0, "Type": 1},
            "canLoop": False,
            "randomRate": 0,
            "nextBehavior": None,
            "idlePointName": None,
            "wanderStyle": 1,
            "wanderRange": 0.0,
            "wanderPointName": None,
            "trainPointName": None,
            "trainTargetName": None,
            "workStreetName": None,
            "stackNum": 0,
            "destoryItem": False,
            "destoryTime": 0.0,
            "workStreetIndex": 0,
            "attraction": 0,
            "peddlePointName": None,
            "attractionPoints": [],
            "staytime": None,
            "patrolStyle": 0,
            "patrolStreetName": None,
            "patrolStreetIndex": 0,
            "patrolRandomStreet": False,
            "exploreStartPointName": None,
            "exploreEndPointName": None,
            "prepareClip": None,
            "clips": [],
            "gaptime": None,
            "loopGapTime": None,
            "isHideWeapon": False,
            "randomPlay": False,
            "onlyOneAction": False,
            "interactPointName": None,
            "interactTargetName": None
        },
        "spellInfoId": -1,
        "stringParam": None,
        "intParam": 0,
        "floatParam": 0.0,
        "isUnitTarget": False
    },
    "defaultstate": 0,
    "cstate": 0,
    "tstate": 9
}

# Helper function to remove an NPC id from any match arrays in an object.
def remove_npc_from_matches_in_obj(obj, npc_id):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ["memberIds", "candidateIds"] and isinstance(value, list):
                obj[key] = [x for x in value if x != npc_id]
            else:
                remove_npc_from_matches_in_obj(value, npc_id)
    elif isinstance(obj, list):
        for item in obj:
            remove_npc_from_matches_in_obj(item, npc_id)

# Scans all arenas and removes the npc_id from match arrays.
def remove_npc_from_arena_matches(npc_id):
    for arena in savegame_data.get("arenas", []):
        remove_npc_from_matches_in_obj(arena, npc_id)

# Function to load savegame data
def load_savegame(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"Loaded {len(data.get('npcs', []))} NPCs from the savegame.")
        return data
    except FileNotFoundError:
        print(f"Savegame file not found: {file_path}")
        messagebox.showerror("Error", f"Savegame file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON. Make sure the savegame file is valid.")
        messagebox.showerror("Error", "Error decoding JSON. Make sure the savegame file is valid.")
        return None

# Function to save the modified savegame data back to file with unique backup naming
def save_savegame(file_path, savegame_data):
    backup_path = file_path + ".backup"
    if os.path.exists(backup_path):
        i = 1
        while True:
            new_backup_path = f"{file_path}.backup{i}"
            if not os.path.exists(new_backup_path):
                backup_path = new_backup_path
                break
            i += 1
    try:
        os.rename(file_path, backup_path)
        print(f"Backup created at {backup_path}")
        with open(file_path, 'w') as file:
            json.dump(savegame_data, file, separators=(',', ':'), sort_keys=False)
        print(f"Savegame updated successfully at {file_path}")
        messagebox.showinfo("Success", f"Savegame updated successfully.\nBackup created at {backup_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")

# Function to extract NPC names using 'unitname'
def get_npc_name(npc):
    return npc.get('unitname', 'Unnamed NPC')

# Modified build_tree function to include keys in leaf nodes
def build_tree(parent, data, parent_path="", tree_widget=None, key=None):
    if tree_widget is None:
        return
    if isinstance(data, dict):
        for k, value in data.items():
            display_text = f"{k}"
            new_path = f"{parent_path}/{k}"
            node = tree_widget.insert(parent, "end", text=display_text, open=False, values=[new_path])
            build_tree(node, value, new_path, tree_widget, key=k)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            name = get_npc_name(value) if isinstance(value, dict) else ''
            display_text = f"[{index}] {name}" if name else f"[{index}]"
            new_path = f"{parent_path}/{index}"
            node = tree_widget.insert(parent, "end", text=display_text, open=False, values=[new_path])
            build_tree(node, value, new_path, tree_widget)
    else:
        if key is not None:
            display_text = f"{key}: {data}"
        else:
            display_text = f"{data}"
        tree_widget.insert(parent, "end", text=display_text, values=[parent_path])

# New helper functions for search filtering
def node_matches(key, value, query):
    query = query.lower()
    if query in str(key).lower():
        return True
    if not isinstance(value, (dict, list)):
        return query in str(value).lower()
    return False

def descendant_matches(data, query):
    query = query.lower()
    if isinstance(data, dict):
        for k, v in data.items():
            if query in str(k).lower():
                return True
            if not isinstance(v, (dict, list)) and query in str(v).lower():
                return True
            if descendant_matches(v, query):
                return True
    elif isinstance(data, list):
        for item in data:
            if not isinstance(item, (dict, list)) and query in str(item).lower():
                return True
            if descendant_matches(item, query):
                return True
    return False

def build_filtered_tree(parent, data, parent_path, tree_widget, query, key=None):
    if isinstance(data, dict):
        for k, value in data.items():
            new_path = f"{parent_path}/{k}" if parent_path else f"/{k}"
            if node_matches(k, value, query) or descendant_matches(value, query):
                node = tree_widget.insert(parent, "end", text=k, open=True, values=[new_path])
                build_filtered_tree(node, value, new_path, tree_widget, query, key=k)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = f"{parent_path}/{index}" if parent_path else f"/{index}"
            display_text = f"[{index}]"
            if isinstance(value, dict):
                name = get_npc_name(value)
                if name:
                    display_text += f" {name}"
            if node_matches("", value, query) or descendant_matches(value, query):
                node = tree_widget.insert(parent, "end", text=display_text, open=True, values=[new_path])
                build_filtered_tree(node, value, new_path, tree_widget, query)
    else:
        text = f"{key}: {data}" if key is not None else f"{data}"
        if query.lower() in text.lower():
            tree_widget.insert(parent, "end", text=text, values=[parent_path])

def update_filter(query):
    tree.delete(*tree.get_children())
    if query.strip() == "":
         build_tree("", savegame_data, tree_widget=tree)
    else:
         build_filtered_tree("", savegame_data, "", tree_widget=tree, query=query)

# Function to display NPC tree for team 0, excluding "Arena Guard"
def display_npc_tree_team_0():
    global team_0_tree
    units = [(index, npc) for index, npc in enumerate(savegame_data.get('npcs', []))
             if npc.get('team') == 0 and npc.get('unitname') != 'Arena Guard']
    if not units:
        messagebox.showerror("Error", "No NPCs on team 0 found in the savegame (excluding 'Arena Guard').")
        return
    units.sort(key=lambda x: (x[0], x[1].get('unitname', '')))
    team_0_window = tk.Toplevel(root)
    team_0_window.title("NPCs on Team 0 (Excluding 'Arena Guard')")
    team_0_window.geometry("800x600")
    team_0_tree = ttk.Treeview(team_0_window, columns=("Path",), show="tree headings")
    team_0_tree.heading("#0", text="NPC (Index and Name)")
    team_0_tree.heading("Path", text="Path")
    team_0_tree.column("#0", width=400)
    team_0_tree.column("Path", width=400)
    team_0_tree.pack(fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(team_0_window, orient="vertical", command=team_0_tree.yview)
    team_0_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    team_0_tree.bind("<Double-1>", lambda event: on_tree_select(event, team_0_tree))
    for index, npc in units:
        unitname = get_npc_name(npc)
        unit_path = f"/npcs/{index}"
        display_text = f"[{index}] {unitname}"
        npc_item = team_0_tree.insert("", "end", text=display_text, open=False, values=[unit_path])
        build_tree(npc_item, npc, parent_path=unit_path, tree_widget=team_0_tree)

# Function to display NPCs on team 0 with only 'hitable' attribute, excluding "Arena Guard"
def display_hitable_attributes_team_0():
    units = [(index, npc) for index, npc in enumerate(savegame_data.get('npcs', []))
             if npc.get('team') == 0 and npc.get('unitname') != 'Arena Guard']
    if not units:
        messagebox.showerror("Error", "No NPCs on team 0 found in the savegame (excluding 'Arena Guard').")
        return
    units.sort(key=lambda x: (x[0], x[1].get('unitname', '')))
    hitable_window = tk.Toplevel(root)
    hitable_window.title("Hitable Attributes of NPCs on Team 0 (Excluding 'Arena Guard')")
    hitable_window.geometry("600x400")
    hitable_tree = ttk.Treeview(hitable_window, columns=("NPC", "Path", "Hitable"), show="headings")
    hitable_tree.heading("#1", text="NPC")
    hitable_tree.heading("#2", text="Path")
    hitable_tree.heading("#3", text="Hitable")
    hitable_tree.column("#1", width=200)
    hitable_tree.column("#2", width=200)
    hitable_tree.column("#3", width=100)
    hitable_tree.pack(fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(hitable_window, orient="vertical", command=hitable_tree.yview)
    hitable_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    hitable_tree.bind("<Double-1>", lambda event: on_hitable_edit(event, hitable_tree))
    for index, npc in units:
        unitname = get_npc_name(npc)
        unit_path = f"/npcs/{index}/hitable"
        hitable_value = npc.get('hitable', False)
        if not isinstance(hitable_value, bool):
            if isinstance(hitable_value, str):
                hitable_value = hitable_value.lower() in ['true', 'yes', '1']
            elif isinstance(hitable_value, (int, float)):
                hitable_value = bool(hitable_value)
            else:
                hitable_value = False
            savegame_data['npcs'][index]['hitable'] = hitable_value
        hitable_tree.insert("", "end", values=(unitname, unit_path, hitable_value))

# Generic function to view any attribute in the savegame
def view_attribute(savegame_data, attribute_path):
    keys = attribute_path.strip('/').split('/')
    current_data = savegame_data
    for key in keys:
        if key.isdigit():
            key = int(key)
            if isinstance(current_data, list) and key < len(current_data):
                current_data = current_data[key]
            else:
                return None
        elif isinstance(current_data, dict):
            current_data = current_data.get(key, None)
        else:
            return None
        if current_data is None:
            return None
    return current_data

# Function to handle double-click events on the tree
def on_tree_select(event, tree_widget=None):
    try:
        if tree_widget is None:
            tree_widget = event.widget
        selected_item = tree_widget.focus()
        if not selected_item:
            return
        path = tree_widget.item(selected_item, "values")[0]
        attribute = tree_widget.item(selected_item, "text").split(":")[0]
        current_value = view_attribute(savegame_data, path)
        if current_value is None:
            messagebox.showerror("Error", f"Attribute '{attribute}' not found at path '{path}'.")
            return
        if attribute == "humanTalent" and isinstance(current_value, dict):
            new_value = simpledialog.askinteger("Edit humanTalent", f"Enter new value for all humanTalent properties (0-10):", minvalue=0, maxvalue=10)
            if new_value is None:
                return
            for sub_attr in current_value:
                current_value[sub_attr] = new_value
            tree_widget.delete(*tree_widget.get_children(selected_item))
            build_tree(selected_item, current_value, parent_path=path, tree_widget=tree_widget)
            messagebox.showinfo("Success", f"All humanTalent properties updated to {new_value}.")
            return
        if path.endswith("/skillSet"):
            parts = path.strip('/').split('/')
            if len(parts) >= 3:
                npc_index = int(parts[1])
                skill_set = savegame_data['npcs'][npc_index].get('skillSet', [])
                edit_skill_set(npc_index, skill_set, tree_widget, selected_item)
            else:
                messagebox.showerror("Error", "Invalid path for 'skillSet'.")
            return
        if "/skillSet/" in path:
            parts = path.strip('/').split('/')
            if len(parts) >= 4:
                npc_index = int(parts[1])
                skill_index = int(parts[3])
                current_skill = savegame_data['npcs'][npc_index]['skillSet'][skill_index]
                edit_individual_skill(npc_index, skill_index, current_skill, tree_widget, selected_item)
            else:
                messagebox.showerror("Error", "Invalid path for individual skill.")
            return
        if path.endswith("/gladiators"):
            parts = path.strip('/').split('/')
            if len(parts) >= 3:
                try:
                    arena_index = int(parts[1])
                except ValueError:
                    messagebox.showerror("Error", "Invalid arena index in path.")
                    return
                gladiators_list = savegame_data["arenas"][arena_index].get("gladiators", [])
                edit_gladiators(arena_index, gladiators_list, tree_widget, selected_item)
            else:
                messagebox.showerror("Error", "Invalid path for 'gladiators'.")
            return
        if isinstance(current_value, bool):
            new_value = messagebox.askyesno("Edit Attribute", f"Set '{attribute}' to True?")
            if new_value is None:
                return
            new_value_converted = new_value
        elif isinstance(current_value, int):
            new_value_str = simpledialog.askstring("Edit Attribute", f"Current value of '{attribute}': {current_value}\nEnter new integer value:")
            if new_value_str is None:
                return
            try:
                new_value_converted = int(new_value_str)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.")
                return
        else:
            new_value_str = simpledialog.askstring("Edit Attribute", f"Current value of '{attribute}': {current_value}\nEnter new value:")
            if new_value_str is None:
                return
            new_value_converted = new_value_str
        keys = path.strip('/').split('/')
        current = savegame_data
        for key in keys[:-1]:
            if key.isdigit():
                key = int(key)
                if isinstance(current, list) and key < len(current):
                    current = current[key]
                else:
                    messagebox.showerror("Error", f"Invalid path segment '{key}'.")
                    return
            elif isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    messagebox.showerror("Error", f"Key '{key}' not found.")
                    return
            else:
                messagebox.showerror("Error", f"Cannot traverse through non-dict/list object at '{key}'.")
                return
        last_key = keys[-1]
        if last_key.isdigit():
            last_key = int(last_key)
            if isinstance(current, list):
                if last_key < len(current):
                    current[last_key] = new_value_converted
                else:
                    messagebox.showerror("Error", f"Index '{last_key}' out of range.")
                    return
        elif isinstance(current, dict):
            current[last_key] = new_value_converted
        else:
            messagebox.showerror("Error", f"Cannot set value on non-dict/list object at '{last_key}'.")
            return
        if isinstance(new_value_converted, bool):
            display_text = f"{attribute}: {str(new_value_converted)}"
        else:
            display_text = f"{attribute}: {new_value_converted}"
        tree_widget.item(selected_item, text=display_text)
    except KeyError as e:
        messagebox.showerror("Key Error", f"KeyError: {e} at path '{path}'.")
    except IndexError as e:
        messagebox.showerror("Index Error", f"IndexError: {e} at path '{path}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to handle double-click events specifically for 'hitable' attribute in the new window
def on_hitable_edit(event, tree_widget=None):
    try:
        if tree_widget is None:
            tree_widget = event.widget
        selected_item = tree_widget.focus()
        if not selected_item:
            return
        values = tree_widget.item(selected_item, "values")
        if len(values) < 3:
            messagebox.showerror("Error", "Insufficient data to edit 'hitable' attribute.")
            return
        unitname, path, hitable_value = values
        if isinstance(hitable_value, bool):
            current_value = hitable_value
        elif isinstance(hitable_value, str):
            current_value = hitable_value.lower() in ['true', 'yes', '1']
        elif isinstance(hitable_value, (int, float)):
            current_value = bool(hitable_value)
        else:
            current_value = False
        new_value = not current_value
        keys = path.strip('/').split('/')
        current = savegame_data
        for key in keys[:-1]:
            if key.isdigit():
                key = int(key)
                if isinstance(current, list) and key < len(current):
                    current = current[key]
                else:
                    messagebox.showerror("Error", f"Invalid path segment '{key}'.")
                    return
            elif isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    messagebox.showerror("Error", f"Key '{key}' not found.")
                    return
            else:
                messagebox.showerror("Error", f"Cannot traverse through non-dict/list object at '{key}'.")
                return
        last_key = keys[-1]
        if last_key.isdigit():
            last_key = int(last_key)
            if isinstance(current, list):
                if last_key < len(current):
                    current[last_key] = new_value
                else:
                    messagebox.showerror("Error", f"Index '{last_key}' out of range.")
                    return
        elif isinstance(current, dict):
            current[last_key] = new_value
        else:
            messagebox.showerror("Error", f"Cannot set value on non-dict/list object at '{last_key}'.")
            return
        tree_widget.item(selected_item, values=(unitname, path, new_value))
    except KeyError as e:
        messagebox.showerror("Key Error", f"KeyError: {e} at path '{path}'.")
    except IndexError as e:
        messagebox.showerror("Index Error", f"IndexError: {e} at path '{path}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to edit individual skill
def edit_individual_skill(npc_index, skill_index, current_skill, tree_widget, selected_item):
    try:
        current_skill_name = skill_set_options.get(current_skill, f"Unknown ({current_skill})")
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Skill")
        edit_window.geometry("300x200")
        ttk.Label(edit_window, text=f"Current Skill: {current_skill_name}").pack(pady=10)
        ttk.Label(edit_window, text="Select New Skill:").pack(pady=5)
        selected_skill = tk.StringVar()
        skill_dropdown = ttk.Combobox(edit_window, textvariable=selected_skill, state="readonly")
        dropdown_values = [f"{k}: {v}" for k, v in skill_set_options.items()]
        skill_dropdown['values'] = dropdown_values
        skill_dropdown.pack(pady=5)
        def confirm_edit():
            new_skill_display = selected_skill.get()
            if not new_skill_display:
                messagebox.showerror("Error", "Please select a skill.")
                return
            try:
                new_skill_code_str, _ = new_skill_display.split(": ", 1)
                new_skill_code = int(new_skill_code_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid skill format selected.")
                return
            if new_skill_code in savegame_data['npcs'][npc_index]['skillSet']:
                messagebox.showerror("Error", "Skill already exists in skillSet.")
                return
            savegame_data['npcs'][npc_index]['skillSet'][skill_index] = new_skill_code
            tree_widget.item(selected_item, text=new_skill_display)
            messagebox.showinfo("Success", "Skill updated successfully.")
            edit_window.destroy()
        confirm_button = ttk.Button(edit_window, text="Update Skill", command=confirm_edit)
        confirm_button.pack(pady=10)
        cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.pack()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to edit skill set
def edit_skill_set(npc_index, skill_set, tree_widget, parent_item):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Skill Set")
    edit_window.geometry("400x300")
    skills_listbox = tk.Listbox(edit_window, selectmode=tk.SINGLE)
    for skill in skill_set:
        skill_name = skill_set_options.get(skill, f"Unknown ({skill})")
        skills_listbox.insert(tk.END, skill_name)
    skills_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
    button_frame = ttk.Frame(edit_window)
    button_frame.pack(pady=5)
    def add_skill():
        add_window = tk.Toplevel(edit_window)
        add_window.title("Add Skill")
        add_window.geometry("300x200")
        ttk.Label(add_window, text="Select Skill:").pack(pady=10)
        selected_skill = tk.StringVar()
        skill_dropdown = ttk.Combobox(add_window, textvariable=selected_skill, state="readonly")
        skill_dropdown['values'] = [f"{k}: {v}" for k, v in skill_set_options.items()]
        skill_dropdown.pack(pady=5)
        def confirm_add():
            new_skill_display = selected_skill.get()
            if not new_skill_display:
                messagebox.showerror("Error", "Please select a skill.")
                return
            try:
                new_skill_code_str, _ = new_skill_display.split(": ", 1)
                new_skill_code = int(new_skill_code_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid skill format selected.")
                return
            if new_skill_code in skill_set:
                messagebox.showerror("Error", "Skill already exists in skillSet.")
                return
            skill_set.append(new_skill_code)
            skills_listbox.insert(tk.END, skill_set_options.get(new_skill_code, f"Unknown ({new_skill_code})"))
            add_window.destroy()
        confirm_button = ttk.Button(add_window, text="Add", command=confirm_add)
        confirm_button.pack(pady=10)
        cancel_button = ttk.Button(add_window, text="Cancel", command=add_window.destroy)
        cancel_button.pack()
    add_button = ttk.Button(button_frame, text="Add Skill", command=add_skill)
    add_button.pack(side=tk.LEFT, padx=5)
    def remove_skill():
        selected = skills_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a skill to remove.")
            return
        index = selected[0]
        skill_key = skill_set[index]
        confirm = messagebox.askyesno("Confirm", f"Remove skill '{skill_set_options.get(skill_key, f'Unknown ({skill_key})')}'?")
        if confirm:
            del skill_set[index]
            skills_listbox.delete(index)
    remove_button = ttk.Button(button_frame, text="Remove Skill", command=remove_skill)
    remove_button.pack(side=tk.LEFT, padx=5)
    def save_changes():
        if not all(isinstance(skill, int) for skill in skill_set):
            messagebox.showerror("Error", "skillSet contains non-integer values.")
            return
        savegame_data['npcs'][npc_index]['skillSet'] = skill_set
        tree_widget.item(parent_item, text=f"skillSet ({len(skill_set)} skills)")
        tree_widget.delete(*tree_widget.get_children(parent_item))
        build_tree(parent_item, savegame_data['npcs'][npc_index]['skillSet'], parent_path=f"/npcs/{npc_index}/skillSet", tree_widget=tree_widget)
        messagebox.showinfo("Success", "Skill set updated successfully.")
        edit_window.destroy()
    def cancel_changes():
        edit_window.destroy()
    save_button = ttk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)
    cancel_button = ttk.Button(edit_window, text="Cancel", command=cancel_changes)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

# New function to edit an arena's gladiators list
def edit_gladiators(arena_index, gladiators_list, tree_widget, parent_item):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Gladiators")
    edit_window.geometry("400x300")
    
    gladiators_listbox = tk.Listbox(edit_window, selectmode=tk.SINGLE)
    # Populate listbox with each gladiator id and its NPC name
    for npc_id in gladiators_list:
        npc = next((npc for npc in savegame_data.get("npcs", []) if npc.get("id") == npc_id), None)
        if npc:
            npc_display = f"{npc_id}: {get_npc_name(npc)}"
        else:
            npc_display = f"{npc_id}: Unknown NPC"
        gladiators_listbox.insert(tk.END, npc_display)
    gladiators_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
    
    button_frame = ttk.Frame(edit_window)
    button_frame.pack(pady=5)
    
    def add_gladiator():
        add_window = tk.Toplevel(edit_window)
        add_window.title("Add Gladiator")
        add_window.geometry("300x250")  # increased height for search bar
        
        # Create search bar frame at the top
        search_frame = ttk.Frame(add_window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Label and dropdown for NPC selection
        ttk.Label(add_window, text="Select NPC:").pack(pady=10)
        selected_npc = tk.StringVar()
        npc_dropdown = ttk.Combobox(add_window, textvariable=selected_npc, state="readonly")
        
        # Build full list of NPC options
        all_dropdown_values = []
        for npc in savegame_data.get("npcs", []):
            npc_id = npc.get("id")
            if npc_id is None:
                continue
            display = f"{npc_id}: {get_npc_name(npc)}"
            all_dropdown_values.append(display)
        npc_dropdown['values'] = all_dropdown_values
        npc_dropdown.pack(pady=5)
        
        # Update the dropdown list based on search text
        def update_dropdown(*args):
            search_text = search_var.get()
            filtered_values = [val for val in all_dropdown_values if search_text.lower() in val.lower()]
            npc_dropdown['values'] = filtered_values
            if selected_npc.get() not in filtered_values:
                selected_npc.set('')
        
        search_var.trace("w", update_dropdown)
        
        def confirm_add():
            new_npc_display = selected_npc.get()
            if not new_npc_display:
                messagebox.showerror("Error", "Please select an NPC.")
                return
            try:
                new_npc_id_str, _ = new_npc_display.split(": ", 1)
                new_npc_id = int(new_npc_id_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid NPC format selected.")
                return
            # Check if the NPC is already in the current arena
            if new_npc_id in gladiators_list:
                messagebox.showerror("Error", "NPC already exists in gladiators.")
                return
            # Remove the NPC from any other arena's gladiators list to enforce uniqueness
            for i, arena in enumerate(savegame_data.get("arenas", [])):
                if i != arena_index:
                    if new_npc_id in arena.get("gladiators", []):
                        arena["gladiators"] = [x for x in arena.get("gladiators", []) if x != new_npc_id]
            # Additionally, remove the NPC id from any match arrays (like memberIds or candidateIds)
            remove_npc_from_arena_matches(new_npc_id)
            gladiators_list.append(new_npc_id)
            # Reset the NPC's state to the hard-coded neutral state.
            for npc in savegame_data.get("npcs", []):
                if npc.get("id") == new_npc_id:
                    npc["state"] = copy.deepcopy(NEUTRAL_STATE)
                    break
            gladiators_listbox.insert(tk.END, new_npc_display)
            add_window.destroy()
        
        confirm_button = ttk.Button(add_window, text="Add", command=confirm_add)
        confirm_button.pack(pady=10)
        cancel_button = ttk.Button(add_window, text="Cancel", command=add_window.destroy)
        cancel_button.pack()
    
    add_button = ttk.Button(button_frame, text="Add Gladiator", command=add_gladiator)
    add_button.pack(side=tk.LEFT, padx=5)
    
    def remove_gladiator():
        selected = gladiators_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select an NPC to remove.")
            return
        index = selected[0]
        npc_display = gladiators_listbox.get(index)
        confirm = messagebox.askyesno("Confirm", f"Remove NPC '{npc_display}' from gladiators?")
        if confirm:
            del gladiators_list[index]
            gladiators_listbox.delete(index)
    
    remove_button = ttk.Button(button_frame, text="Remove Gladiator", command=remove_gladiator)
    remove_button.pack(side=tk.LEFT, padx=5)
    
    def save_changes():
        savegame_data["arenas"][arena_index]["gladiators"] = gladiators_list
        tree_widget.item(parent_item, text=f"gladiators ({len(gladiators_list)} NPCs)")
        tree_widget.delete(*tree_widget.get_children(parent_item))
        build_tree(parent_item, gladiators_list, parent_path=f"/arenas/{arena_index}/gladiators", tree_widget=tree_widget)
        messagebox.showinfo("Success", "Gladiators list updated successfully.")
        edit_window.destroy()
    
    save_button = ttk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)
    cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Function to perform quick edits on selected NPCs
def quick_edit_npc():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No NPC selected for editing.")
        return
    path = tree.item(selected_item, "values")[0]
    npc = view_attribute(savegame_data, path)
    if not isinstance(npc, dict):
        messagebox.showerror("Error", "Selected item is not a valid NPC.")
        return
    edit_window = tk.Toplevel(root)
    edit_window.title("Quick Edit NPC")
    edit_window.geometry("400x350")
    tk.Label(edit_window, text="Unit Name:").pack(pady=5)
    unitname_var = tk.StringVar(value=npc.get('unitname', ''))
    unitname_entry = ttk.Entry(edit_window, textvariable=unitname_var)
    unitname_entry.pack(pady=5)
    tk.Label(edit_window, text="Team:").pack(pady=5)
    team_var = tk.IntVar(value=npc.get('team', 0))
    team_spinbox = ttk.Spinbox(edit_window, from_=0, to=10, textvariable=team_var)
    team_spinbox.pack(pady=5)
    if 'isMagician' in npc:
        tk.Label(edit_window, text="Is Magician:").pack(pady=5)
        isMagician_var = tk.BooleanVar(value=npc.get('isMagician', False))
        isMagician_checkbox = ttk.Checkbutton(edit_window, variable=isMagician_var)
        isMagician_checkbox.pack(pady=5)
    if 'hitable' in npc:
        tk.Label(edit_window, text="Hitable:").pack(pady=5)
        hitable_var = tk.BooleanVar(value=npc.get('hitable', False))
        hitable_checkbox = ttk.Checkbutton(edit_window, variable=hitable_var)
        hitable_checkbox.pack(pady=5)
    def save_edits():
        npc['unitname'] = unitname_var.get()
        npc['team'] = team_var.get()
        if 'isMagician' in npc:
            npc['isMagician'] = isMagician_var.get()
        if 'hitable' in npc:
            npc['hitable'] = hitable_var.get()
        tree.item(selected_item, text=unitname_var.get())
        save_savegame(file_path, savegame_data)
        messagebox.showinfo("Success", "NPC updated successfully.")
        edit_window.destroy()
    save_button = ttk.Button(edit_window, text="Save", command=save_edits)
    save_button.pack(pady=10)
    cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy)
    cancel_button.pack(pady=5)

# Function to display the main GUI
def display_gui(savegame_data_param):
    global root, tree, file_path, savegame_data, team_0_tree
    savegame_data = savegame_data_param
    if not savegame_data:
        messagebox.showerror("Error", "Savegame data is empty or could not be loaded.")
        return
    root = tk.Tk()
    root.title("Savegame Editor")
    root.geometry("1000x700")
    
    # Add search bar at the top
    search_frame = ttk.Frame(root)
    search_frame.pack(fill=tk.X, padx=10, pady=5)
    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side=tk.LEFT)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    search_entry.bind("<KeyRelease>", lambda event: update_filter(search_var.get()))
    
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    global tree
    tree = ttk.Treeview(tree_frame, columns=("Path",), show="tree headings", yscrollcommand=tree_scrollbar.set)
    tree.heading("#0", text="Attribute")
    tree.heading("Path", text="Path")
    tree.column("#0", width=400)
    tree.column("Path", width=600)
    tree.pack(fill=tk.BOTH, expand=True)
    tree_scrollbar.config(command=tree.yview)
    build_tree("", savegame_data, tree_widget=tree)
    tree.bind("<Double-1>", lambda event: on_tree_select(event, tree))
    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(pady=10)
    quick_edit_button = ttk.Button(buttons_frame, text="Quick Edit NPC", command=quick_edit_npc)
    quick_edit_button.pack(side=tk.LEFT, padx=10)
    team_0_button = ttk.Button(buttons_frame, text="Show NPCs on Team 0", command=display_npc_tree_team_0)
    team_0_button.pack(side=tk.LEFT, padx=10)
    hitable_button = ttk.Button(buttons_frame, text="Show Hitable Attributes on Team 0", command=display_hitable_attributes_team_0)
    hitable_button.pack(side=tk.LEFT, padx=10)
    save_button = ttk.Button(buttons_frame, text="Save Changes", command=lambda: save_savegame(file_path, savegame_data))
    save_button.pack(side=tk.LEFT, padx=10)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: saveedit.py <savegame_file>")
        messagebox.showerror("Error", "No savegame file specified.\nUsage: saveedit.py <savegame_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    savegame_data = load_savegame(file_path)
    if savegame_data:
        display_gui(savegame_data)
