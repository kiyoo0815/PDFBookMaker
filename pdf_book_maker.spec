# -*- mode: python ; coding: utf-8 -*-


analysis = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("assets/fonts/malgun.ttf", "assets/fonts"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

python_archive = PYZ(analysis.pure)

executable = EXE(
    python_archive,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="PDFBookMaker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
