import subprocess

subprocess.call(
    "python -m PyInstaller --noconfirm --onefile \"puller.py\"",
    shell=True)