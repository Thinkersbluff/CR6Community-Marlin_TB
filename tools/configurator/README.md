# Marlin Configurator GUI

A Tkinter-based graphical tool for safely editing Marlin firmware configuration files, with onboarding, workflow guidance, and PlatformIO environment management.

## Features
- Select printer configuration examples from dropdown
- Step-by-step workflow menu with onboarding objectives (flash cards)
- Keyword filtering for configuration lines
- Safe file operations (prevents overwriting example configs)
- PlatformIO `default_envs` management
- Conditional visibility and navigation per workflow step

## UI Structure
```
Main Window
├── Workflow Menu (left)
│   ├── Step labels & descriptions
│   └── Navigation buttons (Previous, Next, Start Again)
└── Content Frame (right)
    ├── Default Env Label
    ├── Flash Card Frame
    │   ├── Picklist label & dropdown (printer example)
    │   ├── Objective dropdown
    │   ├── Flash Card Display Frame
    │   │   ├── Objective text label
    │   │   └── Details label
    │   └── Keywords Frame (checkboxes)
    ├── Editor Frame
    │   ├── Current file label
    │   ├── Edit label
    │   ├── Canvas (scrollable)
    │   │   └── Lines Frame
    │   │       └── Filter Frame (keyword entry & apply button)
    │   └── Scrollbar
    └── Controls Frame (file operation buttons)
```

### Frame/Widget Structure

- `self.content_frame`: Main container for the right-side content (everything except the workflow menu)
    - `self.default_envs_label`: Label showing the current PlatformIO environment
    - `self.flash_frame`: Contains the onboarding/flash card area
        - `self.picklist_label` and `self.example_menu`: "Select printer configuration example" label and dropdown
        - `self.objective_menu`: "Select objective" dropdown
        - `self.flash_card_display_frame`: Contains the flash card text and details
            - `self.flash_card_text_label`: Flash card objective text
            - `self.flash_card_details_label`: Flash card details
        - `self.keywords_frame`: Contains keyword filter checkboxes for the flash card
    - `self.editor_frame`: Contains the file editor area
        - `self.current_file_label`: Shows the current file path
        - `self.edit_label`: Label for the editor
        - `self.canvas`: Scrollable area for editing lines
            - `self.lines_frame`: Frame inside the canvas for line widgets
                - `self.filter_frame`: Contains keyword filter entry and apply button
                    - `self.keyword_label`, `self.keyword_entry`, `self.keyword_apply_button`: Keyword filter controls
        - `self.scrollbar`: Scrollbar for the editor
    - `self.controls_frame`: Contains file operation buttons
        - `self.load_base_button`, `self.load_example_button`, `self.load_selected_button`, `self.save_button`: File operation buttons
- `self.workflow_frame`: Left-side frame for the workflow menu
    - Workflow step labels and descriptions
    - Navigation buttons (`self.prev_step_button`, `self.next_step_button`, `self.start_again_button`)

## How It Works
- **Workflow Menu:** Guides users through configuration steps, showing/hiding controls as needed.
- **Flash Card Area:** Presents onboarding objectives, details, and recommended keywords for filtering.
- **Editor:** Allows safe editing of Marlin configuration files, with keyword filtering and file path display.
- **Controls:** Buttons for loading/saving configs and updating PlatformIO environment.

## Getting Started
1. Install Python 3 and Tkinter (`sudo apt install python3-tk`)
2. Run: `python3 configurator_gui.py` from the `tools/configurator` directory
3. Follow the workflow menu and use the flash card area for onboarding and guidance

## File Safety
- The app prevents overwriting example configs in the `config/` folder
- All edits to Marlin/Configuration.h are tracked and can be saved safely

## PlatformIO Integration
- The app can update the `default_envs` value in `platformio.ini` using the selected example's environment

## Customization
- Workflow steps and control visibility are defined in `ui.json`
- Onboarding objectives are defined in `flash_cards.json`

## License
(C) Thinkersbluff, 2025
