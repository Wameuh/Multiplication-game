from cx_Freeze import setup, Executable

base = None

executables = [Executable("menu.py", base=base)]
packages = [
    "idna",
    "numpy",
    "pygame",
    "config",
    "highscores",
    "games",
    "landscape",
    "json",
    "loose",
    "random"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "Multiplications",
    options = options,
    version = "1.0",
    description = 'Jeu des multiplications',
    executables = executables
)