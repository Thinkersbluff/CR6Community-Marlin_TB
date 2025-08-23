# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['configurator.py'],
    pathex=['.'],
    binaries=[('/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0', '.')],
    datas=[
        ('/usr/share/tcltk/tcl8.6', 'tcl'),  # (source, dest in bundle)
        ('/usr/share/tcltk/tk8.6', 'tk'),
        ('flash_cards.json', '.'), 
        ('workflow.json', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hooks/set_tcltk_paths.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='configurator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
