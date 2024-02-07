import os
from tkinter import filedialog
import config

admin_path = "C://Users//Nick//Documents//Build"
config.program_path = admin_path
version = 0


def check_file_existence(file_path):
    return os.path.exists(file_path)

def init_path(arg1):
    global program_path
    if arg1 == "server" or "dev":
        config.program_path = admin_path # Achtung! Wenn das nicht von Nick ausgefürht wird, kann es zu Problemen kommen. Einfach den eigenen Pfad hier einfügen.
        version = get_local_version()
        return
    config.program_path = filedialog.askdirectory(title="Wähle einen Speicherort...")

def get_local_version():
    if check_file_existence(str(program_path) + "//version.txt"):
        with open(program_path + "//version.txt", 'r', encoding='utf-8') as file:
            file_content = file.read()
            return file_content
    else:
        try:
            with open(str(program_path) + "//version.txt", 'w', encoding='utf-8') as file:
                file.write("0")
                print(f"version.txt wurde nicht gefunden. Es wurde eine erstellt.")
                return "0"
        except Exception as e:
            print(program_path)
            print(f"Ein Fehler ist aufgetreten: {e}")






    


