# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

hiddenimports = (
    collect_submodules("pini_desktop")
    + collect_submodules("packages")
    + collect_submodules("ortools")
)

binaries = (
    collect_dynamic_libs("ortools")
)

a = Analysis(
    ["apps/desktop/main.py"],
    pathex=[
        ".",
        "apps/desktop",
    ],
    binaries=binaries,
    datas=[
        ("assets", "assets"),
        ("database", "database"),
        ("docs", "docs"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "pytest",
        "unittest",
        "matplotlib.tests",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PiniPlanner",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PiniPlanner",
)