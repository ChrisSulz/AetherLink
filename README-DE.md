<div align="center">

  <img src="assets/app_icon.ico" alt="AetherLink Logo" width="120" height="120">

# AetherLink

**Nahtlose Spielstand-Synchronisation für Windows**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plattform](https://img.shields.io/badge/Plattform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Vibe Coding](https://img.shields.io/badge/Built%20with-Vibe%20Coding-purple?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/)

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

> **✨ Erstellt per Vibe Coding:** Dieses gesamte Projekt – vom Konzept bis zur letzten Codezeile – entstand in einem iterativen "Vibe Coding"-Prozess.

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

### Option A: Aus dem Quellcode (Python)

```bash
pip install customtkinter pillow pyinstaller
python aetherlink.pyw
```
