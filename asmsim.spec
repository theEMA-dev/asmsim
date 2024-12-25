block_cipher = None

a = Analysis(
    ['ui/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/styles.qss', 'ui'),
        ('ui/assets/*.ico', 'ui/assets'),
        ('ui/assets', 'ui/assets')
    ],
    hiddenimports=[
        'pywinstyles',
        'PyQt5.sip',  # Add missing SIP module
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='asmsim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ui/assets/icon.ico'],
    manifest='builder/windows.manifest',
    manifest_dependencies=[
        "type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' \
        processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'"
    ]
)