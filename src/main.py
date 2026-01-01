# main.py
from datetime import datetime
from pathlib import Path
import colorama
import shutil
import mimetypes

colorama.init(autoreset=True)

g = colorama.Fore.GREEN
r = colorama.Fore.RED
b = colorama.Fore.BLUE
c = colorama.Fore.CYAN
m = colorama.Fore.MAGENTA

logs_enabled = True

def log(msg, statut, color):
    if logs_enabled:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"{color}{now} - [{statut}] - {msg}")

def get_all_files(root: Path):
    return [f for f in root.iterdir() if f.is_file()]

def create_folder(path: Path):
    if not path.exists():
        path.mkdir()
        log(f"Dossier créé : {path.name}", "INFO", g)

def remove_empty_folders(folders):
    for folder in folders:
        if folder.exists() and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            log(f"Dossier vide supprimé : {folder.name}", "INFO", b)

def ask_extensions():
    ext_input = input(f"{c}Voulez-vous trier seulement certains types d'extensions ? (ex: txt,jpg) ou laisser vide pour tous : ")
    extensions = [e.strip().lower() for e in ext_input.split(",") if e.strip()] if ext_input else []
    return extensions

def filter_by_extension(fichiers, extensions):
    if not extensions:
        return fichiers
    return [f for f in fichiers if f.suffix[1:].lower() in extensions]

def get_mime_type(f: Path):
    mime, _ = mimetypes.guess_type(f)
    if mime:
        return mime.split("/")[0]
    return "autre"

