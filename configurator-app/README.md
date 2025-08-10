
# Marlin Configurator App

A web-based tool for viewing and editing Marlin configuration files (`Configuration.h`, `Configuration_adv.h`, `.ini`, `.txt`).

## Features

- **Load a Configuration File**: Upload a local file or paste a URL (GitHub links auto-convert to raw).
- **Edit and Filter Instantly**: The editor and filtering controls appear as soon as a file is loaded.
- **Filtering Controls**:
  - **Hide Comments**: Hide all comment lines for a cleaner view.
  - **Topic Filter**: Filter by topic (Nozzle, Bed, Motors, Endstops, Enable, #define Settings, Commented #define).
    - **Commented #define**: Shows only commented-out `#define` lines, unless Hide Comments is checked.
  - **Keyword Filter**: Type to filter lines by keyword.
  - **View in Context**: Select a line in the filtered view and click to jump to that line in the full document.
- **Download Modified File**: Save your changes with a filename that includes the original name and a date-time tag.

## How to Use


1. **Start the App**
   - Run:
     ```bash
     .venv/bin/python configurator-app/app.py
     ```
   - Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

2. **Load a Configuration File**
   - Upload a Marlin config file (`.h`, `.ini`, `.txt`) or paste a URL.
   - Click **Load**.

3. **Edit and Filter**
   - The editor and controls appear automatically.
   - Use Hide Comments, Topic Filter, Keyword Filter, and View in Context as needed.
   - Make changes directly in the editor.

4. **Download Modified File**
   - Click **Download Modified Config** to save your changes. The downloaded file will have a date-time tag in its name.

5. **Rename and Copy to Marlin Folder**
   - After downloading, rename the tagged file you want to use to remove the date-time tag (e.g., `Configuration_20250810-153000.h` → `Configuration.h`).
   - Copy the renamed file from your Downloads folder to overwrite the corresponding file in the `./Marlin` folder of your firmware source tree.
   - Repeat for both `Configuration.h` and `Configuration_adv.h` as needed.
   - When you are satisfied that both files are correctly configured, proceed to build your customized `firmware.bin`.

## Customizing Filters

To add, modify, or remove topic filters:

1. Edit `configurator-app/templates/index.html`.
2. Update the `<select id="topicFilter">` dropdown for new options.
3. Update the `keywords` object in the `filterTopic()` function for new topic keywords.

## Code Structure

- **Frontend/UI**: `configurator-app/templates/index.html` (HTML, Bootstrap, JavaScript)
- **Backend**: `configurator-app/app.py` (Flask routes, file handling, download logic)

---

For questions or improvements, open an issue or contact the repository owner.
