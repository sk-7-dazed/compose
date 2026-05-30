import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import settings_sync

from kb_shortcuts import kb_shortcuts
from spreadsheet import spreadsheet
from settings_mgr import DEFAULT_SETTINGS, save_settings

import os
import webbrowser


class settings_popup(Gtk.Window):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.set_title("Preferences — compose")
        self.set_default_size(300,300)

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

        # --------------------------------------------------
        # main box

        main_box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 12
        )

        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        self.set_child(main_box)

        # --------------------------------------------------
        # separators

        b_sep1 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        b_sep2 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep1 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep2 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep3 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep4 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep5 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        sep6 = Gtk.Separator(
            orientation = Gtk.Orientation.HORIZONTAL
        )

        # --------------------------------------------------
        # header box

        header_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(b_sep1)
        main_box.append(header_box)

        header_label = Gtk.Label(
            label = "compose — v1.0"
        )

        header_label.set_xalign(0)

        header_box.append(header_label)

        main_box.append(b_sep2)

        # spacer
        spacer1 = Gtk.Box()
        spacer1.set_hexpand(True)

        header_box.append(spacer1)

        # about button
        about_button = Gtk.Button(label = "🛈")

        header_box.append(about_button)

        about_button.connect(
            "clicked",
            self.open_about
        )

        # --------------------------------------------------
        # font section

        font_label = Gtk.Label(label = "Font")
        font_label.set_xalign(0)

        main_box.append(font_label)

        # --------------------------------------------------
        # font face

        face_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(face_box)

        face_label = Gtk.Label(
            label = "· Face: "
        )

        face_label.set_xalign(0)

        face_box.append(face_label)

        fonts = Gtk.StringList.new(["DM Mono"])

        font_dropdown = Gtk.DropDown.new(fonts, None)

        face_box.append(font_dropdown)

        # --------------------------------------------------
        # font size

        size_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 6
        )

        main_box.append(size_box)

        size_label = Gtk.Label(
            label = "· Size: "
        )

        size_label.set_xalign(0)

        size_box.append(size_label)

        minus_button = Gtk.Button(label = "-")
        plus_button  = Gtk.Button(label = "+")

        self.font_size_entry = Gtk.Entry()

        self.font_size_entry.set_text(
            str(
                self.parent.settings["font_size"]
            )
        )

        self.font_size_entry.set_alignment(0.5)

        self.font_size_entry.set_width_chars(4)
        self.font_size_entry.set_max_width_chars(4)

        size_box.append(minus_button)
        size_box.append(self.font_size_entry)
        size_box.append(plus_button)

        # --------------------------------------------------
        # font size sync

        self.font_size_entry.connect(
            "activate",
            lambda entry:
                settings_sync.apply_font_size_from_entry(
                    self.parent,
                    entry
                )
        )

        plus_button.connect(
            "clicked",
            lambda button:
                settings_sync.increase_font_and_sync(
                    self.parent
                )
        )

        minus_button.connect(
            "clicked",
            lambda button:
                settings_sync.decrease_font_and_sync(
                    self.parent
                )
        )

        # --------------------------------------------------
        # separator

        main_box.append(sep1)

        # --------------------------------------------------
        # appearance section

        appearance_label = Gtk.Label(
            label = "Appearance"
        )

        appearance_label.set_xalign(0)

        main_box.append(appearance_label)

        # --------------------------------------------------
        # wrap mode

        wrap_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(wrap_box)

        wrap_type_label = Gtk.Label(
            label = "· Wrap Mode: "
        )

        wrap_type_label.set_xalign(0)

        wrap_box.append(wrap_type_label)

        wrap_modes = Gtk.StringList.new(
            ["None ", "Word ", "Character "]
        )

        self.wrap_dropdown = Gtk.DropDown.new(
            wrap_modes,
            None
        )

        wrap_box.append(self.wrap_dropdown)

        # update json
        self.wrap_dropdown.connect(
                "notify::selected", 
                lambda dropdown, param:
                settings_sync.apply_wrap_from_dropdown(self.parent, dropdown)
                )

        # --------------------------------------------------
        # cursor type

        cursor_type_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(cursor_type_box)

        cursor_type_label = Gtk.Label(
            label = "· Cursor Type: "
        )

        cursor_type_label.set_xalign(0)

        cursor_type_box.append(cursor_type_label)

        cursors = Gtk.StringList.new(
            ["Block ", "Line "]
        )

        self.cursor_type_dropdown = Gtk.DropDown.new(
            cursors,
            None
        )

        cursor_type_box.append(self.cursor_type_dropdown)

        # load current cursor type
        self.cursor_type_dropdown.set_selected(

            0 if self.parent.settings["cursor_type"] == "block"

            else 1
        )

        # dropdown changed
        self.cursor_type_dropdown.connect(
            "notify::selected",

            lambda dropdown, param:
                settings_sync.apply_cursor_from_dropdown(
                    self.parent,
                    dropdown
                )
        )


        # --------------------------------------------------
        # cursor blink

        cursor_blink_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(cursor_blink_box)

        self.cursor_blink_check = Gtk.CheckButton()

        cursor_blink_box.append(self.cursor_blink_check)

        self.cursor_blink_check.set_active(False)

        cursor_blink_label = Gtk.Label(
            label = "Blinking cursor"
        )

        cursor_blink_label.set_xalign(0)

        cursor_blink_box.append(cursor_blink_label)

        # load current cursor blink state
        self.cursor_blink_check.set_active(
            self.parent.settings["cursor_blink"]
        )

        # if checkbox changed
        self.cursor_blink_check.connect(
            "toggled",

            lambda checkbox:
                settings_sync.apply_cursor_blink_from_checkbox(
                    self.parent,
                    checkbox
                )
        )

        # --------------------------------------------------
        # centered text

        center_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(center_box)

        self.center_check = Gtk.CheckButton()

        center_box.append(self.center_check)

        self.center_check.set_active(False)

        center_label = Gtk.Label(
            label = "Centered Text"
        )

        center_label.set_xalign(0)

        center_box.append(center_label)

        # load current state
        self.center_check.set_active(
            self.parent.settings["centered_text"]
        )

        # checkbox changed
        self.center_check.connect(
            "toggled",

            lambda checkbox:
                settings_sync.apply_centered_from_checkbox(
                    self.parent,
                    checkbox
                )
        )

        # --------------------------------------------------
        # full path in title

        title_path_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(title_path_box)

        self.title_path_check = Gtk.CheckButton()

        title_path_box.append(self.title_path_check)

        self.title_path_check.set_active(False)

        title_path_label = Gtk.Label(
            label = "File Path In Title Bar"
        )

        title_path_label.set_xalign(0)

        title_path_box.append(title_path_label)

        # load current full path state
        self.title_path_check.set_active(
            self.parent.settings["show_full_path"]
        )

        # checkbox changed
        self.title_path_check.connect(
            "toggled",

            lambda checkbox:
                settings_sync.apply_full_path_from_checkbox(
                    self.parent,
                    checkbox
                )
        )

        # --------------------------------------------------
        # separator

        main_box.append(sep2)

        # --------------------------------------------------
        # save section

        save_label = Gtk.Label(label = "Save")

        save_label.set_xalign(0)

        main_box.append(save_label)

        # --------------------------------------------------
        # save method

        save_method_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(save_method_box)

        save_method_label = Gtk.Label(
            label = "· Method: "
        )

        save_method_label.set_xalign(0)

        save_method_box.append(save_method_label)

        save_methods = Gtk.StringList.new(
            ["File Dialog ", "Manual Path Entry "]
        )

        self.save_methods_dropdown = Gtk.DropDown.new(
            save_methods,
            None
        )

        save_method_box.append(self.save_methods_dropdown)

        # load current save method
        self.save_methods_dropdown.set_selected(

            0 if self.parent.settings["save_method"] == "dialog"

            else 1
        )

        # dropdown changed
        self.save_methods_dropdown.connect(
            "notify::selected",

            lambda dropdown, param:
                settings_sync.apply_save_method_from_dropdown(
                    self.parent,
                    dropdown
                )
        )

        # --------------------------------------------------
        # default directory

        default_dir_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(default_dir_box)

        default_dir_label = Gtk.Label(
            label = "· Default Directory: "
        )

        default_dir_label.set_xalign(0)

        default_dir_box.append(default_dir_label)

        self.default_dir_entry = Gtk.Entry()

        self.default_dir_entry.set_text(self.parent.settings["default_dir"])

        self.default_dir_entry.set_alignment(0.5)

        self.default_dir_entry.set_width_chars(25)
        self.default_dir_entry.set_max_width_chars(30)

        default_dir_box.append(self.default_dir_entry)

        self.default_dir_entry.connect(
        "activate",
        lambda entry:
            settings_sync.apply_default_dir(
                self.parent,
                entry.get_text()
            )
    )

        # --------------------------------------------------
        # missing directories

        missing_dir_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(missing_dir_box)

        missing_dir_label = Gtk.Label(
            label = "· Missing Directories: "
        )

        missing_dir_label.set_xalign(0)

        missing_dir_box.append(missing_dir_label)

        missing_dirs = Gtk.StringList.new(
            ["Error ", "Automatically Create "]
        )

        self.missing_dir_dropdown = Gtk.DropDown.new(
            missing_dirs,
            None
        )

        missing_dir_box.append(self.missing_dir_dropdown)

        self.missing_dir_dropdown.set_selected(

        0 if self.parent.settings["missing_dirs"] == "error"

        else 1
    )

        self.missing_dir_dropdown.connect(
        "notify::selected",

        lambda dropdown, param:
            settings_sync.apply_missing_dirs(
                self.parent,
                "error" if dropdown.get_selected() == 0
                else "create"
            )
    )

        # --------------------------------------------------
        # default extension

        ext_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(ext_box)

        self.ext_check = Gtk.CheckButton()
        ext_box.append(self.ext_check)
        self.ext_check.set_active(True)
        self.ext_check.set_active(self.parent.settings["default_extension_yn"])

        self.ext_check.connect(
            "toggled",
            lambda checkbox:
                settings_sync.apply_default_extension_toggle(
                    self.parent,
                    checkbox.get_active()
                )
        )
        
        ext_label = Gtk.Label(
            label = "Default Extension: "
        )

        ext_label.set_xalign(0)

        ext_box.append(ext_label)

        self.ext_entry = Gtk.Entry()

        self.ext_entry.set_text(self.parent.settings["default_extension"])

        self.ext_entry.set_alignment(0.5)

        self.ext_entry.set_width_chars(6)
        self.ext_entry.set_max_width_chars(10)

        ext_box.append(self.ext_entry)

        self.ext_entry.connect(
        "activate",

        lambda entry:
            settings_sync.apply_default_extension(
                self.parent,
                entry.get_text()
            )
    )

        # --------------------------------------------------
        # separator

        main_box.append(sep3)

        # --------------------------------------------------
        # startup section

        startup_label = Gtk.Label(
            label = "Startup Behavior"
        )

        startup_label.set_xalign(0)

        main_box.append(startup_label)

        # --------------------------------------------------
        # startup behavior

        startup_open_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(startup_open_box)

        startup_open_label = Gtk.Label(
            label = "· On Launch: "
        )

        startup_open_label.set_xalign(0)

        startup_open_box.append(startup_open_label)

        open_options = Gtk.StringList.new(
            [
                "Empty (New) File ",
                "Last Saved File ",
                "Restore Previous Session"
            ]
        )

        self.startup_open_dropdown = Gtk.DropDown.new(
            open_options,
            None
        )

        startup_open_box.append(self.startup_open_dropdown)

        # load current startup behavior
        self.startup_open_dropdown.set_selected(

            {
                "empty": 0,
                "last_saved": 1,
                "restore": 2
            }[
                self.parent.settings[
                    "startup_behavior"
                ]
            ]
        )

        # dropdown changed
        self.startup_open_dropdown.connect(
            "notify::selected",

            lambda dropdown, param:
                settings_sync.apply_startup_from_dropdown(
                    self.parent,
                    dropdown
                )
        )

        # --------------------------------------------------
        # window size

        win_size_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 9
        )

        main_box.append(win_size_box)

        win_size_label = Gtk.Label(
            label = "· Window Size: "
        )

        win_size_label.set_xalign(0)

        win_width_minus = Gtk.Button(label = "-")
        win_width_plus  = Gtk.Button(label = "+")

        self.win_width_entry = Gtk.Entry()

        self.win_width_entry.set_alignment(0.5)
        self.win_width_entry.set_text(str(self.parent.settings["win_width"]))

        self.win_width_entry.set_width_chars(4)
        self.win_width_entry.set_max_width_chars(4)

        win_height_minus = Gtk.Button(label = "-")
        win_height_plus  = Gtk.Button(label = "+")

        self.win_height_entry = Gtk.Entry()

        self.win_height_entry.set_alignment(0.5)
        self.win_height_entry.set_text(str(self.parent.settings["win_height"]))

        self.win_height_entry.set_width_chars(4)
        self.win_height_entry.set_max_width_chars(4)

        win_x_label = Gtk.Label(label = "x")

        win_x_label.set_xalign(0)

        win_size_box.append(win_size_label)

        win_size_box.append(win_width_minus)
        win_size_box.append(self.win_width_entry)
        win_size_box.append(win_width_plus)

        win_size_box.append(win_x_label)

        win_size_box.append(win_height_minus)
        win_size_box.append(self.win_height_entry)
        win_size_box.append(win_height_plus)

        # width entry
        self.win_width_entry.connect(
            "activate",

            lambda entry:
                settings_sync.apply_window_width_from_entry(
                    self.parent,
                    entry
                )
        )

        # height entry
        self.win_height_entry.connect(
            "activate",

            lambda entry:
                settings_sync.apply_window_height_from_entry(
                    self.parent,
                    entry
                )
        )

        # width buttons
        win_width_plus.connect(
            "clicked",

            lambda button:
                settings_sync.increase_window_width(
                    self.parent
                )
        )

        win_width_minus.connect(
            "clicked",

            lambda button:
                settings_sync.decrease_window_width(
                    self.parent
                )
        )

        # height buttons
        win_height_plus.connect(
            "clicked",

            lambda button:
                settings_sync.increase_window_height(
                    self.parent
                )
        )

        win_height_minus.connect(
            "clicked",

            lambda button:
                settings_sync.decrease_window_height(
                    self.parent
                )
        )

        # --------------------------------------------------
        # separator

        main_box.append(sep4)

        # --------------------------------------------------
        # misc section

        misc_label = Gtk.Label(
            label = "Miscellaneous"
        )

        misc_label.set_xalign(0)

        main_box.append(misc_label)

        # --------------------------------------------------
        # misc buttons

        button_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(button_box)

        kb_button = Gtk.Button(
            label = "Keyboard Shortcuts"
        )

        button_box.append(kb_button)

        kb_button.connect(
            "clicked",
            self.open_shortcuts
        )

        config_button = Gtk.Button(
            label = "Open Config File"
        )

        button_box.append(config_button)

        config_button.connect(
            "clicked",
            self.open_config
        )

        github_button = Gtk.Button(
            label = "GitHub"
        )

        button_box.append(github_button)

        github_button.connect(
            "clicked",
            self.open_github
        )

        spreadsheet_button = Gtk.Button(
            label = "⍼"
        )

        button_box.append(spreadsheet_button)

        spreadsheet_button.connect("clicked", self.open_spreadsheet)

        # --------------------------------------------------
        # separator

        main_box.append(sep5)
        main_box.append(sep6)

        # --------------------------------------------------
        # reset/cancel/apply

        rca_box = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 8
        )

        main_box.append(rca_box)

        reset_button = Gtk.Button(
            label = "Restore Defaults"
        )

        reset_button.connect(
            "clicked",
            self.restore_defaults
        )

        rca_box.append(reset_button)

        spacer2 = Gtk.Box()
        spacer2.set_hexpand(True)

        rca_box.append(spacer2)

        close_button = Gtk.Button(
            label = "Close"
        )

        rca_box.append(close_button)



