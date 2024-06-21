# video_editor.spec

# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['VideoEditor.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('Photo.py', '.'), 
        ('AddText.py', '.'), 
        ('ColorBalance.py', '.'), 
        ('Concatenate.py', '.'), 
        ('Optimizer.py', '.'), 
        ('Importaudio.py', '.'), 
        ('Rotate.py', '.'), 
        ('Speed.py', '.'), 
        ('Subwindow.py', '.'), 
        ('VideoCut.py', '.'), 
        ('Brightness.py', '.'), 
        ('FadeInOut.py', '.'), 
        ('TimeLine.py', '.'), 
        ('VideoSelf.py', '.'), 
        ('Terminal.py', '.'), 
        ('Thread.py', '.'), 
        ('Contrast.py', '.'), 
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VideoEditor'
)