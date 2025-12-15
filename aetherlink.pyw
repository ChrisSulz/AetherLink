import customtkinter as ctk
import os
import json
import shutil
import ctypes
import sys
import datetime
import stat
from tkinter import filedialog, messagebox
from PIL import Image  # Wichtig für das große Icon

# --- Konfiguration & Design (AetherLink v1.4.0) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME = "AetherLink"
APP_VERSION = "1.4.0"
ICON_FILENAME = "app_icon.ico" 

myappid = f'custom.aetherlink.sync.{APP_VERSION}'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# --- Sprach-Datenbank ---
LANG = {
    "DE": {
        "app_title": APP_NAME,
        "tab_setup": "  ➕  Spiel hinzufügen",
        "tab_manage": "  📂  Verwaltung",
        "tab_help": "  ❓  Anleitung / Hilfe",
        
        "lbl_cloud": "Cloud Speicherort:",
        "btn_cloud": "☁️ Cloud Ordner wählen",
        
        "header_setup_main": "Spiel hinzufügen",
        "header_setup_sub": "Ursprungssystem (PC 1) - Erstsicherung",
        
        "lbl_name": "Name des Spiels:",
        "lbl_path": "Lokaler Pfad:",
        "btn_browse": "📂 Ordner suchen...",
        "no_path": "Kein Ordner gewählt",
        "btn_action": "🛡️  Sichern & Synchronisieren",
        "log_title": "Protokoll / Status:",
        
        "header_manage": "Verwaltung & Wiederherstellung",
        "btn_refresh": "🔄 Liste aktualisieren",
        "list_title": "Synchronisierte Spiele in der Cloud",
        
        "header_help": "Wie funktioniert AetherLink?",
        "help_pc1_title": "🖥️  PC 1 (Ursprung)",
        "help_pc1_text": "1. Wähle oben links deinen Cloud-Ordner (Google Drive, Dropbox...).\n2. Gehe auf 'Spiel hinzufügen'.\n3. Wähle den Ordner mit deinen Spielständen.\n4. Klicke 'Sichern'. Der Ordner wird in die Cloud verschoben und verlinkt.",
        "help_pc2_title": "💻  PC 2, 3... (Client)",
        "help_pc2_text": "1. Wähle denselben Cloud-Ordner wie am ersten PC.\n2. Gehe auf 'Verwaltung'.\n3. Klicke bei dem Spiel auf '🔗 Verlinken'.\n4. Fertig! Dein Spielstand ist nun synchron.",
        
        "btn_link": "🔗 Verlinken",
        "btn_unlink": "Trennen (Client)",
        "btn_restore": "⚠️ Reset (Ursprung)",
        "btn_forget": "❌",
        
        "msg_cloud_err": "Bitte zuerst Cloud-Ordner wählen!",
        "msg_name_err": "Bitte Namen eingeben!",
        "msg_path_err": "Bitte Spielordner wählen!",
        
        "admin_ok": "✅ Adminrechte aktiv",
        "admin_no": "❌ Eingeschränkt",
        
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
        "tab_manage": "  📂  Manage",
        "tab_help": "  ❓  Help / Guide",
        
        "lbl_cloud": "Cloud Storage Path:",
        "btn_cloud": "☁️ Select Cloud Folder",
        
        "header_setup_main": "Add New Game",
        "header_setup_sub": "Origin System (PC 1) - Initial Backup",
        
        "lbl_name": "Game Name:",
        "lbl_path": "Local Path:",
        "btn_browse": "📂 Browse...",
        "no_path": "No folder selected",
        "btn_action": "🛡️  Backup & Sync",
        "log_title": "Log / Status:",
        
        "header_manage": "Manage & Restore",
        "btn_refresh": "🔄 Refresh List",
        "list_title": "Synced Games in Cloud",
        
        "header_help": "How to use AetherLink",
        "help_pc1_title": "🖥️  PC 1 (Origin)",
        "help_pc1_text": "1. Select your Cloud Folder (Drive, Dropbox...) on the left.\n2. Go to 'Add Game'.\n3. Select your local save game folder.\n4. Click 'Backup & Sync'. Files are moved to cloud and linked.",
        "help_pc2_title": "💻  PC 2, 3... (Client)",
        "help_pc2_text": "1. Select the same Cloud Folder as on PC 1.\n2. Go to 'Manage'.\n3. Click '🔗 Link Here' next to the game.\n4. Done! Your saves are now synced.",
        
        "btn_link": "🔗 Link Here",
        "btn_unlink": "Unlink (Client)",
        "btn_restore": "⚠️ Reset (Origin)",
        "btn_forget": "❌",
        
        "msg_cloud_err": "Select Cloud Folder first!",
        "msg_name_err": "Enter a game name!",
        "msg_path_err": "Select a game folder!",
        
        "admin_ok": "✅ Admin Active",
        "admin_no": "❌ Restricted",
        
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
        self.geometry("1100x750") 
        
        # --- Pfade & Icon Check ---
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.icon_path_abs = None
        
        possible_icons = [
            os.path.join(base_path, ICON_FILENAME),
            os.path.join(base_path, "data", ICON_FILENAME),
            os.path.join("data", ICON_FILENAME)
        ]
        
        # 1. Window Icon (Bitmap)
        for icon in possible_icons:
            if os.path.exists(icon):
                self.icon_path_abs = icon
                try: self.iconbitmap(icon)
                except: pass
                break

        # 2. Large Image für GUI laden (Pillow)
        self.large_icon_image = None
        if self.icon_path_abs:
            try:
                # Lade Icon als Bild, Größe 64x64
                pil_img = Image.open(self.icon_path_abs)
                self.large_icon_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(64, 64))
            except Exception as e:
                print(f"Icon load error: {e}")

        self.cloud_path = ""
        self.games_data = []
        self.selected_game_path = ""
        self.app_data_dir = os.path.join(os.getenv('APPDATA'), APP_NAME)
        self.config_file = os.path.join(self.app_data_dir, "config.json")

        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Logo Image
        self.lbl_icon_img = ctk.CTkLabel(self.sidebar, text="", image=self.large_icon_image)
        self.lbl_icon_img.grid(row=0, column=0, padx=20, pady=(30, 10))

        # Title Text
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text=APP_NAME, font=ctk.CTkFont(family="Roboto", size=22, weight="bold"))
        self.lbl_logo.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Admin Status (Modern)
        admin_txt = self.t["admin_ok"] if self.is_admin() else self.t["admin_no"]
        admin_col = "#2CC985" if self.is_admin() else "#FF5555"
        self.lbl_admin = ctk.CTkLabel(self.sidebar, text=admin_txt, font=ctk.CTkFont(size=12, weight="bold"), text_color=admin_col)
        self.lbl_admin.grid(row=2, column=0, pady=(0, 30))

        # Navigation Buttons
        self.btn_nav_setup = self.create_nav_btn(self.t["tab_setup"], "setup", 3)
        self.btn_nav_manage = self.create_nav_btn(self.t["tab_manage"], "manage", 4)
        self.btn_nav_help = self.create_nav_btn(self.t["tab_help"], "help", 5)

        # Bottom Area
        self.lang_var = ctk.StringVar(value="Deutsch")
        self.opt_lang = ctk.CTkOptionMenu(self.sidebar, values=["Deutsch", "English"], variable=self.lang_var, command=self.change_language, width=160, fg_color=("gray70", "gray30"), button_color=("gray60", "gray20"))
        self.opt_lang.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.lbl_cloud_status = ctk.CTkLabel(self.sidebar, text=self.t["lbl_cloud"] + "\n❌", font=("Arial", 11), text_color="gray")
        self.lbl_cloud_status.grid(row=8, column=0, padx=20, pady=(5,0))
        
        self.btn_select_cloud = ctk.CTkButton(self.sidebar, text=self.t["btn_cloud"], fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.select_cloud_folder)
        self.btn_select_cloud.grid(row=9, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.lbl_version = ctk.CTkLabel(self.sidebar, text=f"v{APP_VERSION}", font=("Arial", 9), text_color="gray30")
        self.lbl_version.grid(row=10, column=0, pady=(0, 10))

        # --- FRAMES ---
        self.frame_setup = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_manage = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_help = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.setup_ui_setup()
        self.setup_ui_manage()
        self.setup_ui_help()
        
        self.load_config()
        self.select_frame("setup")

    def create_nav_btn(self, text, frame_name, row):
        btn = ctk.CTkButton(self.sidebar, text=text, height=45, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), font=ctk.CTkFont(size=13), command=lambda: self.select_frame(frame_name))
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        return btn

    def is_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    # --- UI LAYOUTS ---
    
    def setup_ui_setup(self):
        # Header Split Design
        self.lbl_setup_main = ctk.CTkLabel(self.frame_setup, text=self.t["header_setup_main"], font=("Roboto", 26, "bold"))
        self.lbl_setup_main.pack(pady=(40, 0), padx=40, anchor="w")
        
        self.lbl_setup_sub = ctk.CTkLabel(self.frame_setup, text=self.t["header_setup_sub"], font=("Roboto", 14), text_color="gray")
        self.lbl_setup_sub.pack(pady=(0, 30), padx=40, anchor="w")

        # Input Area
        frm = ctk.CTkFrame(self.frame_setup)
        frm.pack(pady=10, padx=40, fill="x")
        frm.grid_columnconfigure(1, weight=1)

        self.lbl_name_txt = ctk.CTkLabel(frm, text=self.t["lbl_name"], font=("Arial", 12, "bold"))
        self.lbl_name_txt.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.entry_name = ctk.CTkEntry(frm, placeholder_text="z.B. Elden Ring", height=35)
        self.entry_name.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        self.lbl_path_txt = ctk.CTkLabel(frm, text=self.t["lbl_path"], font=("Arial", 12, "bold"))
        self.lbl_path_txt.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        frm_browse = ctk.CTkFrame(frm, fg_color="transparent")
        frm_browse.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        frm_browse.grid_columnconfigure(1, weight=1)

        self.btn_browse = ctk.CTkButton(frm_browse, text=self.t["btn_browse"], width=140, command=self.browse_game_folder)
        self.btn_browse.grid(row=0, column=0, sticky="w")
        self.lbl_selected_path = ctk.CTkLabel(frm_browse, text=self.t["no_path"], text_color="gray")
        self.lbl_selected_path.grid(row=0, column=1, padx=15, sticky="w")

        # Big Action Button
        self.btn_start_sync = ctk.CTkButton(self.frame_setup, text=self.t["btn_action"], font=("Arial", 14, "bold"), height=50, fg_color="#2CC985", hover_color="#25A970", text_color="white", command=self.process_new_game)
        self.btn_start_sync.pack(pady=30, padx=40, fill="x")

        # Log Area
        self.lbl_log_title = ctk.CTkLabel(self.frame_setup, text=self.t["log_title"], font=("Arial", 12, "bold"))
        self.lbl_log_title.pack(padx=40, anchor="w")
        self.console = ctk.CTkTextbox(self.frame_setup, height=150)
        self.console.pack(padx=40, pady=(5,40), fill="both", expand=True)

    def setup_ui_manage(self):
        self.lbl_manage_header = ctk.CTkLabel(self.frame_manage, text=self.t["header_manage"], font=("Roboto", 26, "bold"))
        self.lbl_manage_header.pack(pady=(40, 20), padx=40, anchor="w")

        # Toolbar
        frm_tool = ctk.CTkFrame(self.frame_manage, fg_color="transparent")
        frm_tool.pack(fill="x", padx=40)
        
        self.btn_refresh_list = ctk.CTkButton(frm_tool, text=self.t["btn_refresh"], command=self.load_database, width=150)
        self.btn_refresh_list.pack(side="left")

        # List
        self.scroll_list = ctk.CTkScrollableFrame(self.frame_manage, label_text=self.t["list_title"])
        self.scroll_list.pack(padx=40, pady=20, fill="both", expand=True)

    def setup_ui_help(self):
        self.lbl_help_header = ctk.CTkLabel(self.frame_help, text=self.t["header_help"], font=("Roboto", 26, "bold"))
        self.lbl_help_header.pack(pady=(40, 30), padx=40, anchor="w")

        # Container PC 1
        frm_pc1 = ctk.CTkFrame(self.frame_help)
        frm_pc1.pack(fill="x", padx=40, pady=10)
        self.lbl_help_pc1_t = ctk.CTkLabel(frm_pc1, text=self.t["help_pc1_title"], font=("Arial", 16, "bold"), text_color="#66aaff")
        self.lbl_help_pc1_t.pack(anchor="w", padx=20, pady=(15, 5))
        self.lbl_help_pc1_msg = ctk.CTkLabel(frm_pc1, text=self.t["help_pc1_text"], justify="left", font=("Arial", 13))
        self.lbl_help_pc1_msg.pack(anchor="w", padx=20, pady=(0, 15))

        # Container PC 2
        frm_pc2 = ctk.CTkFrame(self.frame_help)
        frm_pc2.pack(fill="x", padx=40, pady=10)
        self.lbl_help_pc2_t = ctk.CTkLabel(frm_pc2, text=self.t["help_pc2_title"], font=("Arial", 16, "bold"), text_color="#ffaa44")
        self.lbl_help_pc2_t.pack(anchor="w", padx=20, pady=(15, 5))
        self.lbl_help_pc2_msg = ctk.CTkLabel(frm_pc2, text=self.t["help_pc2_text"], justify="left", font=("Arial", 13))
        self.lbl_help_pc2_msg.pack(anchor="w", padx=20, pady=(0, 15))

    # --- SWITCHING ---

    def change_language(self, choice):
        self.current_lang = "DE" if choice == "Deutsch" else "EN"
        self.t = LANG[self.current_lang]
        self.save_local_settings()
        
        self.title(self.t["app_title"])
        self.lbl_logo.configure(text=self.t["app_title"])
        
        self.btn_nav_setup.configure(text=self.t["tab_setup"])
        self.btn_nav_manage.configure(text=self.t["tab_manage"])
        self.btn_nav_help.configure(text=self.t["tab_help"])
        
        self.lbl_cloud_status.configure(text=self.t["lbl_cloud"] + "\n" + (self.cloud_path[:20]+"..." if self.cloud_path else "❌"))
        self.btn_select_cloud.configure(text=self.t["btn_cloud"])
        
        # Setup Tab
        self.lbl_setup_main.configure(text=self.t["header_setup_main"])
        self.lbl_setup_sub.configure(text=self.t["header_setup_sub"])
        self.lbl_name_txt.configure(text=self.t["lbl_name"])
        self.lbl_path_txt.configure(text=self.t["lbl_path"])
        self.btn_browse.configure(text=self.t["btn_browse"])
        if not self.selected_game_path:
            self.lbl_selected_path.configure(text=self.t["no_path"])
        self.btn_start_sync.configure(text=self.t["btn_action"])
        self.lbl_log_title.configure(text=self.t["log_title"])
        
        # Manage Tab
        self.lbl_manage_header.configure(text=self.t["header_manage"])
        self.btn_refresh_list.configure(text=self.t["btn_refresh"])
        self.scroll_list.configure(label_text=self.t["list_title"])
        
        # Help Tab
        self.lbl_help_header.configure(text=self.t["header_help"])
        self.lbl_help_pc1_t.configure(text=self.t["help_pc1_title"])
        self.lbl_help_pc1_msg.configure(text=self.t["help_pc1_text"])
        self.lbl_help_pc2_t.configure(text=self.t["help_pc2_title"])
        self.lbl_help_pc2_msg.configure(text=self.t["help_pc2_text"])

        # Admin
        admin_txt = self.t["admin_ok"] if self.is_admin() else self.t["admin_no"]
        self.lbl_admin.configure(text=admin_txt)

        self.load_database()

    def select_frame(self, name):
        self.frame_setup.grid_forget()
        self.frame_manage.grid_forget()
        self.frame_help.grid_forget()
        
        active_color = ("gray75", "gray25")
        transparent = "transparent"
        
        # Reset all
        self.btn_nav_setup.configure(fg_color=transparent)
        self.btn_nav_manage.configure(fg_color=transparent)
        self.btn_nav_help.configure(fg_color=transparent)

        if name == "setup":
            self.frame_setup.grid(row=0, column=1, sticky="nsew")
            self.btn_nav_setup.configure(fg_color=active_color)
        elif name == "manage":
            self.frame_manage.grid(row=0, column=1, sticky="nsew")
            self.btn_nav_manage.configure(fg_color=active_color)
            self.load_database()
        elif name == "help":
            self.frame_help.grid(row=0, column=1, sticky="nsew")
            self.btn_nav_help.configure(fg_color=active_color)

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

    # --- LOGIC PC 1 ---
    def process_new_game(self):
        if not self.cloud_path: return messagebox.showerror("Error", self.t["msg_cloud_err"])
        name = self.entry_name.get()
        if not name: return messagebox.showerror("Error", self.t["msg_name_err"])
        if not self.selected_game_path: return messagebox.showerror("Error", self.t["msg_path_err"])

        original_path = self.selected_game_path
        cloud_game_dir = os.path.join(self.cloud_path, name)
        
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

    # --- LOGIC RESTORE / LINK ---
    def restore_origin(self, game):
        target_local = os.path.expandvars(game["path_pattern"])
        cloud_source = os.path.join(self.cloud_path, game["cloud_folder"])
        if not messagebox.askyesno(self.t["restore_title"], self.t["restore_msg"]): return
        try:
            if os.path.exists(target_local):
                if os.path.islink(target_local): os.remove(target_local)
                else: os.rename(target_local, target_local + "_OLD_" + datetime.datetime.now().strftime("%M%S"))
            if os.path.exists(cloud_source): shutil.copytree(cloud_source, target_local)
            else: return messagebox.showerror("Fehler", "Cloud-Daten nicht gefunden!")
            shutil.rmtree(cloud_source, onerror=self.remove_readonly)
            parent = os.path.dirname(target_local)
            bkup = os.path.join(parent, "_BACKUP_SAVE")
            if os.path.exists(bkup): shutil.rmtree(bkup, onerror=self.remove_readonly)
            self.games_data = [g for g in self.games_data if g["name"] != game["name"]]
            self.save_database()
            self.load_database()
            messagebox.showinfo("Fertig", "Ursprungszustand wiederhergestellt.")
        except Exception as e: messagebox.showerror("Fehler", str(e))

    def unlink_client(self, game):
        target = os.path.expandvars(game["path_pattern"])
        if not messagebox.askyesno(self.t["unlink_title"], self.t["unlink_msg"]): return
        try:
            if os.path.exists(target) and os.path.islink(target): os.remove(target)
            backup = target + "_LOCAL_BEFORE_LINK"
            if os.path.exists(backup):
                os.rename(backup, target)
                messagebox.showinfo("Info", "Getrennt & Backup wiederhergestellt.")
            else:
                if not os.path.exists(target): os.makedirs(target)
                messagebox.showinfo("Info", "Getrennt (Kein Backup gefunden).")
        except Exception as e: messagebox.showerror("Fehler", str(e))

    def forget_game_entry(self, game):
        if messagebox.askyesno(self.t["forget_title"], self.t["forget_msg"]):
            self.games_data = [g for g in self.games_data if g["name"] != game["name"]]
            self.save_database()
            self.load_database()

    def link_on_pc2(self, game):
        target = os.path.expandvars(game["path_pattern"])
        source = os.path.join(self.cloud_path, game["cloud_folder"])
        if not os.path.exists(source): return messagebox.showerror("Error", "Cloud folder missing.")
        if os.path.exists(target):
            if os.path.islink(target): return
            backup = target + "_LOCAL_BEFORE_LINK"
            if os.path.exists(backup): shutil.rmtree(backup)
            os.rename(target, backup)
            messagebox.showinfo("Backup", f"Lokal gesichert:\n{os.path.basename(backup)}")
        parent = os.path.dirname(target)
        if not os.path.exists(parent): os.makedirs(parent)
        try:
            os.symlink(source, target, target_is_directory=True)
            messagebox.showinfo("OK", f"Linked {game['name']}!")
        except Exception as e: messagebox.showerror("Error", str(e))

    # --- DB ---
    def add_to_db(self, name, path):
        self.load_database()
        user_profile = os.environ.get('USERPROFILE')
        path_normalized = path.replace("/", "\\")
        if user_profile and path_normalized.startswith(user_profile):
            clean_path = path_normalized.replace(user_profile, "%USERPROFILE%")
        else: clean_path = path
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
        ctk.CTkLabel(r, text=game["name"], font=("Arial", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(r, text=self.t["btn_forget"], width=40, fg_color="#444", hover_color="#666", command=lambda g=game: self.forget_game_entry(g)).pack(side="right", padx=(5, 10))
        ctk.CTkButton(r, text=self.t["btn_restore"], width=120, fg_color="#550000", hover_color="#880000", command=lambda g=game: self.restore_origin(g)).pack(side="right", padx=5)
        ctk.CTkButton(r, text=self.t["btn_unlink"], width=120, fg_color="#C06000", hover_color="#E08000", command=lambda g=game: self.unlink_client(g)).pack(side="right", padx=5)
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