# ----------------------------------------------------------
# end of __init__
# ----------------------------------------------------------

# fn defns

# ----------------------------------------------------------
# keyboard shortcuts

    def open_shortcuts(self, button):

        window = kb_shortcuts(self)

        window.present()

# ----------------------------------------------------------
# spreadsheet

    def open_spreadsheet(self, button):

        window = spreadsheet(self)
        window.present()

# -----------------------------------------------------------
# restore defaults

    def restore_defaults(self, button):

        # reset settings
        self.parent.settings = DEFAULT_SETTINGS.copy()

        save_settings(
            self.parent.settings
        )

        # restart app settings
        settings_sync.apply_font_size(
            self.parent,
            self.parent.settings["font_size"]
        )

        settings_sync.apply_wrap_mode(
            self.parent,
            self.parent.settings["wrap_mode"]
        )

        settings_sync.apply_centered_text(
            self.parent,
            self.parent.settings["centered_text"]
        )

        settings_sync.apply_cursor_type(
            self.parent,
            self.parent.settings["cursor_type"]
        )

        settings_sync.apply_cursor_blink(
            self.parent,
            self.parent.settings["cursor_blink"]
        )

        settings_sync.apply_full_path_in_title(
            self.parent,
            self.parent.settings["show_full_path"]
        )

        settings_sync.apply_window_size(
            self.parent,
            self.parent.settings["win_width"],
            self.parent.settings["win_height"]
        )

        # close settings
        self.close()

