# main.py
from datetime import datetime
from pathlib import Path
import colorama
import shutil
import mimetypes
import locale

colorama.init(autoreset=True)

# ============= Couleurs =============
g = colorama.Fore.GREEN
r = colorama.Fore.RED
b = colorama.Fore.BLUE
c = colorama.Fore.CYAN
m = colorama.Fore.MAGENTA
y = colorama.Fore.YELLOW
# ===================================

logs_enabled = True


def detect_system_language():
    """
    Détecte la langue du système.
    Renvoie 'fr', 'en' ou 'es'.
    Si la langue n'est pas reconnue, renvoie 'en' par défaut.
    """
    try:
        # Essaye de récupérer la locale système
        lang, _ = locale.getdefaultlocale()
        if lang:
            code = lang.split('_')[0].lower()
            if code in ['fr', 'en', 'es']:
                return code
    except:
        pass
    return 'en'

# ===== Choix de la langue =====
# 'en' pour anglais, 'fr' pour français, 'es' pour espagnol
system_lang = detect_system_language()

# ===== Dictionnaire de traduction =====
texts = {
    "title": {
        "en": "=== Automatic Sorter ===",
        "fr": "=== Trieur Automatique ===",
        "es": "=== Ordenador Automático ==="
    },
    "enter_folder": {
        "en": "Enter folder to sort: ",
        "fr": "Entrez le dossier à trier : ",
        "es": "Ingrese la carpeta a ordenar: "
    },
    "invalid_path": {
        "en": "Invalid path or not a folder!",
        "fr": "Chemin invalide ou pas un dossier !",
        "es": "Ruta inválida o no es una carpeta!"
    },
    "empty_folder": {
        "en": "The folder is empty!",
        "fr": "Le dossier est vide !",
        "es": "¡La carpeta está vacía!"
    },
    "method_title": {
        "en": "=== Sorting Method ===",
        "fr": "=== Méthode de tri ===",
        "es": "=== Método de ordenamiento ==="
    },
    "method_1": {
        "en": "1. Sort by extension",
        "fr": "1. Tri par extension",
        "es": "1. Ordenar por extensión"
    },
    "method_2": {
        "en": "2. Sort by file size",
        "fr": "2. Tri par taille de fichier",
        "es": "2. Por tamaño de archivo"
    },
    "method_3": {
        "en": "3. Alphabetical order",
        "fr": "3. Tri par ordre alphabétique",
        "es": "3. Orden alfabético"
    },
    "method_4": {
        "en": "4. By modification date",
        "fr": "4. Tri par date de modification",
        "es": "4. Por fecha de modificación"
    },
    "method_5": {
        "en": "5. By name length",
        "fr": "5. Tri par longueur du nom",
        "es": "5. Por longitud del nombre"
    },
    "method_6": {
        "en": "6. By keyword",
        "fr": "6. Tri par mot clé",
        "es": "6. Por palabra clave"
    },
    "method_7": {
        "en": "7. By MIME type (image/video/doc/other)",
        "fr": "7. Par type MIME (image/vidéo/doc/autre)",
        "es": "7. Por tipo MIME (imagen/video/doc/otro)"
    },
    "method_8": {
        "en": "8. By day of the week of creation",
        "fr": "8. Tri par jour de la semaine de création",
        "es": "8. Por día de la semana de creación"
    },
    "enter_method": {
        "en": "Enter the number of the sorting method: ",
        "fr": "Entrez le numéro de la méthode de tri : ",
        "es": "Ingrese el número del método de ordenamiento: "
    },
    "cancelled": {
        "en": "Sorting cancelled by user!",
        "fr": "Tri annulé par l’utilisateur !",
        "es": "Ordenamiento cancelado por el usuario!"
    },
    "done": {
        "en": "Sorting finished 🚀",
        "fr": "Tri terminé 🚀",
        "es": "Ordenamiento finalizado 🚀"
    },
    "ask_extensions": {
        "en": "Do you want to sort only certain extensions? (ex: txt,jpg) or leave empty for all: ",
        "fr": "Voulez-vous trier seulement certains types d'extensions ? (ex: txt,jpg) ou laisser vide pour tous : ",
        "es": "¿Desea ordenar solo ciertas extensiones? (ej: txt,jpg) o dejar vacío para todas: "
    },
    "enter_tol": {
        "en": "Enter tolerance in bytes for size ranges: ",
        "fr": "Entrez la tolérance en octets pour les tranches : ",
        "es": "Ingrese la tolerancia en bytes para los rangos: "
    },
    "whitelist_count": {
        "en": "Enter the number of files to ignore: ",
        "fr": "Entrez le nombre de fichiers à ignorer : ",
        "es": "Ingrese el número de archivos a ignorar: "
    },
    "whitelist_file": {
        "en": "Enter file #{} to ignore: ",
        "fr": "Entrez le fichier n°{} à ignorer : ",
        "es": "Ingrese el archivo #{} a ignorar: "
    },
    "ask_whitelist": {
        "en": "Do you want to add files to ignore? (Y/N) : ",
        "fr": "Voulez-vous ajouter des fichiers à ignorer ?(Y/N) : ",
        "es": "¿Desea agregar archivos a ignorar? (Y/N) : "
    },
    "undo": {
        "en": "Do you want to undo sorting and restore files? (Y/N) : ",
        "fr": "Voulez-vous annuler le tri et remettre les fichiers à leur place ? (Y/N) : ",
        "es": "¿Desea deshacer la ordenación y restaurar los archivos? (Y/N) : "
    },
}

