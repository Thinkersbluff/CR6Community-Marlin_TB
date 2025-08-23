# Runtime hook to set TCL/TK environment variables when running from a PyInstaller bundle
import os
import sys

# If running as a bundle, sys._MEIPASS points to the temporary extraction folder
if hasattr(sys, '_MEIPASS'):
    base = sys._MEIPASS
    # If we bundled tcl/tk into datas under 'tcl' and 'tk', set env vars
    tcl_dir = os.path.join(base, 'tcl')
    tk_dir = os.path.join(base, 'tk')
    if os.path.isdir(tcl_dir):
        # The TCL_LIBRARY should point to the 'tcl' dir that contains tcl8.x
        os.environ.setdefault('TCL_LIBRARY', tcl_dir)
    if os.path.isdir(tk_dir):
        os.environ.setdefault('TK_LIBRARY', tk_dir)
