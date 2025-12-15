import customtkinter as ctk
import os
import json
import shutil
import ctypes
import sys
import datetime
import stat
from tkinter import filedialog, messagebox

# --- Konfiguration & Design (AetherLink v1.3.0) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME = "AetherLink"
APP_VERSION = "1.3.0"
ICON_FILENAME = "app_icon.ico" 

myappid = f'custom.aetherlink.sync.{APP_VERSION}'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# --- Sprach-Datenbank ---
LANG = {
    "DE": {
        "app_title": APP_NAME,
        "tab_setup": "  ➕  Spiel hinzufügen",
        "tab_manage": "  📂  Verwaltung / Restore",
        "lbl_cloud": "Cloud Pfad:",
        "btn_cloud": "☁️ Cloud Ordner wählen",
        "header_setup": "Spiel zur Cloud hinzufügen (Ursprung / PC 1)",
        "lbl_name": "Name des Spiels:",
        "lbl_path": "Lokaler Pfad:",
        "btn_browse": "📂 Ordner suchen...",
        "no_path": "Kein Ordner gewählt",
        "btn_action": "🛡️ Backup erstellen & Verschieben",
        "log_title": "Protokoll:",
        "header_manage": "Verwaltung & Wiederherstellung",
        "help_text": "ANLEITUNG:\n• PC 1 (Ursprung): Nutze 'Reset (Ursprung)', um alles rückgängig zu machen (Löscht Cloud!).\n• PC 2+ (Client): Nutze 'Verlinken', um mitzuspielen. Nutze 'Trennen (Client)', um die Verbindung zu lösen (Behält Cloud).",
        "btn_refresh": "🔄 Liste aktualisieren",
        "list_title": "Verfügbare Spiele in der Cloud",
        "btn_link": "🔗 Verlinken",
        "btn_unlink": "Trennen (Client)",
        "btn_restore": "⚠️ Reset (Ursprung)",
        "btn_forget": "❌",
        "msg_cloud_err": "Bitte zuerst Cloud-Ordner wählen!",
        "msg_name_err": "Bitte Namen eingeben!",
        "msg_path_err": "Bitte Spielordner wählen!",
        "admin_ok": "Admin: Ja 🛡️",
        "admin_no": "Admin: Nein ⚠️",
        "restore_title": "Vollständiger Reset (PC 1)",
        "restore_msg": "ACHTUNG: Dies ist für den URSPSRUNGS-PC!\n\n1. Link wird entfernt.\n2. Daten werden aus Cloud zurückgeholt.\n3. CLOUD-DATEN WERDEN GELÖSCHT!\n\nFortfahren?",
        "unlink_title": "Verbindung trennen (PC 2+)",
        "unlink_msg": "Soll die Verknüpfung auf diesem PC entfernt werden?\n\n• Cloud-Daten bleiben SICHER.\n• Falls ein lokales Backup (vor Verlinkung) existiert, wird es wiederhergestellt.",
        "forget_title": "Eintrag entfernen",
        "forget_msg": "Nur aus der Liste entfernen?\nEs werden KEINE Dateien gelöscht."
    },
    "EN": {
        "app_title": APP_NAME,
        "tab_setup": "  ➕  Add Game",
        "tab_manage": "  📂  Manage / Restore",
        "lbl_cloud": "Cloud Path:",
        "btn_cloud": "☁️ Select Cloud Folder",
        "header_setup": "Add Game to Cloud (Origin / PC 1)",
        "lbl_name": "Game Name:",
        "lbl_path": "Local Path:",
        "btn_browse": "📂 Browse...",
        "no_path": "No folder selected",
        "btn_action": "🛡️ Backup & Move",
        "log_title": "Log:",
        "header_manage": "Manage & Restore",
        "help_text": "INSTRUCTIONS:\n• PC 1 (Origin): Use 'Reset (Origin)' to revert completely (Deletes Cloud!).\n• PC 2+ (Client): Use 'Link' to join. Use 'Unlink (Client)' to detach (Keeps Cloud).",
        "btn_refresh": "🔄 Refresh List",
        "list_title": "Available Games in Cloud",
        "btn_link": "🔗 Link Here",
        "btn_unlink": "Unlink (Client)",
        "btn_restore": "⚠️ Reset (Origin)",
        "btn_forget": "❌",
        "msg_cloud_err": "Select Cloud Folder first!",
        "msg_name_err": "Enter a game name!",
        "msg_path_err": "Select a game folder!",
        "admin_ok": "Admin: Yes 🛡️",
        "admin_no": "Admin: No ⚠️",
        "restore_title": "Full Reset (PC 1)",
        "restore_msg": "WARNING: This is for the ORIGIN PC!\n\n1. Remove Link.\n2. Copy data back from Cloud.\n3. DELETE CLOUD DATA!\n\nContinue?",
        "unlink_title": "Unlink (PC 2+)",
        "unlink_msg": "Remove link on this PC?\n\n• Cloud data remains SAFE.\n• If a local backup (pre-link) exists, it will be restored.",
        "forget_title": "Remove Entry",
        "forget_msg": "Remove from list only?\nNO files will be deleted."
    }
}

class AetherLinkApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "DE"
        self.t = LANG[self.current_lang]
        
        self.title(self.t["app_title"])
        self.geometry("1000x700") # Etwas breiter für die Buttons
        
        # Icon laden
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        possible_icons = [
            os.path.join(base_path, ICON_FILENAME),
            os.path.join(base_path, "data", ICON_FILENAME),
            os.path.join("data", ICON_FILENAME)
        ]
        for icon in possible_icons:
            if os.path.exists(icon):
                try: 
                    self.iconbitmap(icon)
                    break
                except: pass

        self.cloud_path = ""
        self.games_data = []
        self.selected_game_path = ""

        # Config Pfad
        self.app_data_dir = os.path.join(os.getenv('APPDATA'), APP_NAME)
        self.config_file = os.path.join(self.app_data_dir, "config.json")

        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.lbl_logo = ctk.CTkLabel(self.sidebar, text=APP_NAME, font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 10))

        self.lbl_admin = ctk.CTkLabel(self.sidebar, text=self.t["admin_ok"] if self.is_admin() else self.t["admin_no"], text_color="#2CC985" if self.is_admin() else "red")
        self.lbl_admin.grid(row=1, column=0, pady=(0, 20))

        self.btn_nav_setup = ctk.CTkButton(self.sidebar, text=self.t["tab_setup"], height=40, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.select_frame("setup"))
        self.btn_nav_setup.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.btn_nav_manage = ctk.CTkButton(self.sidebar, text=self.t["tab_manage"], height=40, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.select_frame("manage"))
        self.btn_nav_manage.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.lang_var = ctk.StringVar(value="Deutsch")
        self.opt_lang = ctk.CTkOptionMenu(self.sidebar, values=["Deutsch", "English"], variable=self.lang_var, command=self.change_language, width=150, fg_color=("gray70", "gray30"), button_color=("gray60", "gray20"))
        self.opt_lang.grid(row=4, column=0, padx=20, pady=20)

        self.lbl_cloud_status = ctk.CTkLabel(self.sidebar, text=self.t["lbl_cloud"] + "\n❌", font=("Arial", 11), text_color="gray")
        self.lbl_cloud_status.grid(row=6, column=0, padx=20, pady=(10,0))
        
        self.btn_select_cloud = ctk.CTkButton(self.sidebar, text=self.t["btn_cloud"], fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.select_cloud_folder)
        self.btn_select_cloud.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.lbl_version = ctk.CTkLabel(self.sidebar, text=f"v{APP_VERSION}", font=("Arial", 9), text_color="gray30")
        self.lbl_version.grid(row=8, column=0, pady=(0, 10))

        # Main Frames
        self.frame_setup = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_manage = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.setup_ui_components()
        self.load_config()
        self.select_frame("setup")

    def is_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    # --- UI Components ---
    def setup_ui_components(self):
        # SETUP FRAME
        self.lbl_setup_header = ctk.CTkLabel(self.frame_setup, text=self.t["header_setup"], font=("Arial", 22, "bold"))
        self.lbl_setup_header.pack(pady=20, padx=20, anchor="w")

        frm = ctk.CTkFrame(self.frame_setup)
        frm.pack(pady=10, padx=20, fill="x")
        frm.grid_columnconfigure(1, weight=1)

        self.lbl_name_txt = ctk.CTkLabel(frm, text=self.t["lbl_name"])
        self.lbl_name_txt.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.entry_name = ctk.CTkEntry(frm, placeholder_text="Name...")
        self.entry_name.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        self.lbl_path_txt = ctk.CTkLabel(frm, text=self.t["lbl_path"])
        self.lbl_path_txt.grid(row=1, column=0, padx=15, pady=15, sticky="w")
        
        frm_browse = ctk.CTkFrame(frm, fg_color="transparent")
        frm_browse.grid(row=1, column=1, padx=15, pady=15, sticky="ew")
        frm_browse.grid_columnconfigure(1, weight=1)

        self.btn_browse = ctk.CTkButton(frm_browse, text=self.t["btn_browse"], width=120, command=self.browse_game_folder)
        self.btn_browse.grid(row=0, column=0, sticky="w")
        self.lbl_selected_path = ctk.CTkLabel(frm_browse, text=self.t["no_path"], text_color="gray")
        self.lbl_selected_path.grid(row=0, column=1, padx=10, sticky="w")

        self.btn_start_sync = ctk.CTkButton(self.frame_setup, text=self.t["btn_action"], font=("Arial", 14, "bold"), height=45, command=self.process_new_game)
        self.btn_start_sync.pack(pady=10, padx=20, fill="x")

        self.lbl_log_title = ctk.CTkLabel(self.frame_setup, text=self.t["log_title"])
        self.lbl_log_title.pack(padx=20, anchor="w")
        self.console = ctk.CTkTextbox(self.frame_setup, height=150)
        self.console.pack(padx=20, pady=(5,20), fill="both", expand=True)

        # MANAGE FRAME
        self.lbl_manage_header = ctk.CTkLabel(self.frame_manage, text=self.t["header_manage"], font=("Arial", 22, "bold"))
        self.lbl_manage_header.pack(pady=(20, 10), padx=20, anchor="w")

        # Anleitung (Help Box)
        self.help_frame = ctk.CTkFrame(self.frame_manage, fg_color=("gray85", "gray20"))
        self.help_frame.pack(padx=20, pady=(0, 10), fill="x")
        self.lbl_help = ctk.CTkLabel(self.help_frame, text=self.t["help_text"], justify="left", font=("Arial", 12))
        self.lbl_help.pack(padx=10, pady=10, anchor="w")

        self.btn_refresh_list = ctk.CTkButton(self.frame_manage, text=self.t["btn_refresh"], command=self.load_database)
        self.btn_refresh_list.pack(padx=20, pady=5, anchor="w")

        self.scroll_list = ctk.CTkScrollableFrame(self.frame_manage, label_text=self.t["list_title"])
        self.scroll_list.pack(padx=20, pady=10, fill="both", expand=True)

    def change_language(self, choice):
        self.current_lang = "DE" if choice == "Deutsch" else "EN"
        self.t = LANG[self.current_lang]
        self.save_local_settings()
        
        self.title(self.t["app_title"])
        self.lbl_logo.configure(text=self.t["app_title"])
        self.btn_nav_setup.configure(text=self.t["tab_setup"])
        self.btn_nav_manage.configure(text=self.t["tab_manage"])
        self.lbl_cloud_status.configure(text=self.t["lbl_cloud"] + "\n" + (self.cloud_path[:20]+"..." if self.cloud_path else "❌"))
        self.btn_select_cloud.configure(text=self.t["btn_cloud"])
        self.lbl_setup_header.configure(text=self.t["header_setup"])
        self.lbl_name_txt.configure(text=self.t["lbl_name"])
        self.lbl_path_txt.configure(text=self.t["lbl_path"])
        self.btn_browse.configure(text=self.t["btn_browse"])
        if not self.selected_game_path:
            self.lbl_selected_path.configure(text=self.t["no_path"])
        self.btn_start_sync.configure(text=self.t["btn_action"])
        self.lbl_log_title.configure(text=self.t["log_title"])
        self.lbl_manage_header.configure(text=self.t["header_manage"])
        self.lbl_help.configure(text=self.t["help_text"])
        self.btn_refresh_list.configure(text=self.t["btn_refresh"])
        self.scroll_list.configure(label_text=self.t["list_title"])
        self.lbl_admin.configure(text=self.t["admin_ok"] if self.is_admin() else self.t["admin_no"])
        self.load_database()

    def select_frame(self, name):
        self.frame_setup.grid_forget()
        self.frame_manage.grid_forget()
        active_color = ("gray75", "gray25")
        transparent = "transparent"

        if name == "setup":
            self.frame_setup.grid(row=0, column=1, sticky="nsew")
            self.btn_nav_setup.configure(fg_color=active_color)
            self.btn_nav_manage.configure(fg_color=transparent)
        else:
            self.frame_manage.grid(row=0, column=1, sticky="nsew")
            self.btn_nav_setup.configure(fg_color=transparent)
            self.btn_nav_manage.configure(fg_color=active_color)
            self.load_database()

    def browse_game_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_game_path = path
            disp = path if len(path) < 45 else path[:20] + " ... " + path[-20:]
            self.lbl_selected_path.configure(text=disp, text_color="white")

    def log(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{ts}] {msg}\n")
        self.console.see("end")

    def remove_readonly(self, func, path, excinfo):
        try: os.chmod(path, stat.S_IWRITE); func(path)
        except: pass

    # --- MAIN LOGIC PC 1 ---
    def process_new_game(self):
        if not self.cloud_path: return messagebox.showerror("Error", self.t["msg_cloud_err"])
        name = self.entry_name.get()
        if not name: return messagebox.showerror("Error", self.t["msg_name_err"])
        if not self.selected_game_path: return messagebox.showerror("Error", self.t["msg_path_err"])

        original_path = self.selected_game_path
        cloud_game_dir = os.path.join(self.cloud_path, name)
        
        # Backup Lokal
        parent_dir = os.path.dirname(original_path)
        backups_dir = os.path.join(parent_dir, "_BACKUP_SAVE")
        if not os.path.exists(backups_dir): os.makedirs(backups_dir)

        self.log(f"Start: {name}")
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = os.path.join(backups_dir, f"{name}_BACKUP_{ts}")
        
        try:
            shutil.make_archive(zip_path, 'zip', original_path)
            self.log("✅ Backup OK (Lokal).")
        except Exception as e:
            return messagebox.showerror("Backup Error", str(e))

        try:
            if os.path.exists(cloud_game_dir):
                if not messagebox.askyesno("Info", f"'{name}' in Cloud gefunden.\nLokal löschen und verlinken?"): return
                shutil.rmtree(original_path, onerror=self.remove_readonly)
            else:
                shutil.move(original_path, cloud_game_dir)
            
            os.symlink(cloud_game_dir, original_path, target_is_directory=True)
            self.log("✅ Symlink OK.")
            self.add_to_db(name, original_path)
            self.entry_name.delete(0, "end")
            self.lbl_selected_path.configure(text=self.t["no_path"], text_color="gray")
            self.selected_game_path = ""
            messagebox.showinfo("Success", f"{name} synced!")
        except Exception as e:
            self.log(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))

    # --- RESTORE / UNLINK LOGIC ---
    
    # 1. PC 1: Kompletter Reset (Gefährlich)
    def restore_origin(self, game):
        target_local = os.path.expandvars(game["path_pattern"])
        cloud_source = os.path.join(self.cloud_path, game["cloud_folder"])

        if not messagebox.askyesno(self.t["restore_title"], self.t["restore_msg"]): return

        try:
            if os.path.exists(target_local):
                if os.path.islink(target_local):
                    os.remove(target_local)
                else:
                    os.rename(target_local, target_local + "_OLD_" + datetime.datetime.now().strftime("%M%S"))

            if os.path.exists(cloud_source):
                shutil.copytree(cloud_source, target_local)
            else:
                messagebox.showerror("Fehler", "Cloud-Daten nicht gefunden!")
                return

            shutil.rmtree(cloud_source, onerror=self.remove_readonly)

            # Backup löschen
            parent_dir = os.path.dirname(target_local)
            local_backup_dir = os.path.join(parent_dir, "_BACKUP_SAVE")
            if os.path.exists(local_backup_dir):
                shutil.rmtree(local_backup_dir, onerror=self.remove_readonly)

            self.games_data = [g for g in self.games_data if g["name"] != game["name"]]
            self.save_database()
            self.load_database()
            messagebox.showinfo("Fertig", "Ursprungszustand wiederhergestellt.")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei Restore: {e}")

    # 2. PC 2: Verbindung trennen (Sicher)
    def unlink_client(self, game):
        target_local = os.path.expandvars(game["path_pattern"])
        
        if not messagebox.askyesno(self.t["unlink_title"], self.t["unlink_msg"]): return

        try:
            # Link entfernen
            if os.path.exists(target_local) and os.path.islink(target_local):
                os.remove(target_local)
            
            # Backup von VOR der Verknüpfung wiederherstellen?
            local_backup = target_local + "_LOCAL_BEFORE_LINK"
            if os.path.exists(local_backup):
                os.rename(local_backup, target_local)
                messagebox.showinfo("Info", "Verbindung getrennt. Alter lokaler Spielstand wurde wiederhergestellt.")
            else:
                # Kein Backup da (PC war vielleicht vorher leer)
                if not os.path.exists(target_local):
                    os.makedirs(target_local) # Leeren Ordner erstellen
                messagebox.showinfo("Info", "Verbindung getrennt (Kein lokales Backup gefunden).")
                
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def forget_game_entry(self, game):
        if messagebox.askyesno(self.t["forget_title"], self.t["forget_msg"]):
            self.games_data = [g for g in self.games_data if g["name"] != game["name"]]
            self.save_database()
            self.load_database()

    # 3. PC 2: Verknüpfen (Starten)
    def link_on_pc2(self, game):
        target = os.path.expandvars(game["path_pattern"])
        source = os.path.join(self.cloud_path, game["cloud_folder"])
        
        if not os.path.exists(source): return messagebox.showerror("Error", "Cloud folder missing.")
        
        # Lokaler Check: Backup erstellen, falls schon was da ist
        if os.path.exists(target):
            if os.path.islink(target): return # Schon verlinkt
            
            # Backup erstellen für späteres "Unlink"
            backup_name = target + "_LOCAL_BEFORE_LINK"
            if os.path.exists(backup_name): shutil.rmtree(backup_name) # Altes Backup weg
            os.rename(target, backup_name)
            messagebox.showinfo("Backup", f"Lokaler Spielstand gefunden.\nBackup erstellt als:\n{os.path.basename(backup_name)}")
            
        parent = os.path.dirname(target)
        if not os.path.exists(parent): os.makedirs(parent)
        try:
            os.symlink(source, target, target_is_directory=True)
            messagebox.showinfo("OK", f"Linked {game['name']}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- DB ---
    def add_to_db(self, name, path):
        self.load_database()
        user_profile = os.environ.get('USERPROFILE')
        clean_path = path.replace(user_profile, "%USERPROFILE%") if user_profile else path
        for g in self.games_data:
            if g["name"] == name:
                g["path_pattern"] = clean_path
                self.save_database()
                return
        self.games_data.append({"name": name, "path_pattern": clean_path, "cloud_folder": name})
        self.save_database()

    def load_database(self):
        for w in self.scroll_list.winfo_children(): w.destroy()
        if not self.cloud_path: return
        p = os.path.join(self.cloud_path, "games_db.json")
        if os.path.exists(p):
            with open(p, "r") as f: self.games_data = json.load(f)
            for g in self.games_data: self.create_row(g)

    def create_row(self, game):
        r = ctk.CTkFrame(self.scroll_list)
        r.pack(fill="x", pady=5)
        
        # Name
        ctk.CTkLabel(r, text=game["name"], font=("Arial", 12, "bold")).pack(side="left", padx=10)
        
        # Buttons (Rechtsbündig)
        
        # 4. Forget
        ctk.CTkButton(r, text=self.t["btn_forget"], width=40, fg_color="#444", hover_color="#666", command=lambda g=game: self.forget_game_entry(g)).pack(side="right", padx=(5, 10))

        # 3. Restore (Origin) - Dunkelrot
        ctk.CTkButton(r, text=self.t["btn_restore"], width=120, fg_color="#550000", hover_color="#880000", command=lambda g=game: self.restore_origin(g)).pack(side="right", padx=5)

        # 2. Unlink (Client) - Orange
        ctk.CTkButton(r, text=self.t["btn_unlink"], width=120, fg_color="#C06000", hover_color="#E08000", command=lambda g=game: self.unlink_client(g)).pack(side="right", padx=5)

        # 1. Link (Client) - Blau/Grün
        ctk.CTkButton(r, text=self.t["btn_link"], width=100, command=lambda g=game: self.link_on_pc2(g)).pack(side="right", padx=5)

    def save_database(self):
        with open(os.path.join(self.cloud_path, "games_db.json"), "w") as f: json.dump(self.games_data, f, indent=4)
        
    def select_cloud_folder(self):
        f = filedialog.askdirectory()
        if f:
            self.cloud_path = f
            self.lbl_cloud_status.configure(text=self.t["lbl_cloud"] + "\n" + (f[:25]+"..." if len(f)>25 else f), text_color="green")
            self.save_local_settings()
            self.load_database()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                d = json.load(f)
                self.cloud_path = d.get("cloud_path", "")
                saved_lang = d.get("language", "DE")
                if saved_lang != self.current_lang:
                    self.lang_var.set("Deutsch" if saved_lang == "DE" else "English")
                    self.change_language(self.lang_var.get())
                if(self.cloud_path): 
                     self.lbl_cloud_status.configure(text=self.t["lbl_cloud"] + "\n" + (self.cloud_path[:25]+"..." if len(self.cloud_path)>25 else self.cloud_path), text_color="green")
                     
    def save_local_settings(self):
        if not os.path.exists(self.app_data_dir): os.makedirs(self.app_data_dir)
        data = {"cloud_path": self.cloud_path, "language": self.current_lang}
        with open(self.config_file, "w") as f: json.dump(data, f)
                     
if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        script_path = os.path.abspath(sys.argv[0])
        params = f'"{script_path}"'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    else:
        app = AetherLinkApp()
        app.mainloop()