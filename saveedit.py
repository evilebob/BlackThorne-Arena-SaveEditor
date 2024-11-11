import json
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys

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

# Function to load savegame data
def load_savegame(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Debug: Print the number of NPCs loaded
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
    
    # If backup file exists, append a number to create a unique backup
    if os.path.exists(backup_path):
        i = 1
        while True:
            new_backup_path = f"{file_path}.backup{i}"
            if not os.path.exists(new_backup_path):
                backup_path = new_backup_path
                break
            i += 1
    try:
        # Create a backup before overwriting
        os.rename(file_path, backup_path)
        print(f"Backup created at {backup_path}")
        
        with open(file_path, 'w') as file:
            # Save JSON in compressed format without unnecessary whitespace
            json.dump(savegame_data, file, separators=(',', ':'), sort_keys=False)
        print(f"Savegame updated successfully at {file_path}")
        messagebox.showinfo("Success", f"Savegame updated successfully.\nBackup created at {backup_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")

# Function to extract NPC names using 'unitname'
def get_npc_name(npc):
    return npc.get('unitname', 'Unnamed NPC')

# Function to build the main data tree
def build_tree(parent, data, parent_path="", tree_widget=None):
    if tree_widget is None:
        return
    if isinstance(data, dict):
        for key, value in data.items():
            display_text = f"{key}"
            # Construct the new path
            new_path = f"{parent_path}/{key}"
            node = tree_widget.insert(parent, "end", text=display_text, open=False, values=[new_path])
            build_tree(node, value, new_path, tree_widget)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            name = get_npc_name(value) if isinstance(value, dict) else ''
            display_text = f"[{index}] {name}" if name else f"[{index}]"
            # Construct the new path
            new_path = f"{parent_path}/{index}"
            node = tree_widget.insert(parent, "end", text=display_text, open=False, values=[new_path])
            build_tree(node, value, new_path, tree_widget)
    else:
        # Leaf node, display the value
        tree_widget.insert(parent, "end", text=f"{data}", values=[parent_path])

# Function to display NPC tree for team 0, excluding "Arena Guard"
def display_npc_tree_team_0():
    # Filter NPCs on team 0 and exclude those named "Arena Guard"
    units = [(index, npc) for index, npc in enumerate(savegame_data.get('npcs', []))
             if npc.get('team') == 0 and npc.get('unitname') != 'Arena Guard']
    if not units:
        messagebox.showerror("Error", "No NPCs on team 0 found in the savegame (excluding 'Arena Guard').")
        return

    # Sort NPCs by index and name for better organization
    units.sort(key=lambda x: (x[0], x[1].get('unitname', '')))

    # Create a new window to display the NPC tree
    team_0_window = tk.Toplevel(root)
    team_0_window.title("NPCs on Team 0 (Excluding 'Arena Guard')")
    team_0_window.geometry("800x600")

    # Treeview to display NPCs with tree structure
    team_0_tree = ttk.Treeview(team_0_window, columns=("Path",), show="tree headings")
    team_0_tree.heading("#0", text="NPC (Index and Name)")
    team_0_tree.heading("Path", text="Path")
    team_0_tree.column("#0", width=400)
    team_0_tree.column("Path", width=400)
    team_0_tree.pack(fill=tk.BOTH, expand=True)

    # Scrollbar for the tree
    scrollbar = ttk.Scrollbar(team_0_window, orient="vertical", command=team_0_tree.yview)
    team_0_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Bind double-click action to the team_0_tree
    team_0_tree.bind("<Double-1>", lambda event: on_tree_select(event, team_0_tree))

    # Insert each NPC as a top-level item with its index and name
    for index, npc in units:
        unitname = get_npc_name(npc)
        unit_path = f"/npcs/{index}"
        display_text = f"[{index}] {unitname}"
        npc_item = team_0_tree.insert("", "end", text=display_text, open=False, values=[unit_path])

        # Build the NPC's attributes as child items
        build_tree(npc_item, npc, parent_path=unit_path, tree_widget=team_0_tree)

# Function to display NPCs on team 0 with only 'hitable' attribute, excluding "Arena Guard"
def display_hitable_attributes_team_0():
    # Filter NPCs on team 0 and exclude those named "Arena Guard"
    units = [(index, npc) for index, npc in enumerate(savegame_data.get('npcs', []))
             if npc.get('team') == 0 and npc.get('unitname') != 'Arena Guard']
    if not units:
        messagebox.showerror("Error", "No NPCs on team 0 found in the savegame (excluding 'Arena Guard').")
        return

    # Sort NPCs by index and name for better organization
    units.sort(key=lambda x: (x[0], x[1].get('unitname', '')))

    # Create a new window to display the hitable attributes
    hitable_window = tk.Toplevel(root)
    hitable_window.title("Hitable Attributes of NPCs on Team 0 (Excluding 'Arena Guard')")
    hitable_window.geometry("600x400")

    # Treeview to display NPCs and their 'hitable' attribute
    hitable_tree = ttk.Treeview(hitable_window, columns=("NPC", "Path", "Hitable"), show="headings")
    hitable_tree.heading("#1", text="NPC")
    hitable_tree.heading("#2", text="Path")
    hitable_tree.heading("#3", text="Hitable")
    hitable_tree.column("#1", width=200)
    hitable_tree.column("#2", width=200)
    hitable_tree.column("#3", width=100)
    hitable_tree.pack(fill=tk.BOTH, expand=True)

    # Scrollbar for the tree
    scrollbar = ttk.Scrollbar(hitable_window, orient="vertical", command=hitable_tree.yview)
    hitable_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Bind double-click action to the hitable_tree
    hitable_tree.bind("<Double-1>", lambda event: on_hitable_edit(event, hitable_tree))

    # Insert each NPC with their 'hitable' attribute
    for index, npc in units:
        unitname = get_npc_name(npc)
        unit_path = f"/npcs/{index}/hitable"
        hitable_value = npc.get('hitable', False)  # Default to False if 'hitable' not present

        # Ensure 'hitable' is a boolean
        if not isinstance(hitable_value, bool):
            # Attempt to convert to boolean
            if isinstance(hitable_value, str):
                if hitable_value.lower() in ['true', 'yes', '1']:
                    hitable_value = True
                elif hitable_value.lower() in ['false', 'no', '0']:
                    hitable_value = False
                else:
                    # If ambiguous, default to False and inform the user
                    hitable_value = False
                    print(f"Warning: 'hitable' attribute for NPC '{unitname}' at path '{unit_path}' is not a boolean. Defaulting to False.")
            elif isinstance(hitable_value, (int, float)):
                hitable_value = bool(hitable_value)
            else:
                # Default to False for other types
                hitable_value = False
                print(f"Warning: 'hitable' attribute for NPC '{unitname}' at path '{unit_path}' is not a boolean. Defaulting to False.")

            # Update the savegame_data with the converted value
            savegame_data['npcs'][index]['hitable'] = hitable_value

        # Insert into the treeview with correct path
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
        # Determine which treeview triggered the event
        if tree_widget is None:
            tree_widget = event.widget

        selected_item = tree_widget.focus()
        if not selected_item:
            return

        # Get the path of the selected item
        path = tree_widget.item(selected_item, "values")[0]
        attribute = tree_widget.item(selected_item, "text")

        # Retrieve the current value
        current_value = view_attribute(savegame_data, path)

        if current_value is None:
            messagebox.showerror("Error", f"Attribute '{attribute}' not found at path '{path}'.")
            return

        # Special handling for 'skillSet' attribute
        if path.endswith("/skillSet"):
            # Extract NPC index from path
            parts = path.strip('/').split('/')
            if len(parts) >= 3:
                npc_index = int(parts[1])  # Assumes path is /npcs/{index}/skillSet
                skill_set = savegame_data['npcs'][npc_index].get('skillSet', [])
                edit_skill_set(npc_index, skill_set, tree_widget, selected_item)
            else:
                messagebox.showerror("Error", "Invalid path for 'skillSet'.")
            return

        # Special handling for individual skill items within 'skillSet'
        if "/skillSet/" in path:
            # Extract NPC index and skill index from path
            parts = path.strip('/').split('/')
            if len(parts) >= 4:
                npc_index = int(parts[1])  # Assumes path is /npcs/{index}/skillSet/{skill_index}
                skill_index = int(parts[3])
                current_skill = savegame_data['npcs'][npc_index]['skillSet'][skill_index]
                edit_individual_skill(npc_index, skill_index, current_skill, tree_widget, selected_item)
            else:
                messagebox.showerror("Error", "Invalid path for individual skill.")
            return

        # Determine the data type
        if isinstance(current_value, bool):
            # For boolean, present a dialog with True/False options
            new_value = messagebox.askyesno("Edit Attribute", f"Set '{attribute}' to True?")
            if new_value is None:
                return  # User canceled
            new_value_converted = new_value  # True or False
        elif isinstance(current_value, int):
            # For integers, use simpledialog to get integer input
            new_value_str = simpledialog.askstring("Edit Attribute", f"Current value of '{attribute}': {current_value}\nEnter new integer value:")
            if new_value_str is None:
                return  # User canceled
            try:
                new_value_converted = int(new_value_str)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.")
                return
        else:
            # For strings or other types, use simpledialog to get string input
            new_value_str = simpledialog.askstring("Edit Attribute", f"Current value of '{attribute}': {current_value}\nEnter new value:")
            if new_value_str is None:
                return  # User canceled
            new_value_converted = new_value_str

        # Update the savegame_data with the new value
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

        # Update the treeview
        tree_widget.item(selected_item, text=f"{new_value_converted}")

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

        # Get the path and current 'hitable' value
        values = tree_widget.item(selected_item, "values")
        if len(values) < 3:
            messagebox.showerror("Error", "Insufficient data to edit 'hitable' attribute.")
            return

        unitname, path, hitable_value = values
        attribute = "hitable"

        # Debug: Print current value and type
        print(f"Editing 'hitable' for NPC '{unitname}' at path '{path}'. Current value: {hitable_value} (Type: {type(hitable_value)})")

        # Convert hitable_value from string to boolean
        if isinstance(hitable_value, bool):
            current_value = hitable_value
        elif isinstance(hitable_value, str):
            if hitable_value.lower() in ['true', 'yes', '1']:
                current_value = True
            elif hitable_value.lower() in ['false', 'no', '0']:
                current_value = False
            else:
                current_value = False
        elif isinstance(hitable_value, (int, float)):
            current_value = bool(hitable_value)
        else:
            current_value = False

        # Toggle the 'hitable' value
        new_value = not current_value

        # Update the savegame_data with the new value
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

        # Update the treeview
        tree_widget.item(selected_item, values=(unitname, path, new_value))

        # Debug: Print the updated value
        print(f"'hitable' for NPC '{unitname}' at path '{path}' set to {new_value}.")

    except KeyError as e:
        messagebox.showerror("Key Error", f"KeyError: {e} at path '{path}'.")
    except IndexError as e:
        messagebox.showerror("Index Error", f"IndexError: {e} at path '{path}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to edit individual skill
def edit_individual_skill(npc_index, skill_index, current_skill, tree_widget, selected_item):
    try:
        # Get the current skill name
        current_skill_name = skill_set_options.get(current_skill, f"Unknown ({current_skill})")

        # Create a new window for editing the skill
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
            # Parse the selected skill to extract code
            try:
                new_skill_code_str, _ = new_skill_display.split(": ", 1)
                new_skill_code = int(new_skill_code_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid skill format selected.")
                return
            # Check for duplicates
            if new_skill_code in savegame_data['npcs'][npc_index]['skillSet']:
                messagebox.showerror("Error", "Skill already exists in skillSet.")
                return
            # Update the skill in the skillSet list
            savegame_data['npcs'][npc_index]['skillSet'][skill_index] = new_skill_code
            # Update the treeview item
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

    # Listbox to display current skills
    skills_listbox = tk.Listbox(edit_window, selectmode=tk.SINGLE)
    for skill in skill_set:
        skill_name = skill_set_options.get(skill, f"Unknown ({skill})")
        skills_listbox.insert(tk.END, skill_name)
    skills_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    button_frame = ttk.Frame(edit_window)
    button_frame.pack(pady=5)

    # Add Skill Button
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

    # Remove Skill Button
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

    # Save and Cancel Buttons
    def save_changes():
        # Ensure 'skillSet' remains a flat list of integers
        if not all(isinstance(skill, int) for skill in skill_set):
            messagebox.showerror("Error", "skillSet contains non-integer values.")
            return
        # Update the savegame_data
        savegame_data['npcs'][npc_index]['skillSet'] = skill_set
        # Update the treeview
        tree_widget.item(parent_item, text=f"skillSet ({len(skill_set)} skills)")
        # Refresh child items to reflect changes
        tree_widget.delete(*tree_widget.get_children(parent_item))
        # Correctly pass only the 'skillSet' list and its path
        build_tree(parent_item, savegame_data['npcs'][npc_index]['skillSet'], parent_path=f"/npcs/{npc_index}/skillSet", tree_widget=tree_widget)
        messagebox.showinfo("Success", "Skill set updated successfully.")
        edit_window.destroy()

    def cancel_changes():
        edit_window.destroy()

    save_button = ttk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button = ttk.Button(edit_window, text="Cancel", command=cancel_changes)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Function to perform quick edits on selected NPCs
def quick_edit_npc():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No NPC selected for editing.")
        return

    # Retrieve the path of the selected item
    # Assuming the first column is "Path"
    path = tree.item(selected_item, "values")[0]
    npc = view_attribute(savegame_data, path)
    if not isinstance(npc, dict):
        messagebox.showerror("Error", "Selected item is not a valid NPC.")
        return

    # Create a dialog to edit NPC attributes
    edit_window = tk.Toplevel(root)
    edit_window.title("Quick Edit NPC")
    edit_window.geometry("400x350")  # Increased height to accommodate more fields

    # Example: Editing 'unitname' and 'team' attributes
    tk.Label(edit_window, text="Unit Name:").pack(pady=5)
    unitname_var = tk.StringVar(value=npc.get('unitname', ''))
    unitname_entry = ttk.Entry(edit_window, textvariable=unitname_var)
    unitname_entry.pack(pady=5)

    tk.Label(edit_window, text="Team:").pack(pady=5)
    team_var = tk.IntVar(value=npc.get('team', 0))
    team_spinbox = ttk.Spinbox(edit_window, from_=0, to=10, textvariable=team_var)
    team_spinbox.pack(pady=5)

    # Example: Editing a boolean attribute 'isMagician' if it exists
    if 'isMagician' in npc:
        tk.Label(edit_window, text="Is Magician:").pack(pady=5)
        isMagician_var = tk.BooleanVar(value=npc.get('isMagician', False))
        isMagician_checkbox = ttk.Checkbutton(edit_window, variable=isMagician_var)
        isMagician_checkbox.pack(pady=5)

    # Example: Editing a boolean attribute 'hitable' if it exists
    if 'hitable' in npc:
        tk.Label(edit_window, text="Hitable:").pack(pady=5)
        hitable_var = tk.BooleanVar(value=npc.get('hitable', False))
        hitable_checkbox = ttk.Checkbutton(edit_window, variable=hitable_var)
        hitable_checkbox.pack(pady=5)

    def save_edits():
        # Update the NPC data
        npc['unitname'] = unitname_var.get()
        npc['team'] = team_var.get()
        if 'isMagician' in npc:
            npc['isMagician'] = isMagician_var.get()
        if 'hitable' in npc:
            npc['hitable'] = hitable_var.get()

        # Update the treeview
        tree.item(selected_item, text=unitname_var.get())

        # Save the changes back to the file
        save_savegame(file_path, savegame_data)

        messagebox.showinfo("Success", "NPC updated successfully.")
        edit_window.destroy()

    save_button = ttk.Button(edit_window, text="Save", command=save_edits)
    save_button.pack(pady=10)

    # Add Cancel Button
    cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy)
    cancel_button.pack(pady=5)

# Function to display the main GUI
def display_gui(savegame_data_param):
    global root, tree, file_path, savegame_data
    savegame_data = savegame_data_param
    if not savegame_data:
        messagebox.showerror("Error", "Savegame data is empty or could not be loaded.")
        return

    root = tk.Tk()
    root.title("Savegame Editor")
    root.geometry("1000x700")  # Increased size for better visibility

    # Treeview Frame
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Scrollbar for the treeview
    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview to display the savegame data
    global tree  # Declare as global to access in other functions
    tree = ttk.Treeview(tree_frame, columns=("Path",), show="tree headings", yscrollcommand=tree_scrollbar.set)
    tree.heading("#0", text="Attribute")
    tree.heading("Path", text="Path")
    tree.column("#0", width=400)
    tree.column("Path", width=600)
    tree.pack(fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    tree_scrollbar.config(command=tree.yview)

    # Build the main data tree
    build_tree("", savegame_data, tree_widget=tree)

    # Bind double-click action to the tree
    tree.bind("<Double-1>", lambda event: on_tree_select(event, tree))

    # Buttons Frame
    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(pady=10)

    # Quick Edit NPC button
    quick_edit_button = ttk.Button(buttons_frame, text="Quick Edit NPC", command=quick_edit_npc)
    quick_edit_button.pack(side=tk.LEFT, padx=10)

    # Show NPCs on Team 0 button
    team_0_button = ttk.Button(buttons_frame, text="Show NPCs on Team 0", command=display_npc_tree_team_0)
    team_0_button.pack(side=tk.LEFT, padx=10)

    # New Button: Show Hitable Attributes on Team 0
    hitable_button = ttk.Button(buttons_frame, text="Show Hitable Attributes on Team 0", command=display_hitable_attributes_team_0)
    hitable_button.pack(side=tk.LEFT, padx=10)

    # Save Changes button
    save_button = ttk.Button(buttons_frame, text="Save Changes", command=lambda: save_savegame(file_path, savegame_data))
    save_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: saveedit.py <savegame_file>")
        messagebox.showerror("Error", "No savegame file specified.\nUsage: saveedit.py <savegame_file>")
        sys.exit(1)

    # Load savegame file
    file_path = sys.argv[1]
    savegame_data = load_savegame(file_path)

    if savegame_data:
        # Display the GUI for interactive editing
        display_gui(savegame_data)
