I got lazy, so Readme done by GPT. lemme know if there's an issue or it sucks. 

# Blackthorn Arena Reforged Savegame Editor

Welcome to the **Blackthorn Arena Reforged Savegame Editor**! This tool allows you to customize your game experience by editing your savegame files. Whether you want to enhance your gladiators, enable powerful spells, or tweak game mechanics like invincibility flags, this editor provides a simple and user-friendly interface to make those changes effortlessly.

---

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Launching the Editor](#launching-the-editor)
  - [GUI Overview](#gui-overview)
- [Features](#features)
  - [Quick Edit NPC](#quick-edit-npc)
  - [Show NPCs on Team 0](#show-npcs-on-team-0)
  - [Show Hitable Attributes on Team 0](#show-hitable-attributes-on-team-0)
  - [Save Changes](#save-changes)
- [Wizard: Enabling Spells](#wizard-enabling-spells)
- [Understanding the `hitable` Attribute](#understanding-the-hitable-attribute)
- [Backup Mechanism](#backup-mechanism)
- [Preventing Savegame Corruption](#preventing-savegame-corruption)
- [Disclaimer](#disclaimer)

---

## Installation

1. **Install Python 3:**
   - Download and install Python 3 from the [official website](https://www.python.org/downloads/).
   - Ensure that Python is added to your system's PATH during installation.

2. **Download the Editor:**
   - Clone the repository or download the `saveedit.py` script directly.

   ```bash
   git clone https://github.com/yourusername/BlackthornArenaReforgedSavegameEditor.git
   ```

3. **Install Dependencies:**
   - The editor uses standard Python libraries (`tkinter`, `json`, `os`, `sys`) which are typically included with Python.
   - If `tkinter` is not installed, follow instructions based on your operating system:
     - **Windows:** Included with standard Python installation.
     - **macOS:** Included with standard Python installation.
     - **Linux (Debian/Ubuntu):**
       ```bash
       sudo apt-get install python3-tk
       ```

---

## Getting Started

### Launching the Editor

1. **Open Terminal/Command Prompt:**
   - Navigate to the directory containing the `saveedit.py` script.

2. **Run the Script:**
   - Execute the script by specifying your savegame file as an argument.

   ```bash
   python3 saveedit.py path/to/your/savegame.dat
   ```

   - **Example:**

     ```bash
     python3 saveedit.py sav.dat
     ```

### GUI Overview

Upon launching, you'll see a window with the following main components:

- **Main Treeview:** Displays the JSON structure of your savegame in a hierarchical tree format.
- **Buttons Panel:** Located below the Treeview, contains buttons for various editing features.

Double-click on any attribute (leaf node) in the Treeview to edit its value.

---

## Features

### Quick Edit NPC

![Quick Edit NPC Button](https://example.com/quick-edit-npc.png)

**Purpose:** Quickly modify common attributes of a selected NPC without navigating through the entire JSON structure.

**How to Use:**

1. **Select an NPC:**
   - Click on an NPC entry in the main Treeview to highlight it.

2. **Click "Quick Edit NPC":**
   - A new window will appear with editable fields:
     - **Unit Name (`unitname`):** Change the NPC's name.
     - **Team (`team`):** Assign the NPC to a different team (integer value).
     - **Is Magician (`isMagician`):** Toggle magical abilities (`True` or `False`).
     - **Hitable (`hitable`):** Control invincibility (`True` or `False`).

3. **Modify Attributes:**
   - Update the desired fields as needed.

4. **Save or Cancel:**
   - Click **"Save"** to apply changes or **"Cancel"** to discard.

**Notes:**
- **Hitable Attribute:** Setting `hitable` to `False` makes the gladiator invincible except against traps and specific quests.

---

### Show NPCs on Team 0

![Show NPCs on Team 0 Button](https://example.com/show-npcs-team0.png)

**Purpose:** Display all NPCs assigned to team 0, excluding those named "Arena Guard".

**How to Use:**

1. **Click "Show NPCs on Team 0":**
   - A new window will open listing all relevant NPCs.

2. **Interact with NPCs:**
   - **View Attributes:** Expand NPC entries to see their attributes.
   - **Edit Attributes:** Double-click on any attribute to modify its value.

**Benefits:**
- **Focused Editing:** Manage a specific subset of NPCs without unrelated entries.

---

### Show Hitable Attributes on Team 0

![Show Hitable Attributes on Team 0 Button](https://example.com/show-hitable-team0.png)

**Purpose:** Display and toggle the `hitable` attribute for each NPC on team 0, excluding "Arena Guard".

**How to Use:**

1. **Click "Show Hitable Attributes on Team 0":**
   - A new window will display a list of NPCs with their `hitable` status.

2. **Toggle Hitable Status:**
   - **Double-Click `hitable`:** Click on the `hitable` value to toggle between `True` and `False`.

**Impact:**
- **Hitable `False`:** Gladiators become invincible except against traps and certain quests.
- **Hitable `True`:** Gladiators can be targeted and defeated normally.

---

### Save Changes

![Save Changes Button](https://example.com/save-changes.png)

**Purpose:** Save all modifications made within the editor to your savegame file.

**How to Use:**

1. **After Making Edits:**
   - Whether you've edited attributes via the main Treeview, Quick Edit NPC, or specialized views.

2. **Click "Save Changes":**
   - The script will:
     - **Create a Backup:** Generates a backup (`sav.dat.backup`, `sav.dat.backup1`, etc.) to prevent data loss.
     - **Save JSON Data:** Writes the modified data back to the original savegame file in a compressed format.

3. **Confirmation:**
   - A success message will confirm that changes have been saved and a backup has been created.

**Note:** Always ensure backups are created before making significant changes.

---

## Wizard: Enabling Spells

Enhancing your gladiators with spells can significantly boost their combat abilities. Follow this simple wizard to enable spells through the skill sets.

**Steps:**

1. **Launch the Editor and Select an NPC:**
   - Open `saveedit.py` with your savegame file.
   - Select the NPC you want to empower.

2. **Open Skill Set Editor:**
   - Double-click on the `skillSet` attribute in the NPC's entry.

3. **Add a New Spell:**
   - Click the **"Add Skill"** button.
   - Choose a spell from the dropdown menu (e.g., `101: fire`).
   - Click **"Add"** to include the spell in the NPC's `skillSet`.

4. **Remove Existing Skill (Optional):**
   - Select a skill from the list and click **"Remove Skill"** if you wish to replace it.

5. **Save Changes:**
   - Click **"Save"** in the Skill Set Editor.
   - Then, click **"Save Changes"** in the main editor to apply all modifications.

6. **Verify in Game:**
   - Launch **Blackthorn Arena Reforged** and check the NPC's new abilities.

**Tips:**
- **Avoid Duplicates:** The editor prevents adding duplicate skills to maintain data integrity.
- **Spell Codes:** Ensure you're selecting the correct spell codes as per the `skill_set_options` dictionary.

---

## Understanding the `hitable` Attribute

The `hitable` attribute determines whether a gladiator can be targeted and defeated in combat.

- **`hitable: True`**
  - **Description:** The gladiator can be hit and defeated by opponents.
  - **Use Case:** Standard combat scenarios.

- **`hitable: False`**
  - **Description:** The gladiator is invincible and cannot be defeated through standard combat.
  - **Exceptions:** Vulnerable to traps and specific map quests that reset this flag.
  - **Use Case:** Creating unbeatable gladiators for challenging gameplay or special events.

**Caution:** Setting `hitable` to `False` can impact game balance. Use it judiciously to enhance your gaming experience without making it too easy or unmanageable.

---

## Backup Mechanism

Protecting your savegame data is crucial. The editor automatically creates backups to prevent data loss.

- **Automatic Backups:**
  - **Backup Naming:** Saves backups as `sav.dat.backup`, `sav.dat.backup1`, `sav.dat.backup2`, etc., to avoid overwriting existing backups.
  
- **Manual Backups (Recommended):**
  - **How to Create:**
    ```bash
    cp sav.dat sav.dat.manual_backup
    ```
  - **Purpose:** Provides an additional layer of security before making major changes.

**Note:** Always keep backups until you're confident that your modifications work as intended.

---

## Preventing Savegame Corruption

To ensure a smooth and error-free experience, follow these guidelines:

1. **Use the Editor Properly:**
   - Always launch the editor using the correct command with your savegame file as an argument.
   
2. **Create Backups:**
   - Rely on the automatic backup feature and create manual backups for extra safety.
   
3. **Avoid Interruptions:**
   - Do not close the editor or shut down your computer while saving changes.
   
4. **Validate Changes:**
   - Double-check the attributes and skills you've modified to ensure they're correct.
   
5. **Test Incrementally:**
   - Make small changes and test them in-game before proceeding with more extensive edits.

**Remember:** Proper backup and cautious editing are your best defenses against savegame corruption.

---

## Disclaimer

Modifying game save files can lead to unexpected behavior or game instability. **Use this editor at your own risk.** Always ensure you have proper backups before making any changes. The creators are not responsible for any data loss or game issues resulting from the use of this tool.

---

Enjoy customizing your **Blackthorn Arena Reforged** experience!
