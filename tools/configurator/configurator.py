# Marlin Configuration Tool (C) Thinkersbluff, 2025
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Use this python3 tool to edit the baseline configuration files in ./Marlin
# prior to building your customized firmware
#
# Prerequisites:
#   Install Python 3 (See BUILD_AND_TEST.md for guideance)
#     If you get an ImportError for tkinter when launching the app, install it via your package manager
#      (e.g., sudo apt install python3-tk).
#
# Recommended workflow:
# 
# 1. Plan your edits, according to:
#  - Which printer configuration you wish to target with your build
#  - Whether you plan to modify an existing configuration or start from one of the examples in ./config
#  - Whether you need to create multiple variants of configuration file or just one 
#        (e,g, how many CR6 printer configurations you wish to target and where will you store those files)
#
# 2. Launch the tool, from the .tools/configurator directory:
#       python3 configurator_gui.py
# Then, using this tool:
# 1. Select the applicable printer configuration example from the dropdown menu.
# 2. Select one objective at a time and review the flash card
# 3. Filter the display by selecting the recommended keywords
# 4. Modify the configuration settings as needed.
# 5. Save your changes 
# 6. Copy the platformio.txt field to Platformio.ini
# 7. Build your customized firmware. (See BUILD_AND_TEST.md for guideance)
#
#

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import logging
import subprocess
# Import flash card logic
from flash_cards import load_flash_cards

# Setup logging to file
logging.basicConfig(filename='configurator_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config'))
MARLIN_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Marlin/Configuration.h'))

# Find all example folders containing 'cr6' in their name
example_folders = [f for f in os.listdir(CONFIG_DIR) if os.path.isdir(os.path.join(CONFIG_DIR, f)) and 'cr6' in f]