def main():
    # ===== Choix du dossier =====
    while True:
        print(f"{c}=== Trieur Automatique ===")
        folder_input = input(f"{c}Entrez le dossier à trier : ")
        path = Path(folder_input)

        if not path.exists() or not path.is_dir():
            log("Chemin invalide", "ERREUR", r)
            print(f"{r}Chemin invalide ou pas un dossier !")
            continue

        fichiers = get_all_files(path)
        if len(fichiers) == 0:
            log("Dossier vide", "INFO", r)
            print(f"{r}Le dossier est vide !")
            continue

        log(f"{len(fichiers)} fichiers trouvés", "INFO", g)
        break

    # ===== Méthode & Whitelist =====
    whiteliste = []
    while True:
        print(f"{m}=== Méthode de tri ===")
        print(f"{m}1. Tri par extension")
        print(f"{m}2. Tri par taille de fichier")
        print(f"{m}3. Tri par ordre alphabétique")
        print(f"{m}4. Tri par date de modification")
        print(f"{m}5. Tri par longueur du nom")
        print(f"{m}6. Tri par mot clé")
        print(f"{m}7. Tri par type MIME (image/vidéo/doc/autre)")
        print(f"{m}8. Tri par jour de la semaine de création")

        how = input(f"{c}Entrez le numéro de la méthode de tri : ")
        if how not in tuple(str(i) for i in range(1, 9)):
            print(f"{r}Numéro invalide !")
            log("Numéro invalide", "ERREUR", r)
            continue

        choice = input(f"{c}Voulez-vous ajouter des fichiers à ignorer ?(Y/N) : ").lower()
        if choice == "y":
            try:
                n_whiteliste = int(input(f"{c}Entrez le nombre de fichiers à ignorer : "))
            except ValueError:
                print(f"{r}Nombre invalide !")
                log("Nombre invalide pour la whitelist", "ERREUR", r)
                n_whiteliste = 0

            for i in range(n_whiteliste):
                add = input(f"{c}Entrez le fichier n°{i+1} à ignorer : ")
                whiteliste.append(add)

            log(f"Whitelist définie : {whiteliste}", "INFO", m)

        extensions = []
        if how != "1":  # permet de choisir certaines extensions même si pas tri par extension
            extensions = ask_extensions()

        break

    # ===== Tri effectif =====
    print(f"{g}=== Début du tri ===")
    historique = []  # pour undo
    dossiers_crees = set()

    fichiers = filter_by_extension(fichiers, extensions)

    if how == "1":  # Tri par extension
        for f in fichiers:
            if f.name in whiteliste:
                continue
            ext = f.suffix[1:] if f.suffix else "no_extension"
            folder_ext = path / ext
            create_folder(folder_ext)
            dossiers_crees.add(folder_ext)
            nouveau = folder_ext / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par extension terminé", "INFO", g)

    elif how == "2":  # Tri par taille
        try:
            tol = int(input(f"{c}Entrez la tolérance en octets pour les tranches : "))
        except ValueError:
            tol = 1024

        for f in fichiers:
            if f.name in whiteliste:
                continue
            taille = f.stat().st_size
            tranche = (taille // tol) * tol
            folder_size = path / f"{tranche}_{tranche+tol-1}B"
            create_folder(folder_size)
            dossiers_crees.add(folder_size)
            nouveau = folder_size / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par taille terminé", "INFO", g)

    elif how == "3":  # Tri alphabétique
        for f in fichiers:
            if f.name in whiteliste:
                continue
            lettre = f.name[0].upper()
            folder_letter = path / lettre
            create_folder(folder_letter)
            dossiers_crees.add(folder_letter)
            nouveau = folder_letter / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri alphabétique terminé", "INFO", g)

    elif how == "4":  # Tri par date de modification
        for f in fichiers:
            if f.name in whiteliste:
                continue
            date_mod = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
            folder_date = path / date_mod
            create_folder(folder_date)
            dossiers_crees.add(folder_date)
            nouveau = folder_date / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par date terminé", "INFO", g)

    elif how == "5":  # Tri par longueur du nom
        for f in fichiers:
            if f.name in whiteliste:
                continue
            longueur = len(f.name)
            folder_len = path / f"{longueur}_chars"
            create_folder(folder_len)
            dossiers_crees.add(folder_len)
            nouveau = folder_len / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par longueur du nom terminé", "INFO", g)

    elif how == "6":  # Tri par mot clé
        mot = input(f"{c}Entrez le mot clé à utiliser pour le tri : ").lower()
        for f in fichiers:
            if f.name in whiteliste:
                continue
            if mot in f.name.lower():
                folder_kw = path / f"{mot}"
                create_folder(folder_kw)
                dossiers_crees.add(folder_kw)
                nouveau = folder_kw / f.name
                shutil.move(str(f), nouveau)
                historique.append((nouveau, f))
        log(f"Tri par mot clé '{mot}' terminé", "INFO", g)

    elif how == "7":  # Tri par type MIME
        for f in fichiers:
            if f.name in whiteliste:
                continue
            mime_type = get_mime_type(f)
            folder_mime = path / mime_type
            create_folder(folder_mime)
            dossiers_crees.add(folder_mime)
            nouveau = folder_mime / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par type MIME terminé", "INFO", g)

    elif how == "8":  # Tri par jour de la semaine
        for f in fichiers:
            if f.name in whiteliste:
                continue
            day = datetime.fromtimestamp(f.stat().st_ctime).strftime("%A")
            folder_day = path / day
            create_folder(folder_day)
            dossiers_crees.add(folder_day)
            nouveau = folder_day / f.name
            shutil.move(str(f), nouveau)
            historique.append((nouveau, f))
        log("Tri par jour de la semaine terminé", "INFO", g)

    print(f"{g}Tri terminé 🚀")

    # ===== Undo complet =====
    choice = input(f"{c}Voulez-vous annuler le tri et remettre les fichiers à leur place ? (Y/N) : ").lower()
    if choice == "y":
        for nouveau, ancien in historique:
            shutil.move(str(nouveau), ancien)
        remove_empty_folders(dossiers_crees)
        log("Tri annulé et dossiers vides supprimés", "INFO", g)
        print(f"{g}Tous les fichiers ont été remis à leur emplacement initial !")

if __name__ == "__main__":
    main()