# -----------------------------------------------------------
# open config file

    def open_config(self, button):

        config_path = os.path.expanduser(
            "~/.config/compose/settings.json"
        )

        self.parent.file_path = config_path
        self.parent.open_file_path(config_path)

# -----------------------------------------------------------
# github

    def open_github(self, button):

        webbrowser.open(
            "https://github.com/your/repo"
        )

# -----------------------------------------------------------
# about dialog

    def open_about(self, button):

        dialog = Gtk.Window()
        dialog.set_title("About — compose")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_default_size(400, 200)

        # box
        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 12
        )

        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)
        dialog.set_child(box)

        # title
        title = Gtk.Label()
        title.set_markup(
            "<span size='16000'>"
            "<b>compose</b>"
            "</span>"
        )
        box.append(title)


        # version
        version = Gtk.Label(
            label = "v1.0"
        )
        box.append(version)

        # description
        desc = Gtk.Label(
            label = (
                "\nMinimal text editor\n"
                "With temporary utilities\n\n"
                "Keyboard-first\n"
                "GTK-native. If the app looks bad, \n"
                "please check your gtk4/gtk.css\n\n"
                "UI stays out of the way of your text\n"
                "editing.\n\n"
                "Inspired loosely by TextEdit of macOS"
            )
        )
        box.append(desc)

        dialog.present()
