# Admin Utility for Marlin Configuration Tool (C) Thinkersbluff, 2025
'''A gui-based app for managing the Admin tasks required to support the Marlin Configuration Tool'''


import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys
import re
import webbrowser
import json
import logging

# Setup logging to file (same format as configurator.py)
logging.basicConfig(
    filename='configurator_admin_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Application metadata
APP_VERSION = "v1.0.0"

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LICENSE_PATH = os.path.join(APP_DIR, "LICENSE")
README_FILES = [
    ("README (User Guide)", os.path.join(APP_DIR, "README.md")),
    ("README (Developer Notes)", os.path.join(APP_DIR, "README_DEV.md")),
]
FLASH_CARDS_PATH = os.path.join(APP_DIR, "flash_cards.json")
CONFIG_PATH = os.path.join(APP_DIR, "config.json")



WORKFLOW_PATH = os.path.join(APP_DIR, "workflow.json")

def edit_workflow():
    WorkflowEditor()

class WorkflowEditor(tk.Toplevel):
    '''A window for editing the workflow checklist.'''
    def __init__(self):
        super().__init__()
        self.title("Workflow Checklist Editor")
        self.geometry("650x400")
        self.steps = self.load_workflow()
        self.index = 0 if self.steps else -1
        self.create_widgets()
        self.show_step()

    def load_workflow(self):
        try:
            with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("workflow", [])
        except Exception:
            return []

    def save_workflow(self):
        try:
            with open(WORKFLOW_PATH, "w", encoding="utf-8") as f:
                json.dump({"workflow": self.steps}, f, indent=2, ensure_ascii=False)
            self.show_autoclose_popup("Workflow saved.", duration=2500)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def show_autoclose_popup(self, message, duration=2000):
        popup = tk.Toplevel(self)
        popup.title("Saved")
        popup.geometry("250x80")
        popup.resizable(False, False)
        tk.Label(popup, text=message, font=("Arial", 12)).pack(expand=True, fill="both", pady=18)
        popup.after(duration, popup.destroy)

    def create_widgets(self):
        self.fields = {}
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Step heading
        tk.Label(frame, text="Step Heading:").grid(row=0, column=0, sticky="ne")
        self.fields["step"] = tk.Entry(frame, width=70)
        self.fields["step"].grid(row=0, column=1, sticky="w", pady=2)
        # Description (multi-line)
        tk.Label(frame, text="Description:").grid(row=1, column=0, sticky="ne")
        self.fields["description"] = tk.Text(frame, width=70, height=4, wrap="word")
        self.fields["description"].grid(row=1, column=1, sticky="we", pady=2)
        scroll = tk.Scrollbar(frame, command=self.fields["description"].yview)
        self.fields["description"].config(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=2, sticky="nsw")
        frame.grid_columnconfigure(1, weight=1)
        # Navigation and actions
        nav = tk.Frame(self)
        nav.pack(pady=10)
        tk.Button(nav, text="Previous", command=self.prev_step).pack(side="left", padx=5)
        tk.Button(nav, text="Next", command=self.next_step).pack(side="left", padx=5)
        tk.Button(nav, text="Move Up", command=self.move_up).pack(side="left", padx=5)
        tk.Button(nav, text="Move Down", command=self.move_down).pack(side="left", padx=5)
        tk.Button(nav, text="Add New", command=self.add_step).pack(side="left", padx=5)
        tk.Button(nav, text="Delete", command=self.delete_step).pack(side="left", padx=5)
        tk.Button(nav, text="Save", command=self.save_current_and_all).pack(side="left", padx=5)
        tk.Button(nav, text="Close", command=self.destroy).pack(side="left", padx=5)

    def show_step(self):
        if self.index == -1 or not self.steps:
            for widget in self.fields.values():
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                else:
                    widget.delete(0, tk.END)
            self.title("Workflow Checklist Editor (0/0)")
            return
        step = self.steps[self.index]
        self.fields["step"].delete(0, tk.END)
        self.fields["step"].insert(0, step.get("step", ""))
        self.fields["description"].delete("1.0", tk.END)
        self.fields["description"].insert("1.0", step.get("description", ""))
        self.title(f"Workflow Checklist Editor ({self.index+1}/{len(self.steps)})")

    def save_current_and_all(self):
        if self.index == -1:
            return
        step = self.steps[self.index]
        step["step"] = self.fields["step"].get()
        step["description"] = self.fields["description"].get("1.0", tk.END).strip()
        self.steps[self.index] = step
        self.save_workflow()

    def next_step(self):
        if self.steps and self.index < len(self.steps) - 1:
            self.save_current_and_all()
            self.index += 1
            self.show_step()

    def prev_step(self):
        if self.steps and self.index > 0:
            self.save_current_and_all()
            self.index -= 1
            self.show_step()

    def move_up(self):
        if self.steps and self.index > 0:
            self.save_current_and_all()
            self.steps[self.index-1], self.steps[self.index] = self.steps[self.index], self.steps[self.index-1]
            self.index -= 1
            self.show_step()

    def move_down(self):
        if self.steps and self.index < len(self.steps) - 1:
            self.save_current_and_all()
            self.steps[self.index+1], self.steps[self.index] = self.steps[self.index], self.steps[self.index+1]
            self.index += 1
            self.show_step()

    def add_step(self):
        self.save_current_and_all()
        new_step = {"step": "", "description": ""}
        self.steps.insert(self.index+1 if self.index != -1 else 0, new_step)
        self.index = self.index+1 if self.index != -1 else 0
        self.show_step()

    def delete_step(self):
        if self.steps and self.index != -1:
            del self.steps[self.index]
            if self.index >= len(self.steps):
                self.index = len(self.steps) - 1
            if not self.steps:
                self.index = -1
            self.show_step()


def display_license():
    '''Show the license text in a new window.'''
    try:
        with open(LICENSE_PATH, "r", encoding="utf-8") as f:
            license_text = f.read()
    except Exception as e:
        license_text = f"Could not load license: {e}"
    TextWindow("License", license_text, linkify=True)



def get_repo_root():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("repo_root", "")
    except Exception:
        return ""

def set_repo_root(new_path):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data["repo_root"] = new_path
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def prompt_for_repo_root():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Set Repository Root", "Please select the repository root directory.")
    new_path = filedialog.askdirectory(title="Select Repository Root")
    if new_path:
        set_repo_root(new_path)
        return new_path
    return None

def launch_configurator():
    logging.info('launch_configurator called')
    configurator_path = os.path.join(APP_DIR, "configurator.py")
    repo_root = get_repo_root()
    if not os.path.isfile(configurator_path):
        logging.error(f"Configurator app not found at {configurator_path}")
        messagebox.showerror("Error", "Configurator app not found.")
        return
    # Default to current working directory if repo_root is blank
    if not repo_root:
        logging.warning('repo_root not set in config.json, defaulting to current working directory')
        repo_root = os.getcwd()
    if not os.path.isdir(repo_root):
        logging.warning(f'repo_root {repo_root} is not a directory, prompting user')
        repo_root = prompt_for_repo_root()
        if not repo_root or not os.path.isdir(repo_root):
            logging.error('Repository root not set or not found after prompt. Aborting launch.')
            messagebox.showerror("Error", "Repository root not set or not found. Please fix config.json.")
            return
    # Change directory to repo_root before launching
    logging.info(f'Changing directory to repo_root: {repo_root}')
    os.chdir(repo_root)
    logging.info(f'Launching configurator: {configurator_path}')
    os.system(f'"{sys.executable}" "{configurator_path}"')

def main_menu():
    '''Create the main menu for the application.'''
    logging.info('main_menu started')
    root = tk.Tk()
    root.title(f"Configurator Admin Utility {APP_VERSION}")
    root.geometry("420x420")

    tk.Label(root, text="Marlin Configurator Admin", font=("Arial", 14, "bold")).pack(pady=12)
    tk.Button(root, text="Launch Configurator", width=32, command=launch_configurator).pack(pady=18)
    tk.Frame(root, height=2, bd=0, relief="sunken", bg="#888").pack(fill="x", padx=10, pady=8)    
    tk.Button(root, text="Add/Delete/Modify Flash Cards", width=32, command=FlashCardEditor).pack(pady=6)
    tk.Button(root, text="Edit Workflow Checklist", width=32, command=edit_workflow).pack(pady=6)
    tk.Button(root, text="Set Repository Root", width=32, command=prompt_for_repo_root_menu).pack(pady=6)
    tk.Frame(root, height=2, bd=0, relief="sunken", bg="#888").pack(fill="x", padx=10, pady=8)
    tk.Button(root, text="Display License", width=32, command=display_license).pack(pady=6)
    tk.Button(root, text="Exit", width=10, command=root.destroy).pack(pady=2)
    root.mainloop()

def prompt_for_repo_root_menu():
    '''Prompt the user to set the repository root directory.'''
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Set Repository Root", "Please select the repository root directory.")
    new_path = filedialog.askdirectory(title="Select Repository Root")
    if new_path:
        set_repo_root(new_path)
        messagebox.showinfo("Repository Root Set", f"Repository root set to:\n{new_path}")
        return new_path
    else:
        messagebox.showwarning("No Selection", "No directory selected. Repository root not changed.")
        return None
 

class TextWindow(tk.Toplevel):
    '''A window for displaying text content.'''
    def __init__(self, title, text, linkify=False):
        super().__init__()
        self.title(title)
        self.geometry("700x600")
        text_widget = tk.Text(self, wrap="word")
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")
        if linkify:
            self.linkify_text(text_widget)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)

    def linkify_text(self, text_widget):
        '''Make URLs in the text clickable.'''
        # Find URLs in the text and make them clickable
        text = text_widget.get("1.0", "end-1c")
        url_pattern = re.compile(r"https?://[\w./?=#%&+\-]+")
        for match in url_pattern.finditer(text):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            text_widget.tag_add("url", start, end)
        text_widget.tag_config("url", foreground="blue", underline=1)
        text_widget.tag_bind("url", "<Button-1>", lambda e: self.open_url(text_widget, e))

    def open_url(self, text_widget, event):
        '''Open the clicked URL in a web browser.'''
        index = text_widget.index(f"@{event.x},{event.y}")
        # Find the start and end of the tagged region
        tag_ranges = text_widget.tag_ranges("url")
        for i in range(0, len(tag_ranges), 2):
            start = tag_ranges[i]
            end = tag_ranges[i+1]
            if text_widget.compare(index, ">=", start) and text_widget.compare(index, "<", end):
                url = text_widget.get(start, end)
                webbrowser.open(url)
                break
            
