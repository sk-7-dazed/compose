import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class kb_shortcuts(Gtk.Window):

    def __init__(self, parent):

        super().__init__()

        self.set_transient_for(parent)
        self.set_title("Keyboard Shortcuts — compose")
        self.set_default_size(500, 500)

        # making it scrollable
        scrollable_window = Gtk.ScrolledWindow()
        self.set_child(scrollable_window)
        
        # monospace font ui
        css = """
        window 
        {
            font-family: "DM Mono Light";
            font-size: 11pt;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        display = self.get_display()
        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        # main vertical box
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12
        )

        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(24)

        scrollable_window.set_child(main_box)

        # helper function
        def make_key(label_text):
            return Gtk.Button(label=label_text)

        # helper function
        def make_row(action, *keys):

            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=8
            )

            label = Gtk.Label(label=f"· {action}")
            label.set_xalign(0)
            label.set_hexpand(True)

            row.append(label)

            for key in keys:
                row.append(make_key(key))

            return row

        # =========================================================
        # FILE SECTION
        # =========================================================

        file_header = Gtk.Label(label="File")
        file_header.set_xalign(0)

        main_box.append(file_header)

        main_box.append(
            make_row("New File", "Ctrl", "N")
        )

        main_box.append(
            make_row("Open File", "Ctrl", "O")
        )

        main_box.append(
            make_row("Save File", "Ctrl", "S")
        )

        main_box.append(
            make_row("Save As", "Ctrl", "Shift", "S")
        )

        main_box.append(
                make_row("Open Temporary Spreadsheet", "Ctrl", "Shift", "T")
                )

        main_box.append(
            make_row("Quit", "Ctrl", "Q")
        )

        main_box.append(
            make_row("Open Preferences", "Ctrl", ",")
        )

        main_box.append(
                make_row("Show Keyboard Shortcuts", "Ctrl", "Shift", "?")
                )

        file_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(file_sep)

        # =========================================================
        # APPEARANCE SECTION
        # =========================================================

        appearance_header = Gtk.Label(label="Appearance")
        appearance_header.set_xalign(0)

        main_box.append(appearance_header)

        main_box.append(
            make_row("Increase Font Size", "Ctrl", "+")
        )

        main_box.append(
            make_row("Decrease Font Size", "Ctrl", "-")
        )

        main_box.append(
            make_row("Toggle Centered Text", "Ctrl", "Space")
        )

        main_box.append(
            make_row("Toggle Cursor Type", "Insert")
        )

        appearance_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(appearance_sep)

        # =========================================================
        # EDITING SECTION
        # =========================================================

        editing_header = Gtk.Label(label="Editing")
        editing_header.set_xalign(0)

        main_box.append(editing_header)

        main_box.append(
            make_row("Cut", "Ctrl", "X")
        )

        main_box.append(
            make_row("Copy", "Ctrl", "C")
        )

        main_box.append(
            make_row("Paste", "Ctrl", "V")
        )

        main_box.append(
            make_row("Undo", "Ctrl", "Z")
        )

        main_box.append(
            make_row("Redo", "Ctrl", "Shift", "Z")
        )

        main_box.append(
                make_row("Open Emoji Picker", "Ctrl", ".")
                )

        editing_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(editing_sep)

        # =========================================================
        # NAVIGATION SECTION
        # =========================================================

        navigation_header = Gtk.Label(label="Navigation")
        navigation_header.set_xalign(0)

        main_box.append(navigation_header)

        main_box.append(
            make_row("Move One Character Left", "←")
        )

        main_box.append(
            make_row("Move One Character Right", "→")
        )

        main_box.append(
            make_row("Move One Word Left", "Ctrl", "←")
        )

        main_box.append(
            make_row("Move One Word Right", "Ctrl", "→")
        )

        main_box.append(
            make_row("Move One Line Up", "↑")
        )

        main_box.append(
            make_row("Move One Line Down", "↓")
        )

        main_box.append(
            make_row("Move To Beginning Of File", "Ctrl", "Home")
        )

        main_box.append(
            make_row("Move To End Of File", "Ctrl", "End")
        )

        main_box.append(
            make_row("Move To Beginning Of Line", "Home")
        )

        main_box.append(
            make_row("Move To End Of Line", "End")
        )

        navigation_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(navigation_sep)

        # =========================================================
        # SELECTION SECTION
        # =========================================================

        selection_header = Gtk.Label(label="Selection")
        selection_header.set_xalign(0)

        main_box.append(selection_header)

        main_box.append(
            make_row("Select One Character Left", "Shift", "←")
        )

        main_box.append(
            make_row("Select One Character Right", "Shift", "→")
        )

        main_box.append(
            make_row("Select One Word Left", "Ctrl", "Shift", "←")
        )

        main_box.append(
            make_row("Select One Word Right", "Ctrl", "Shift", "→")
        )

        main_box.append(
            make_row("Select One Line Up", "Shift", "↑")
        )

        main_box.append(
            make_row("Select One Line Down", "Shift", "↓")
        )

        main_box.append(
            make_row(
                "Select Till Beginning Of File",
                "Ctrl",
                "Shift",
                "Home"
            )
        )

        main_box.append(
            make_row(
                "Select Till End Of File",
                "Ctrl",
                "Shift",
                "End"
            )
        )

        main_box.append(
            make_row(
                "Select Till Beginning Of Line",
                "Shift",
                "Home"
            )
        )

        main_box.append(
            make_row(
                "Select Till End Of Line",
                "Shift",
                "End"
            )
        )

        main_box.append(
            make_row("Select All", "Ctrl", "A")
        )

        selection_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(selection_sep)

        # =========================================================
        # DELETION SECTION
        # =========================================================

        deletion_header = Gtk.Label(label="Deletion")
        deletion_header.set_xalign(0)

        main_box.append(deletion_header)

        main_box.append(
            make_row("Delete One Character Left", "Backspace")
        )

        main_box.append(
            make_row("Delete One Character Right", "Delete")
        )

        main_box.append(
            make_row("Delete One Word Left", "Ctrl", "Backspace")
        )

        main_box.append(
            make_row("Delete One Word Right", "Ctrl", "Delete")
        )

        main_box.append(
            make_row(
                "Delete Till Beginning Of Line",
                "Alt",
                "Backspace"
            )
        )

        main_box.append(
            make_row(
                "Delete Till End Of Line",
                "Alt",
                "Delete"
            )
        )

        deletion_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(deletion_sep)


        # =========================================================
        # SPREADSHEET SECTION
        # =========================================================

        ss_header = Gtk.Label(label="Spreadsheet")
        ss_header.set_xalign(0)

        main_box.append(ss_header)

        main_box.append(
            make_row("Move Down", "↓")
        )
        main_box.append(
            make_row("Move Up", "↑")
        )

        main_box.append(
            make_row("Move Right", "Tab")
        )

        main_box.append(
            make_row("Move Left", "Shift", "Tab")
        )

        ss_sep = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        main_box.append(ss_sep)
