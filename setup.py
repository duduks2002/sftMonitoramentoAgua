import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "includes": ["tkinter", "time", "csv", "serial", "threading"],
    "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Monitoramento NIvel de Agua",
    version="0.1",
    description="Projeto criado por Edward para TCC, para fins de estudo!",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)