# --- Flash Card Editor ---
class FlashCardEditor(tk.Toplevel):
    '''A window for editing flash cards.'''
    def __init__(self):
        super().__init__()
        self.title("Flash Card Editor")
        self.geometry("600x500")
        self.cards = self.load_cards()
        self.index = 0 if self.cards else -1
        self.create_widgets()
        self.show_card()

    def load_cards(self):
        '''Load flash cards from the JSON file.'''
        try:
            with open(FLASH_CARDS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_cards(self):
        '''Save flash cards to the JSON file.'''
        try:
            with open(FLASH_CARDS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.cards, f, indent=2, ensure_ascii=False)
            self.show_autoclose_popup("Flash cards saved.", duration=3000)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def show_autoclose_popup(self, message, duration=2000):
        '''Show a popup message that closes after a delay.'''
        popup = tk.Toplevel(self)
        popup.title("Saved")
        popup.geometry("250x80")
        popup.resizable(False, False)
        tk.Label(popup, text=message, font=("Arial", 12)).pack(expand=True, fill="both", pady=18)
        popup.after(duration, popup.destroy)

    def create_widgets(self):
        '''Create the widgets for the flash card editor.'''
        self.fields = {}
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Define which fields are multi-line
        multiline_fields = {"description", "instructions", "warnings"}
        field_list = ["objective", "description", "instructions", "files to edit", "related_settings", "docs_link", "warnings"]
        for i, field in enumerate(field_list):
            tk.Label(frame, text=field+":").grid(row=i, column=0, sticky="ne")
            if field in multiline_fields:
                text_widget = tk.Text(frame, width=60, height=4, wrap="word")
                text_widget.grid(row=i, column=1, sticky="we", pady=2)
                # Add a vertical scrollbar
                scroll = tk.Scrollbar(frame, command=text_widget.yview)
                text_widget.config(yscrollcommand=scroll.set)
                scroll.grid(row=i, column=2, sticky="nsw")
                self.fields[field] = text_widget
            else:
                entry = tk.Entry(frame, width=60)
                entry.grid(row=i, column=1, sticky="w", pady=2)
                self.fields[field] = entry
        frame.grid_columnconfigure(1, weight=1)
        # Navigation and actions
        nav = tk.Frame(self)
        nav.pack(pady=10)
        tk.Button(nav, text="Previous", command=self.prev_card).pack(side="left", padx=5)
        tk.Button(nav, text="Next", command=self.next_card).pack(side="left", padx=5)
        tk.Button(nav, text="Add New", command=self.add_card).pack(side="left", padx=5)
        tk.Button(nav, text="Delete", command=self.delete_card).pack(side="left", padx=5)
        tk.Button(nav, text="Save", command=self.save_current_and_all).pack(side="left", padx=5)
        tk.Button(nav, text="Close", command=self.destroy).pack(side="left", padx=5)

    def show_card(self):
        '''Show the current flash card.'''
        if self.index == -1 or not self.cards:
            for widget in self.fields.values():
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                else:
                    widget.delete(0, tk.END)
            return
        card = self.cards[self.index]
        for field, widget in self.fields.items():
            val = card.get(field, "")
            if isinstance(val, list):
                val = ", ".join(str(x) for x in val)
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", val)
            else:
                widget.delete(0, tk.END)
                widget.insert(0, val)
        self.title(f"Flash Card Editor ({self.index+1}/{len(self.cards)})")

    def save_current_and_all(self):
        '''Save the current flash card and all changes.'''
        if self.index == -1:
            return
        card = self.cards[self.index]
        for field, widget in self.fields.items():
            if isinstance(widget, tk.Text):
                val = widget.get("1.0", tk.END).strip()
            else:
                val = widget.get()
            # Try to keep lists as lists
            if field in ("instructions", "related_settings"):
                val = [x.strip() for x in val.split(",") if x.strip()]
            card[field] = val
        self.cards[self.index] = card
        self.save_cards()

    def next_card(self):
        '''Move to the next flash card.'''
        if self.cards and self.index < len(self.cards) - 1:
            self.save_current_and_all()
            self.index += 1
            self.show_card()

    def prev_card(self):
        '''Move to the previous flash card.'''
        if self.cards and self.index > 0:
            self.save_current_and_all()
            self.index -= 1
            self.show_card()

    def add_card(self):
        '''Add a new flash card.'''
        self.save_current_and_all()
        new_card = {field: "" for field in self.fields}
        self.cards.append(new_card)
        self.index = len(self.cards) - 1
        self.show_card()

    def delete_card(self):
        '''Delete the current flash card.'''
        if self.cards and self.index != -1:
            del self.cards[self.index]
            if self.index >= len(self.cards):
                self.index = len(self.cards) - 1
            if not self.cards:
                self.index = -1
            self.show_card()

if __name__ == "__main__":
    logging.info('configurator_admin.py starting as __main__')
    main_menu()
