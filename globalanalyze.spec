# globalanalyze.spec
block_cipher = None

a = Analysis(
    ['main.py', 'report.py', 'Preliminary_sifting.py', 'other_point.py', 'order_fun.py', 'is_free_befor.py', 'global_point.py', 'analyze_fie.py','print_warning.py'],
    pathex=['D:/code/c++/project'],  # 替换为项目目录的路径
    binaries=[(r'D:/work/conda/Lib/site-packages/clang/native/libclang.dll', '.')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
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
    name='globalanalyze',  # 更新工具名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True  # 控制台窗口
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='globalanalyze'  # 更新工具名称
)