# compose
A minimal, GTK-native text editor

![compose — main editor window](/screenshots/compose-main.png)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why compose?](#why-compose)
3. [Installation](#installation)
4. [Features](#features)
5. [Screenshots](#screenshots)
6. [Future Plans](#future-plans)

---

## Introduction

> This app was loosely inspired by TextEdit of macOS. My intention was not to create a clone of or to recreate all the features from TextEdit, but instead, to create an equally minimal GTK-native equivalent for GNU/Linux systems (as I didn't find anything that matched my requirements).

**compose** is a writing-focused plain text editor, that is designed with one simple concept — easy translation of thoughts into text. The main editor window intentionally contains almost no visible controls, making the text itself the focal point. The UI, instead, is mainly keyboard-driven. All the settings are consolidated into one global settings window. 

**compose** also has some niche/unconventional features, such as a temporary spreadsheet utility for quick tabulation of whatever you have in mind, and a shell-like manual path entry method for saving files. It also has support for custom automatic file extensions. 

---

## Why compose?

I wanted a text editor that felt at home in GTK environments while remaining focused on writing. Most editors I tried either included features I personally didn't need, or did not fit naturally into my setup.

compose was built to provide a calm, keyboard-driven writing experience with a native GTK interface and a small, understandable codebase.

---

## Installation

### Platform Support

This application is GTK-native, and is mainly made for GNU/Linux systems. It is developed on Arch Linux and is supported and tested on:

* Any GNU/Linux Distribution
* macOS

It may work on other operating systems as well, but this is currently untested.

> Some keyboard shortcuts are different on macOS. 

### Requirements

* Python 3.12+
* GTK4
* PyGObject
* *Also, DM Mono is required to render the UI text in the application, and the editor font itself is also set to DM Mono. System fonts will be available in future versions. Install it [here](https://fonts.google.com/specimen/DM+Mono?preview.script=Latn).*

> *You can use any font of your preference, but it requires editing the source code, since the usage of DM Mono is hard-coded into compose.*

> *While testing on macOS, I found that it does not use DM Mono, but that might just be a macOS quirk.*

### Clone Repository

Make sure you have `git` installed. Run the following commands in your Terminal:

1. `git clone https://github.com/sk-7-dazed/compose`
2. `cd compose`

### Install Dependencies

#### Arch Linux
`sudo pacman -S python python-gobject gtk4`

#### macOS (with `homebrew`)
`brew install python pygobject3 gtk4`

#### Fedora
`sudo dnf install python3-gobject gtk4`

#### Ubuntu/Debian
`sudo apt install python3-gi gir1.2-gtk-4.0`

### Run compose
`python main.py` or `./compose`

### Optional but Recommended: Desktop Integration

> This section only applies to GNU/Linux desktop environments that support XDG desktop entries.

Create `~/.local/share/applications/compose.desktop` with the following contents:

```{ini}
[Desktop Entry]
Type = Application
Name = compose
Comment = Minimal GTK4 text editor
Exec = /path/to/compose/compose
Terminal = false
Categories = Utility;TextEditor;
```

After creating the desktop file, compose should appear in rofi, other application launchers, desktop menus, etc.

---

## Features

compose is minimal and some features are intentionally excluded to preserve its calm plain text nature. It is not an IDE.

* Niche features
    * Temporary spreadsheet utility (accessible via keyboard shortcut, or by clicking the `⍼` button in the Preferences window)
    * Shell-like path entry save method
    * Dynamic title bar indicating session state
* Basic text editing features
    * New, Open, Save, Save As
    * Undo, Redo
    * Cut, Copy, Paste
    * Font size controls
* Appearance
    * Fully respects your GTK4 theme
    * Configurable word wrapping
    * Configurable cursor styles
    * Centered writing mode
* Keyboard shortcuts
    * Extensive keyboard shortcut support with built-in documentation
    * Custom line deletion shortcuts
* Preferences
    * Persistent settings (via Preferences window, or manually configurable by editing `~/.config/compose/settings.json`)
    * Window size controls
    * Startup behavior options
    * Session recovery
    * Save method configuration
    * Default directory support

---

## Screenshots

> Appearance varies from theme to theme. Install and use a GTK4 theme that suits your preferences. Keep in mind that in order for compose to use a dark theme, your GTK4 theme must be dark-themed too.

### Main editor

![compose with default settings](/screenshots/compose-normal.png)

### Centered writing mode

![compose with centered text and block cursor](/screenshots/compose-center.png)

### Preferences

![Preferences window](/screenshots/compose-prefs.png)

### Path entry save method

![Manual path entry save dialog](/screenshots/compose-save.png)

### Temporary Spreadsheet utility

![Temporary spreadsheet utility](/screenshots/compose-spreadsheet.png)

### Keyboard shortcuts window

![Keyboard shortcuts window](/screenshots/compose-kb.png)

---

## Future plans

* System fonts support
* Find & Replace
* Terminal launch mode
* CSV export/import for spreadsheet
* Spreadsheet navigation
* Autocomplete for manual path entry mode

---

## Closing note

compose began as a personal summer project to create the text editor I wanted but could not find.

It is intentionally small, intentionally focused, and intentionally opinionated. Every feature exists because I found it useful, and every omission is equally deliberate.

If compose happens to fit your workflow/needs, then it has achieved exactly what it was designed to do.

---