class ConfiguratorApp(tk.Tk):
    '''Main application class for the Marlin Configurator GUI.'''
    def __init__(self):
        logging.info('ConfiguratorApp __init__ started')
        super().__init__()
        logging.info('Tkinter __init__ started')
        self.title('Marlin Configurator')
        self.geometry('1280x1024')
        
        # Picklist frame
        self.picklist_frame = tk.Frame(self, bd=1, relief='groove')
        logging.info('picklist_frame created')
        self.picklist_frame.pack(side='top', fill='x', padx=10, pady=(10,0))
        logging.info('picklist_frame packed')
        self.picklist_label = tk.Label(self.picklist_frame, text='Select printer configuration example:', font=('Arial', 10, 'bold'), anchor='w', justify='left')
        logging.info('picklist_label created')
        self.picklist_label.pack(side='left', anchor='w')
        logging.info('picklist_label packed')
        self.selected_example = tk.StringVar()
        self.example_menu = ttk.Combobox(self.picklist_frame, textvariable=self.selected_example, values=example_folders, state='readonly', width=35 )
        logging.info('example_menu created')
        self.example_menu.pack(side='left', padx=(10,0), anchor='w')
        logging.info('example_menu packed')
        self.example_menu.bind('<<ComboboxSelected>>', lambda e: self.on_example_select(self.selected_example.get()))
        logging.info('example_menu bind complete')

        # Main content frame
        self.content_frame = tk.Frame(self)
        logging.info('content_frame created')
        self.content_frame.pack(side='top', fill='both', expand=True)
        logging.info('content_frame packed')

        # Default envs frame
        self.default_envs_frame = tk.Frame(self.content_frame, bd=1, relief='ridge')
        logging.info('default_envs_frame created')
        self.default_envs_frame.pack(fill='x', padx=10, pady=2)
        logging.info('default_envs_frame packed')
        self.default_envs_label = tk.Label(self.default_envs_frame, text='Current default_envs:', font=('Arial', 10, 'bold'), fg='purple', anchor='w', justify='left')
        logging.info('default_envs_label created')
        self.default_envs_label.pack(side='left', padx=(0,10))
        logging.info('default_envs_label packed')
        self.default_envs_value = tk.StringVar()
        self.default_envs_entry = tk.Entry(self.default_envs_frame, textvariable=self.default_envs_value, width=40, state='readonly', font=('Arial', 10))
        logging.info('default_envs_entry created')
        self.default_envs_entry.pack(side='left', padx=(0,10))
        logging.info('default_envs_entry packed')
        self.example_env_value = tk.StringVar()
        self.example_env_label = tk.Label(self.default_envs_frame, textvariable=self.example_env_value, font=('Arial', 10), fg='gray', anchor='w', justify='left')
        logging.info('example_env_label created')
        self.example_env_label.pack(side='left', padx=(0,10))
        logging.info('example_env_label packed')
        self.copy_env_button = tk.Button(self.default_envs_frame, text='Copy env to platformio.ini', command=self.copy_env_to_platformio)
        logging.info('copy_env_button created')
        self.copy_env_button.pack(side='left', padx=(0,10))
        logging.info('copy_env_button packed')

        # Main row frame
        self.main_row_frame = tk.Frame(self.content_frame)
        logging.info('main_row_frame created')
        self.main_row_frame.pack(fill='both', expand=True)
        logging.info('main_row_frame packed')
        self.workflow_frame = tk.Frame(self.main_row_frame)
        logging.info('workflow_frame created')
        self.workflow_frame.pack(side='left', fill='y', padx=10, pady=10)
        logging.info('workflow_frame packed')
        self.workflow_checkboxes = []
        self.workflow_desc_labels = []

        self.selected_objective = tk.StringVar()

        self.flash_cards = load_flash_cards()
        logging.info('flash_cards loaded')

     # Flash card frame
        self.flash_frame = tk.Frame(self.main_row_frame, bd=1, relief='groove', width=500)
        logging.info('flash_frame created')
        self.flash_frame.pack(side='left', fill='y', padx=10, pady=5)
        self.flash_frame.pack_propagate(False)
        logging.info('flash_frame packed')
        objectives = [card['objective'] for card in self.flash_cards]
        if objectives:
            self.selected_objective.set(objectives[0])
        self.objective_menu = ttk.Combobox(self.flash_frame, textvariable=self.selected_objective, values=objectives, state='readonly', width=28,  font=('Arial', 10, 'bold'))
        logging.info('objective_menu created')
        self.objective_menu.pack(side='top', fill='x', padx=10, pady=(0,4))
        logging.info('objective_menu packed')
        self.objective_menu.bind('<<ComboboxSelected>>', lambda e: self.on_objective_select(self.selected_objective.get()))
        logging.info('objective_menu bind complete')

        # Flash card display area
        self.flash_card_display_frame = tk.Frame(self.flash_frame, bd=1, relief='ridge', width=500)
        logging.info('flash_card_display_frame created')
        self.flash_card_display_frame.pack(fill='x', padx=10, pady=(8,0))
        self.flash_card_display_frame.pack_propagate(True)
        logging.info('flash_card_display_frame packed')


        self.flash_card_desc_label = tk.Label(self.flash_card_display_frame, text='Description:', font=('Arial', 10), fg='black', justify='left', wraplength=460, anchor='w')
        logging.info('flash_card_desc_label created')
        self.flash_card_desc_label.pack(fill='x')
        logging.info('flash_card_desc_label packed')
        self.flash_card_files_label = tk.Label(self.flash_card_display_frame, text='Files to Edit:', font=('Arial', 10), fg='black', justify='left', wraplength=460, anchor='w')
        logging.info('flash_card_files_label created')
        self.flash_card_files_label.pack(fill='x')
        logging.info('flash_card_files_label packed')
        self.flash_card_instructions_label = tk.Label(self.flash_card_display_frame, text='Instructions:', font=('Arial', 10), fg='black', justify='left', wraplength=460, anchor='w')
        logging.info('flash_card_instructions_label created')
        self.flash_card_instructions_label.pack(fill='x')
        logging.info('flash_card_instructions_label packed')
        self.flash_card_related_label = tk.Label(self.flash_card_display_frame, text='Related Topics:', font=('Arial', 10), fg='black', justify='left', wraplength=460, anchor='w')
        logging.info('flash_card_related_label created')
        self.flash_card_related_label.pack(fill='x')
        logging.info('flash_card_related_label packed')
        self.flash_card_docs_label = tk.Label(self.flash_card_display_frame, text='More Info:', font=('Arial', 10), fg='blue', justify='left', wraplength=460, anchor='w', cursor='hand2')
        logging.info('flash_card_docs_label created')
        self.flash_card_docs_label.pack(fill='x')
        logging.info('flash_card_docs_label packed')
        self.flash_card_warnings_label = tk.Label(self.flash_card_display_frame, text='Warnings:', font=('Arial', 10), fg='red', justify='left', wraplength=460, anchor='w')
        logging.info('flash_card_warnings_label created')
        self.flash_card_warnings_label.pack(fill='x')
        logging.info('flash_card_warnings_label packed')

        # Load flash cards using the shared function
        self.flash_cards = load_flash_cards()
        logging.info('flash_cards loaded')

        # Objective Keywords subframe
        self.keywords_frame = tk.Frame(self.flash_frame)
        logging.info('keywords_frame created')
        self.keywords_frame.pack(fill='x', padx=10, pady=2)
        logging.info('keywords_frame packed')
        self.update_flash_card_display()
        logging.info('update_flash_card_display called after all flash card widgets created')

        ui_json_path = os.path.join(os.path.dirname(__file__), 'ui.json')
        with open(ui_json_path, 'r', encoding='utf-8') as f:
            self.workflow_data = json.load(f)["workflow"]
        logging.info('workflow_data loaded')
        self.workflow_step = 0
        self.workflow_completed = [False] * len(self.workflow_data)
        for i, step in enumerate(self.workflow_data):
            cb = tk.Checkbutton(self.workflow_frame, text=step['step'], variable=tk.BooleanVar(value=False), font=('Arial', 12), anchor='w', justify='left')
            logging.info('workflow checkbox created for step: %s', step["step"])
            cb.pack(fill='x', pady=(2,0), anchor='w')
            logging.info('workflow checkbox packed for step: %s', step["step"])
            self.workflow_checkboxes.append(cb)
            desc_label = tk.Label(self.workflow_frame, text=step.get('description', ''), font=('Arial', 9), anchor='w', justify='left', wraplength=260, fg='gray')
            logging.info('workflow desc_label created for step: %s', step["step"])
            desc_label.pack(fill='x', pady=(0,8), anchor='w')
            logging.info('workflow desc_label packed for step: %s', step["step"])
            self.workflow_desc_labels.append(desc_label)
            
    # Editor frame
        self.editor_frame = tk.Frame(self.main_row_frame, bd=1, relief='groove')
        logging.info('editor_frame created')
        self.editor_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        logging.info('editor_frame packed')
                # Config file selection dropdown
        self.config_files = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Marlin/Configuration.h')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Marlin/Configuration_adv.h'))
        ]
        self.config_file_label = tk.Label(
            self.editor_frame,
            text="Select file to edit:",
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        self.config_file_label.pack(fill='x', padx=2, pady=(8,2))

        self.config_file_names = [os.path.basename(f) for f in self.config_files]
        self.selected_config_file = tk.StringVar(value="")
        self.config_file_menu = ttk.Combobox(
            self.editor_frame,
            textvariable=self.selected_config_file,
            values=self.config_file_names,
            state='readonly',
            width=20
        )
        self.config_file_menu.pack(fill='x', padx=2, pady=2)
        self.config_file_menu.bind('<<ComboboxSelected>>', lambda e: self.on_config_file_select())
        self.opened_config_path = self.config_files[0]  # Track currently opened file
        self.current_file_label = tk.Label(self.editor_frame, text='', font=('Arial', 10, 'bold'), fg='darkgreen', anchor='w', justify='left')
        logging.info('current_file_label created')
        self.current_file_label.pack(fill='x', padx=2, pady=2)
        logging.info('current_file_label packed')
        self.edit_label = tk.Label(self.editor_frame, text='Edit Marlin/Configuration.h (filtered by keyword):', font=('Arial', 10))
        logging.info('edit_label created')
        self.edit_label.pack(anchor='w')
        logging.info('edit_label packed')

        # Controls subframe
        self.controls_frame = tk.Frame(self.editor_frame)
        logging.info('controls_frame created')
        self.controls_frame.pack(fill='x', padx=2, pady=2)
        logging.info('controls_frame packed')
        self.load_base_button = tk.Button(self.controls_frame, text='Load Base (default)', command=self.load_base_config)
        logging.info('load_base_button created')
        self.load_base_button.pack(side='left', padx=5)
        logging.info('load_base_button packed')
        self.load_example_button = tk.Button(self.controls_frame, text='Load Config Example', command=self.load_example_dialog)
        logging.info('load_example_button created')
        self.load_example_button.pack(side='left', padx=5)
        logging.info('load_example_button packed')
        self.load_selected_button = tk.Button(self.controls_frame, text='Load Other...', command=self.load_other_file)
        logging.info('load_selected_button created')
        self.load_selected_button.pack(side='left', padx=5)
        logging.info('load_selected_button packed')
        self.save_edit_button = tk.Button(self.controls_frame, text='Save Edit', command=self.save_edit)
        logging.info('save_edit_button created')
        self.save_edit_button.pack(side='left', padx=15)
        logging.info('save_edit_button packed')
        self.save_file_button = tk.Button(self.controls_frame, text='Save File', command=self.save_with_prompt)
        logging.info('save_file_button created')
        self.save_file_button.pack(side='left', padx=5)
        logging.info('save_file_button packed')
        self.build_firmware_button = tk.Button(self.controls_frame, text='Build Firmware', command=self.build_firmware)
        logging.info('build_firmware_button created')
        self.build_firmware_button.pack(side='left', fill='x', padx=15)
        logging.info('build_firmware_button packed')

        # Keyword filter subframe
        self.filter_frame = tk.Frame(self.editor_frame)
        logging.info('filter_frame created')
        self.filter_frame.pack(side='top', anchor='w', fill='x', pady=(10, 0))
        logging.info('filter_frame packed')
        self.keyword_label = tk.Label(self.filter_frame, text='Keyword filter:')
        logging.info('keyword_label created')
        self.keyword_label.pack(side='left')
        logging.info('keyword_label packed')
        self.keyword_var = tk.StringVar()
        self.keyword_entry = tk.Entry(self.filter_frame, textvariable=self.keyword_var)
        logging.info('keyword_entry created')
        self.keyword_entry.pack(side='left', padx=5)
        logging.info('keyword_entry packed')
        # Bind filter to key release for live filtering
        self.keyword_entry.bind('<KeyRelease>', lambda e: self.apply_keyword_filter())
        logging.info('keyword_entry bound to KeyRelease for live filtering')
        self.view_in_context_button = tk.Button(self.filter_frame, text='View in Context', command=self.view_in_context)
        logging.info('view_in_context_button created')
        self.view_in_context_button.pack(side='left', padx=5)
        logging.info('view_in_context_button packed')
        self.hide_comments_var = tk.BooleanVar(value=False)
        self.hide_comments_check = tk.Checkbutton(
            self.filter_frame,
            text="Hide Comments",
            variable=self.hide_comments_var,
            command=self.apply_keyword_filter
        )
        self.hide_comments_check.pack(side='left', padx=5)

        # Canvas and scrollbar
        self.canvas = tk.Canvas(self.editor_frame)
        logging.info('canvas created')
        self.scrollbar = tk.Scrollbar(self.editor_frame, orient='vertical', command=self.canvas.yview)
        logging.info('scrollbar created')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        logging.info('scrollbar packed')
        self.canvas.pack(side='left', fill='both', expand=True)
        logging.info('canvas packed')
        self.lines_frame = tk.Frame(self.canvas)
        logging.info('lines_frame created')
        self.lines_frame_id = self.canvas.create_window((0, 0), window=self.lines_frame, anchor='nw')
        logging.info('lines_frame_id created')

        # Initialize editor state variables
        self.modified_entries = []
        self.displayed_indices = []
        self.lines = []
        self.base_lines = []

    def on_config_file_select(self):
        '''Handle config file dropdown selection.'''
        selected_name = self.selected_config_file.get()
        idx = self.config_file_names.index(selected_name)
        self.opened_config_path = self.config_files[idx]
        self.edit_label.config(text=f'Edit Marlin/{selected_name} (filtered by keyword):')
        self.load_config_file(self.opened_config_path)

    def copy_env_to_platformio(self):
        '''Copy the example environment value to platformio.ini.'''
        logging.info('copy_env_to_platformio called')
        folder = self.selected_example.get()
        env_file = os.path.join(CONFIG_DIR, folder, 'platformio-environment.txt') if folder else None
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../platformio.ini'))
        if not folder or not os.path.isfile(env_file):
            messagebox.showerror('Error', 'No example environment value found.')
            return
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                env_value = f.readline().strip()
            # Read all lines, replace default_envs line
            with open(ini_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            replaced = False
            for line in lines:
                if line.strip().startswith('default_envs'):
                    new_lines.append(f'default_envs = {env_value}\n')
                    replaced = True
                else:
                    new_lines.append(line)
            if not replaced:
                new_lines.append(f'default_envs = {env_value}\n')
            with open(ini_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            messagebox.showinfo('Copied', f'platformio.ini updated with env: {env_value}')
            self.update_default_envs_label()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to copy env: {e}')
        self.update_default_envs_label()
        logging.info('update_default_envs_label called')

    def show_lines(self, highlight_line_num=None, scroll_to_index=None):
        '''Display lines in the editor area, filtered by match attribute if present. Optionally highlight a line and scroll to a given index.'''
        logging.info('show_lines called')
        if self.lines_frame is None:
            return
        # Clear previous widgets
        for widget in self.lines_frame.winfo_children():
            if widget != self.filter_frame:
                widget.destroy()
        self.modified_entries = []
        self.displayed_indices = []
        # Always use self.base_lines for filtering and editing
        if self.base_lines and any('match' in line for line in self.base_lines):
            lines_to_display = [line for line in self.base_lines if line.get('match', True)]
        elif self.base_lines:
            lines_to_display = self.base_lines
        else:
            lines_to_display = self.lines
        logging.info("Displaying %d lines, first line_num: %s", len(lines_to_display), lines_to_display[0]['line_num'] if lines_to_display else 'None')
        max_lines = 200  # Limit for testing large files
        for idx, line in enumerate(lines_to_display[:max_lines]):
            entry = tk.Entry(self.lines_frame, width=120)
            entry.insert(0, line["content"])
            entry.pack(fill='x', padx=2, pady=1)
            self.modified_entries.append(entry)
            self.displayed_indices.append(line.get('line_num', idx))
            # Highlight if needed
            if highlight_line_num is not None and line.get('line_num', idx) == highlight_line_num:
                entry.config(bg='yellow')
        self.lines_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.lines_frame_id))
        self.update_idletasks()
        # Scroll so that the highlighted line is in the desired position
        if highlight_line_num is not None:
            try:
                idx = [line.get('line_num', i) for i, line in enumerate(lines_to_display[:max_lines])].index(highlight_line_num)
                if scroll_to_index is not None:
                    total = len(lines_to_display[:max_lines])
                    frac = max(0, min(1, (idx - scroll_to_index) / max(1, total)))
                    self.after(10, lambda: self.canvas.yview_moveto(frac))
                else:
                    self.after(10, lambda: self.canvas.yview_moveto(0))
            except Exception as e:
                logging.warning('Could not scroll to highlighted line: %s', e)
        else:
            self.after(10, lambda: self.canvas.yview_moveto(0))

    def apply_keyword_filter(self):
        '''Filter displayed lines based on keywords, text input, and hide comments option.'''
        logging.info('apply_keyword_filter called')
        if not self.base_lines:
            return
        keywords = [kw for kw, var in getattr(self, 'keyword_vars', []) if var.get()]
        filter_text = self.keyword_var.get().strip().lower()
        hide_comments = self.hide_comments_var.get()

        for line in self.base_lines:
            match = True
            if keywords:
                match = any(kw.lower() in line["content"].lower() for kw in keywords)
            if filter_text:
                match = match and (filter_text in line["content"].lower())
            if hide_comments:
                stripped = line["content"].strip()
                # Hide lines that start with // or * or /* are empty or only whitespace
                if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*") or stripped == "":
                    match = False
            line['match'] = match
        self.show_lines()

    def view_in_context(self):
        '''Show +/- 99 lines around the selected line, scroll to selected line, and highlight it.'''
        logging.info('view_in_context called')
        # Find which entry has focus
        selected_idx = None
        for i, entry in enumerate(self.modified_entries):
            if entry == self.focus_get():
                selected_idx = i
                break
        if selected_idx is None:
            messagebox.showinfo('No Selection', 'Please click on a line to select it before using View in Context.')
            return
        # Get the line number in the full file
        if selected_idx >= len(self.displayed_indices):
            messagebox.showerror('Error', 'Selected line index out of range.')
            return
        line_num = self.displayed_indices[selected_idx]
        logging.info('view_in_context: selected line_num=%s', line_num)
        # Set all lines to display False, then set +/- 99 to True
        for line in self.base_lines:
            line['match'] = False
        start = max(0, line_num - 99)
        end = min(len(self.base_lines), line_num + 100)
        for i in range(start, end):
            self.base_lines[i]['match'] = True
        self.show_lines(highlight_line_num=line_num, scroll_to_index=10)

    def load_other_file(self):
        '''Load a different configuration file.'''
        logging.info('load_other_file called')
        file_path = filedialog.askopenfilename(
            title='Load Configuration File',
            filetypes=[('Header Files', '*.h'), ('All Files', '*.*')],
            initialdir=os.path.dirname(MARLIN_CONFIG_PATH)
        )
        if file_path:
            self.load_config_file(file_path)

    def load_config_file(self, file_path=None, error_message=None):
        '''Load the specified configuration file.'''
        if file_path is None:
            file_path = self.opened_config_path if hasattr(self, 'opened_config_path') else self.config_files[0]
        logging.info('load_config_file called with file_path: %s', file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_lines = f.readlines()
            self.lines = [
                {"line_num": i, "content": line.rstrip('\n'), "display": True, "edited": False}
                for i, line in enumerate(file_lines)
            ]
            self.base_lines = self.lines.copy()
            self.show_lines()
            self.current_file_label.config(text=file_path)
            self.opened_config_path = file_path
        except Exception as e:
            msg = error_message if error_message else f'Failed to load: {e}'
            messagebox.showerror('Error', msg)

    def load_base_config(self):
        '''Load the selected config file into the editor, only if a config example is selected.'''
        logging.info('load_base_config called')
        self.load_config_file(self.opened_config_path, error_message='Failed to load base Marlin configuration file.')

    def load_example_dialog(self):
        '''Load an example configuration file.'''
        current_example = self.selected_example.get()
        if not current_example or current_example not in example_folders:
            messagebox.showwarning('Select Example', 'Please select a printer configuration example before loading an example config.')
            return
        folder = simpledialog.askstring('Load Example', 'Enter example folder name:', initialvalue=current_example)
        if folder and folder in example_folders:
            example_path = os.path.join(CONFIG_DIR, folder, 'Configuration.h')
            self.load_config_file(example_path)
        elif folder:
            messagebox.showerror('Error', f'Example folder not found: {folder}')

    def save_edit(self):
        """
        Save edits from displayed lines into self.base_lines and self.lines, marking edited lines.
        Only lines currently displayed and changed will be updated and marked as edited.
        """
        logging.info('save_edit called')
        if not self.base_lines or not self.modified_entries or not self.displayed_indices:
            messagebox.showwarning('No file loaded', 'No file is loaded or no lines are displayed.')
            return
        for i, idx in enumerate(self.displayed_indices):
            entry_val = self.modified_entries[i].get()
            # Update base_lines
            for line in self.base_lines:
                if line.get('line_num', None) == idx:
                    if line['content'] != entry_val:
                        line['content'] = entry_val
                        line['edited'] = True
            # Update lines (full file)
            if idx < len(self.lines):
                if self.lines[idx]['content'] != entry_val:
                    self.lines[idx]['content'] = entry_val
                    self.lines[idx]['edited'] = True
        messagebox.showinfo('Edits Saved', 'Your edits have been saved to the full file. Use Save to write the complete file.')
        logging.info('Edits saved to lines')

    def save_with_prompt(self):
        '''Prompt user to save changes to base config or as a new file.'''
        logging.info('save_with_prompt called')
        result = messagebox.askquestion('Save', 'Update base file (Marlin/Configuration.h)?\nChoose No to Save As elsewhere.', icon='question')
        if result == 'yes':
            self.save_base_config()
        else:
            self.save_as_config()

    def save_base_config(self):
        '''Save changes to the currently opened config file.'''
        logging.info('save_base_config called')
        try:
            content = '\n'.join(line['content'] for line in self.lines)
            with open(self.opened_config_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo('Saved', f'Configuration updated: {self.opened_config_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save: {e}')

    def save_as_config(self):
        '''Save changes to a new configuration file/location.'''
        logging.info('save_as_config called')
        file_path = filedialog.asksaveasfilename(
            title='Save Configuration As...',
            defaultextension='.h',
            filetypes=[('Header Files', '*.h'), ('All Files', '*.*')],
            initialdir=os.path.dirname(self.opened_config_path),
            initialfile=os.path.basename(self.opened_config_path)
        )
        if file_path:
            config_dir_abs = os.path.abspath(CONFIG_DIR)
            file_path_abs = os.path.abspath(file_path)
            if file_path_abs.startswith(config_dir_abs):
                messagebox.showerror('Error', 'Cannot overwrite example config files.')
                return
            try:
                content = '\n'.join(line['content'] for line in self.lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo('Saved', f'Configuration saved as {file_path}')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save: {e}')

    def on_objective_select(self, value):
        '''Handle selection of an objective flash card.'''
        logging.info('on_objective_select called with value: %s', value)
        self.selected_objective.set(value)
        # Only update widget contents, never recreate frames/widgets
        self.update_flash_card_display()

    def update_flash_card_display(self):
        '''Update the display of the selected flash card.'''
        logging.info('update_flash_card_display called')
        selected = self.selected_objective.get()
        card = next((c for c in self.flash_cards if c['objective'] == selected), None)
        logging.debug('Flash card selected: %s, card data: %s', selected, card)
        if card:
            self.flash_card_desc_label.config(text=f"Description: {card.get('description', '')}")
            self.flash_card_files_label.config(text=f"Files to edit: {card.get('files to edit', '')}")
            instructions = card.get('instructions', [])
            if instructions:
                instr_text = '\n'.join(f"- {line}" for line in instructions)
                self.flash_card_instructions_label.config(text=f"Instructions:\n{instr_text}")
            else:
                self.flash_card_instructions_label.config(text="Instructions: (none)")
            related = card.get('related_settings', [])
            if related:
                self.flash_card_related_label.config(text=f"Related settings: {', '.join(related)}")
            else:
                self.flash_card_related_label.config(text="Related settings: (none)")
            docs_link = card.get('docs_link', '')
            if docs_link:
                self.flash_card_docs_label.config(text=f"Docs: {docs_link}")
                self.flash_card_docs_label.bind('<Button-1>', lambda e: self.open_docs_link(docs_link))
            else:
                self.flash_card_docs_label.config(text="Docs: (none)")
                self.flash_card_docs_label.unbind('<Button-1>')
            warnings = card.get('warnings', '')
            if warnings:
                self.flash_card_warnings_label.config(text=f"Warnings: {warnings}")
            else:
                self.flash_card_warnings_label.config(text="Warnings: (none)")
        else:
            self.flash_card_desc_label.config(text="Description: ")
            self.flash_card_files_label.config(text="Files to edit: ")
            self.flash_card_instructions_label.config(text="Instructions: ")
            self.flash_card_related_label.config(text="Related settings: ")
            self.flash_card_docs_label.config(text="Docs: ")
            self.flash_card_docs_label.unbind('<Button-1>')
            self.flash_card_warnings_label.config(text="Warnings: ")
        # Only update widget contents, never create frames/widgets
        self.update_flash_card_keywords()

    def open_docs_link(self, url):
        logging.info('open_docs_link called with url: %s', url)
        import webbrowser
        webbrowser.open(url)
        
    def update_default_envs_label(self):
        '''Update the default_envs label and example_env label based on selected example.'''
        logging.info('update_default_envs_label called')
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../platformio.ini'))
        env_value = ""
        try:
            with open(ini_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('default_envs'):
                        env_value = line.strip().split('=',1)[-1].strip()
                        break
        except Exception:
            env_value = '(Could not read platformio.ini)'
        self.default_envs_value.set(env_value)

        # Get example env value if a folder is selected
        folder = self.selected_example.get()
        example_env_value = ''
        env_file = os.path.join(CONFIG_DIR, folder, 'platformio-environment.txt') if folder else None
        if folder and os.path.isfile(env_file):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    example_env_value = f.readline().strip()
            except Exception:
                example_env_value = '(Could not read platformio-environment.txt)'
        else:
            example_env_value = '(not set)'
        self.example_env_value.set(f'Example env: {example_env_value}')

        # Color logic for default_envs_label
        if not folder or example_env_value == '(not set)':
            self.default_envs_label.config(fg='purple')
            self.example_env_label.config(fg='gray')
        elif env_value == example_env_value:
            self.default_envs_label.config(fg='green')
            self.example_env_label.config(fg='green')
        else:
            self.default_envs_label.config(fg='red')
            self.example_env_label.config(fg='red')

    def update_flash_card_keywords(self):
        '''Update flash card keywords UI with checkboxes for selection.'''
        logging.info('update_flash_card_keywords called')
        # Only update widgets inside keywords_frame, never create frames
        for widget in self.keywords_frame.winfo_children():
            widget.destroy()
        self.keyword_vars = []  # Reset keyword_vars for new objective
        selected = self.selected_objective.get()
        card = next((c for c in self.flash_cards if c['objective'] == selected), None)
        keywords = card.get('keywords', []) if card else []
        if keywords:
            tk.Label(self.keywords_frame, text='Recommended keywords:', font=('Arial', 10, 'bold'), fg='navy').pack(anchor='w')
            for kw in keywords:
                var = tk.BooleanVar(value=False)
                cb = tk.Checkbutton(self.keywords_frame, text=kw, variable=var, font=('Arial', 10), anchor='w', command=self.apply_keyword_filter)
                cb.pack(anchor='w')
                self.keyword_vars.append((kw, var))
        else:
            tk.Label(self.keywords_frame, text='No keywords for this objective.', font=('Arial', 10), fg='gray').pack(anchor='w')

    def on_example_select(self, value):
        '''Handle selection of a printer configuration example.'''
        self.selected_example.set(value)
        self.update_default_envs_label()
		# Optionally refresh UI or load config file here

    def build_firmware(self):
        '''Verify readiness and prompt user before running firmware build.'''
        logging.info('build_firmware called')
        # 1. Check that base config file is ready (file exists and has content)
        try:
            with open(MARLIN_CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_content = f.read().strip()
            if not config_content:
                messagebox.showerror('Error', 'Base configuration file is empty!')
                return
        except Exception as e:
            messagebox.showerror('Error', f'Base configuration file not found or unreadable: {e}')
            return

        # 2. Check that selected configuration matches target printer
        selected = self.selected_example.get()
        if not selected:
            messagebox.showerror('Error', 'No printer configuration example selected!')
            return

        # 3. Check that platformio default_env matches example env
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../platformio.ini'))
        env_value = ''
        try:
            with open(ini_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('default_envs'):
                        env_value = line.strip().split('=',1)[-1].strip()
                        break
        except Exception:
            env_value = ''
        folder = selected
        example_env_value = ''
        env_file = os.path.join(CONFIG_DIR, folder, 'platformio-environment.txt') if folder else None
        if folder and os.path.isfile(env_file):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    example_env_value = f.readline().strip()
            except Exception:
                example_env_value = ''

        # Compose summary for user
        summary = f"Base config: {MARLIN_CONFIG_PATH}\nPrinter config: {selected}\nPlatformIO default_envs: {env_value}\nTarget env: {example_env_value}\n\nProceed with build?"
        result = messagebox.askquestion('Build Firmware', summary, icon='question')
        if result != 'yes':
            logging.info('User aborted firmware build')
            return

        # Run build command
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
            build_script = os.path.join(repo_root, 'tools', 'configurator', 'auto_build.py')
            build_cmd = [sys.executable, build_script, 'build']
            logging.info('Running build command: %s in %s', build_cmd, repo_root)
            subprocess.Popen(build_cmd, cwd=repo_root)
            messagebox.showinfo('Build Started', 'Firmware build started in background. Check terminal or logs for output.')
        except Exception as e:
            logging.error('Build failed: %s', e)
            messagebox.showerror('Error', f'Failed to start build: {e}')

if __name__ == "__main__":
    app = ConfiguratorApp()
    app.mainloop()
