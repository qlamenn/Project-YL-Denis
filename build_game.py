import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=DefenseGame',
    '--add-data=game/assets;game/assets',
    '--clean'
])