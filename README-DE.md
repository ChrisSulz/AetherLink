<div align="center">

  <img src="assets/app_icon.ico" alt="AetherLink Logo" width="120" height="120">

# AetherLink

**Nahtlose Spielstand-Synchronisation für Windows**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plattform](https://img.shields.io/badge/Plattform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

  <p>
    <a href="README.md">🇬🇧 Englisch</a> •
    <b>🇩🇪 Deutsch</b>
  </p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-funktionsweise">Funktionsweise</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-anleitung">Anleitung</a>
  </p>

</div>

---

## 🚀 Über das Projekt

**AetherLink** ist ein modernes Tool, um lokale Spielstände mithilfe von **Symbolischen Verknüpfungen (Symlinks)** über Cloud-Anbieter (Google Drive, Dropbox, OneDrive) zu synchronisieren.

AetherLink unterscheidet intelligent zwischen dem **Ursprungs-PC** (wo der Save herkommt) und **Client-PCs** (wo du weiterspielen willst). Sicherheit steht an erster Stelle: Vor jeder kritischen Aktion werden automatisch lokale Backups erstellt.

---

## 📸 Screenshots

|              **Dashboard & Setup**               |         **Verwaltung & Wiederherstellung**         |
| :----------------------------------------------: | :------------------------------------------------: |
| ![Dashboard](assets/Screenshot_Dashboard_DE.png) | ![Management](assets/Screenshot_Management_DE.png) |
|  _Moderne dunkle GUI mit simpler Konfiguration_  |   _Links verwalten und Backups wiederherstellen_   |

---

## ✨ Features

- **☁️ Universeller Cloud-Sync:** Funktioniert mit jedem Ordner, der mit einer Cloud synchronisiert wird.
- **🛡️ Sicherheit zuerst:** Automatische `.zip`-Backups vor jedem Verschieben oder Verlinken.
- **🖥️ Multi-PC Logik:**
  - **PC 1 (Ursprung):** Verschiebt Saves in die Cloud und verlinkt sie.
  - **PC 2+ (Client):** Erkennt vorhandene Saves, sichert diese lokal und verlinkt zur Cloud.
- **↩️ Smart Restore:** Verknüpfungen einfach aufheben und Originaldateien wiederherstellen.
- **🎨 Modernes UI:** Schickes Windows 11 Design (Dark-Mode) mit `CustomTkinter`.
- **🌍 Mehrsprachig:** Komplette Unterstützung für **Deutsch** und **Englisch**.

---

## ⚙️ Funktionsweise

AetherLink nutzt die **"Sync & Link"** Methode:

1.  **Verschieben:** Das Programm verschiebt deinen lokalen Save-Ordner (z.B. aus `AppData`) in deinen Cloud-Ordner.
2.  **Verlinken:** Es platziert eine _Symbolische Verknüpfung_ (Symlink) am ursprünglichen Ort.
3.  **Sync:** Das Spiel denkt, die Dateien wären noch da, aber sie liegen physisch in der Cloud.

---

## 📥 Installation

### Option A: Aus dem Quellcode starten (Python)

1.  **Repository klonen**
    ```bash
    git clone https://github.com/DEIN_BENUTZERNAME/AetherLink.git
    cd AetherLink
    ```
2.  **Abhängigkeiten installieren**
    ```bash
    pip install customtkinter pillow pyinstaller
    ```
3.  **Anwendung starten**
    ```bash
    python aetherlink.pyw
    ```

### Option B: Ausführbare Datei (.exe) erstellen

Wenn du eine portable Datei für die Nutzung auf mehreren PCs möchtest:

1.  Führe das beigefügte Build-Skript aus (falls vorhanden) oder nutze:
    ```bash
    py -m PyInstaller --noconsole --onefile --uac-admin --clean --icon=app_icon.ico --add-data "app_icon.ico;." --name=AetherLink aetherlink.pyw
    ```
2.  Die Datei `AetherLink.exe` befindet sich anschließend im Ordner `dist`.

---

## 🎮 Anleitung

### 🖥️ Auf PC 1 (Der Ursprung)

_Dort, wo sich deine Spielstände aktuell befinden._

1.  Wähle deinen **Cloud-Ordner** (unten links).
2.  Gehe zu **„Add Game“**.
3.  Gib den Spielnamen ein und suche den lokalen Speicherordner.
4.  Klicke auf **„Backup & Sync“**.

### 💻 Auf PC 2, 3... (Die Clients)

_Dort, wo du weiterspielen möchtest._

1.  Wähle den **gleichen Cloud-Ordner**.
2.  Gehe zu **„Manage“**.
3.  Suche das Spiel in der Liste und klicke auf den blauen **„🔗 Link Here“**-Button.
    - _Hinweis: Falls auf PC 2 bereits ein lokaler Spielstand existiert, erstellt AetherLink vor dem Verknüpfen automatisch ein Backup davon._

### 🔓 Trennen / Deinstallieren

- **Client:** Klicke auf „Unlink (Client)“, um die Verknüpfung zu entfernen und lokale Backups wiederherzustellen. Die Cloud-Daten bleiben sicher.
- **Origin (Ursprung):** Klicke auf „Reset (Origin)“, um die Daten aus der Cloud zurückzuholen und die Cloud-Kopie zu löschen.

---

## 🤝 Mitwirken

1.  Forke das Projekt
2.  Erstelle deinen Feature Branch (`git checkout -b feature/TollesFeature`)
3.  Committe deine Änderungen (`git commit -m 'Füge ein TollesFeature hinzu'`)
4.  Pushe auf den Branch (`git push origin feature/TollesFeature`)
5.  Eröffne einen Pull Request

---

## 📄 Lizenz

Verbreitet unter der MIT-Lizenz. Weitere Informationen finden Sie unter `LICENSE`.