def _(key, *args):
    """Retourne le texte selon la langue et formate avec args si nécessaire"""
    text = texts.get(key, {}).get(system_lang, key)
    if args:
        text = text.format(*args)
    return text

# ===== Logging =====
def log(msg, statut, color):
    if logs_enabled:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"{color}{now} - [{statut}] - {msg}")

# ===== Gestion fichiers =====
def get_all_files(root: Path):
    return [f for f in root.iterdir() if f.is_file()]

def create_folder(path: Path):
    if not path.exists():
        path.mkdir()
        log(_("Folder created: {}", path.name), "INFO", g)

def remove_empty_folders(folders):
    for folder in folders:
        if folder.exists() and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            log(_("Empty folder removed: {}", folder.name), "INFO", b)

def ask_extensions():
    ext_input = input(_("ask_extensions"))
    return [e.strip().lower() for e in ext_input.split(",") if e.strip()] if ext_input else []

def filter_by_extension(fichiers, extensions):
    if not extensions:
        return fichiers
    return [f for f in fichiers if f.suffix[1:].lower() in extensions]

def get_mime_type(f: Path):
    mime, _ = mimetypes.guess_type(f)
    return mime.split("/")[0] if mime else "other"

# ===== Main =====
def main():
    # Choix dossier
    while True:
        print(f"{c}{_('title')}")
        folder_input = input(f"{c}{_('enter_folder')}")
        path = Path(folder_input)

        if not path.exists() or not path.is_dir():
            log(_("invalid_path"), "ERREUR", r)
            print(f"{r}{_('invalid_path')}")
            continue

        fichiers = get_all_files(path)
        if len(fichiers) == 0:
            log(_("empty_folder"), "INFO", r)
            print(f"{r}{_('empty_folder')}")
            continue

        log(_("{0} files found", len(fichiers)), "INFO", g)
        break

    # Méthode & whitelist
    whiteliste = []
    while True:
        print(f"{m}{_('method_title')}")
        for i in range(1, 9):
            print(f"{m}{_('method_' + str(i))}")

        how = input(f"{c}{_('enter_method')}")
        if how not in tuple(str(i) for i in range(1, 9)):
            print(f"{r}Invalid number!")
            log("Invalid number!", "ERREUR", r)
            continue

        choice = input(_("ask_whitelist")).lower()
        if choice == "y":
            try:
                n_whitelist = int(input(_("whitelist_count")))
            except:
                n_whitelist = 0
            for i in range(n_whitelist):
                add = input(_("whitelist_file", i+1))
                whiteliste.append(add)

        extensions = ask_extensions() if how != "1" else []
        break

    # Tri effectif
    print(f"{g}{_('done')}")
    historique = []
    dossiers_crees = set()
    fichiers = filter_by_extension(fichiers, extensions)

    for f in fichiers:
        if f.name in whiteliste:
            continue

        if how == "1":
            folder = path / (f.suffix[1:] if f.suffix else "no_extension")
        elif how == "2":
            tol = int(input(_("enter_tol")))
            taille = f.stat().st_size
            tranche = (taille // tol) * tol
            folder = path / f"{tranche}_{tranche+tol-1}B"
        elif how == "3":
            folder = path / f.name[0].upper()
        elif how == "4":
            folder = path / datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
        elif how == "5":
            folder = path / f"{len(f.name)}_chars"
        elif how == "6":
            mot = input("Enter keyword: ").lower()
            if mot not in f.name.lower():
                continue
            folder = path / mot
        elif how == "7":
            folder = path / get_mime_type(f)
        elif how == "8":
            folder = path / datetime.fromtimestamp(f.stat().st_ctime).strftime("%A")
        else:
            folder = path

        create_folder(folder)
        dossiers_crees.add(folder)
        nouveau = folder / f.name
        shutil.move(str(f), nouveau)
        historique.append((nouveau, f))

    log(_("done"), "INFO", g)

    # Undo
    if input(_("undo")).lower() == "y":
        for nouveau, ancien in historique:
            if not nouveau.exists():
                log(f"{_('missing_file')} {nouveau}", "WARN", y)
                continue
            shutil.move(nouveau, ancien)

        remove_empty_folders(dossiers_crees)
        log("Rollback finished", "INFO", g)

if __name__ == "__main__":
    main()
