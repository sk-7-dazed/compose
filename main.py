import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib

# settings stuff
from settings_window import settings_popup
from settings_mgr import load_settings
from spreadsheet import spreadsheet
from kb_shortcuts import kb_shortcuts
import settings_sync

# session restore
import os

class to_be_named_later(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application = app)

        # session restore
        self.session_file = os.path.expanduser("~/.config/compose/session_restore.txt")

# -------------------------------------------------------------
# getting an actual window

        # window title and window size
        self.set_title("Something must be broken")
        # self.set_default_size(1440, 810) - moved to settings_sync.py

        # making the window a text editor
        self.textview = Gtk.TextView()

# ------------------------------------------------------------
# making it pretty

        # word wrap
        # self.textview.set_wrap_mode(Gtk.WrapMode.WORD) - moved to settings_sync.py

        # margins
        # self.textview.set_left_margin(40) - moved to settings_sync.py
        # self.textview.set_right_margin(40) - moved to settings_sync.py
        self.textview.set_top_margin(30)

# -----------------------------------------------------------
# making it a text editor

        # initializing text buffer
        self.buffer = self.textview.get_buffer()
        self.buffer.connect("changed", self.on_text_changed)

# ----------------------------------------------------------
# making it usable with scrolling

        # making the window scrollable
        scrollable_window = Gtk.ScrolledWindow()
        scrollable_window.set_child(self.textview)

        self.set_child(scrollable_window)

# ----------------------------------------------------------
# font size stuff (ctrl +/-)

        self.font_size = 14

        increase_action = Gio.SimpleAction.new("increase_font", None)
        increase_action.connect("activate", lambda action, param: settings_sync.increase_font(self) )
        self.add_action(increase_action)

        decrease_action = Gio.SimpleAction.new("decrease_font", None)
        decrease_action.connect("activate", lambda action, param: settings_sync.decrease_font(self) )
        self.add_action(decrease_action)

        # self.apply_font() - moved to settings_sync.py

# ----------------------------------------------------------
# save and save as

        # action for save on ctrl+s
        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.save_actual)      # connecting action to actual save function
                                                               # meaning *activate* this action when the fn is called
        self.add_action(save_action)
        
        self.file_path = None
        self.is_modified = False
        self.last_saved_text = ""
        self.show_full_path = False

# -----------------------------------------------------------
# open file

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.open_fn)             # connecting action to actual open fn
                                                                  # meaning *activate* this action when fn is called
        self.add_action(open_action)

# -----------------------------------------------------------
# settings window
        
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.open_settings)
        self.add_action(settings_action)

# -----------------------------------------------------------
# setting window title

        self.update_title()

# -----------------------------------------------------------
# centered text keybinding ctrl space


        center_action = Gio.SimpleAction.new(
            "centered_text",
            None
        )

        center_action.connect(
            "activate",
            lambda action, param:
                settings_sync.toggle_centered_text(
                    self
                )
        )

        self.add_action(center_action)

# -----------------------------------------------------------
# loading settings
        
        self.settings = load_settings()

        # restore previous session
        if self.settings["startup_behavior"] != "empty":
            if os.path.exists(self.session_file):
                with open(self.session_file, "r") as f:
                    text = f.read()
                self.buffer.set_text(text)
                self.is_modified = True
                self.update_title()

        # window size
        settings_sync.apply_window_size(self, self.settings["win_width"], self.settings["win_height"])

        # font size
        settings_sync.apply_font_size(self, self.settings["font_size"])

        # wrap mode
        settings_sync.apply_wrap_mode(self, self.settings["wrap_mode"])

        # centered text
        settings_sync.apply_centered_text(self, self.settings["centered_text"])

        # cursor type
        settings_sync.apply_cursor_type(self, self.settings["cursor_type"])

        # cursor blink
        settings_sync.apply_cursor_blink(self, self.settings["cursor_blink"])

        # path in title bar
        settings_sync.apply_full_path_in_title(self, self.settings["show_full_path"])


# ------------------------------------------------------------
# actions
# ------------------------------------------------------------


# ------------------------------------------------------------
    # shortcut key for opening kb shortcuts window

        shortcuts_action = Gio.SimpleAction.new("shortcuts", None)

        shortcuts_action.connect("activate", self.open_shortcuts)

        self.add_action(shortcuts_action)

    # shortcut key for opening temp spreadsheet

        spreadsheet_action = Gio.SimpleAction.new("temp_spreadsheet", None)

        spreadsheet_action.connect("activate", self.open_spreadsheet)

        self.add_action(spreadsheet_action)

# -----------------------------------------------------------
# ins = change cursor type 

        # cursor type action

        cursor_action = Gio.SimpleAction.new(
            "cursor_type",
            None
        )

        cursor_action.connect(
            "activate",

            lambda action, param:
                settings_sync.toggle_cursor_type(
                    self
                )
        )

        self.add_action(cursor_action)

# session restore saving

        self.connect("close-request", self.on_close)

# delete to start of line

        delete_start_action = Gio.SimpleAction.new(
            "delete_to_line_start",
            None
        )

        delete_start_action.connect(
            "activate",

            lambda action, param:
                self.delete_to_line_start()
        )

        self.add_action(
            delete_start_action
        )



        # delete to end of line

        delete_end_action = Gio.SimpleAction.new(
            "delete_to_line_end",
            None
        )

        delete_end_action.connect(
            "activate",

            lambda action, param:
                self.delete_to_line_end()
        )

        self.add_action(
            delete_end_action
        )

# ------------------------------------------------------------
# end of actions
# ------------------------------------------------------------


# ----------------------------------------------------------
# end of __init__
# ----------------------------------------------------------

# ----------------------------------------------------------
# fn defns

# -----------------------------------------------------------
# save and save as

    # what actually happens when you save with ctrl+s
    def save_actual(self, action, param):
        if self.file_path is None:
            if self.settings["save_method"] == "dialog":
                self.save_as()         # if path doesnt exist, save as
            else:
                self.manual_save_dialog()
            self.is_modified = False
            self.last_saved_text = False
            self.update_title()
        else:
            self.save_to_file()    # if path already exists, save to current file instead of save as
            self.is_modified = False
            self.last_saved_text = False
            self.update_title()


    # save as dialog and stuff
    def save_as(self):
        save_as_dialog = Gtk.FileDialog()
        save_as_dialog.set_title("Save File")
        save_as_dialog.save(self, None, self.save_as_fn)

    # -----------------------------------------------------------
    # manual save dialog

    def manual_save_dialog(self):

        dialog = Gtk.Window()
        dialog.set_title("Save Path")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_default_size(500, 60)

        # box
        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 12
        )
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        dialog.set_child(box)

        # entry
        entry = Gtk.Entry()
        default_dir = self.settings["default_dir"]
        extension = self.settings["default_extension"]
        entry.set_text(
            f"{default_dir}/untitled.{extension}"
        )
        box.append(entry)

        # enter to save
        entry.connect(
            "activate",
            lambda entry:
                self.manual_save_confirm(
                    dialog,
                    entry
                )
        )

        dialog.present()

    # -----------------------------------------------------------
    # manual save confirm
    # -----------------------------------------------------------

    def manual_save_confirm(
        self,
        dialog,
        entry
    ):

        import os
        path = entry.get_text().strip()
        path = os.path.expanduser(path)

        # auto extension
        extension = self.settings["default_extension"]
        filename = os.path.basename(path)
        if "." not in filename:
            path += f".{extension}"

        # directory
        directory = os.path.dirname(path)

        # missing dir
        if not os.path.exists(directory):
            behavior = self.settings[
                "missing_dirs"
            ]

            # auto create
            if behavior == "create":
                os.makedirs(
                    directory,
                    exist_ok = True
                )
            # error
            else:
                error = Gtk.AlertDialog()
                error.set_message(
                    "Directory does not exist."
                )
                error.show(self)
                return

        # save
        self.file_path = path
        self.save_to_file()
        self.is_modified = False
        self.update_title()
        dialog.destroy()


    # what actually happens when you do save as
    def save_as_fn(self, save_as_dialog, result):
        try:
            file = save_as_dialog.save_finish(result)
            if file is None:
                return

            # get path
            # path = file.get_path()

            # # .txt auto extension added if user doesnt specify extension while saving
            # import os
            # dirname = os.path.dirname(path)
            # filename = os.path.basename(path)
            # # if "." not in filename:  - moved to next fn
            # #     filename += ".txt"
            # path = os.path.join(dirname, filename)

            # self.file_path = path

            self.file_path = file.get_path()
            self.save_to_file()

        except GLib.Error as e:
            print("Save cancelled or failed:", e)

    # save to *some* file fn
    def save_to_file(self):
        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        text = self.buffer.get_text(start, end, True)   # getting text from start to end of buffer

        # auto extension
        if self.settings["default_extension_yn"]:
            extension = self.settings["default_extension"]
            filename = os.path.basename(self.file_path)
            if "." not in filename:
                self.file_path += f".{extension}"

        with open(self.file_path, "w") as f:
            f.write(text)                               # write that text to file
            self.last_saved_text = text

        print(f"Saved to {self.file_path}")

# -----------------------------------------------------------
# font size increase and decrease - moved to settings_sync.py

    # def apply_font(self):
    #     css = f"""
    #     textview {{ 
    #         font-family: "DM Mono Light";
    #         font-size: {self.font_size}pt;
    #     }}
    #     """

    #     provider = Gtk.CssProvider()
    #     provider.load_from_data(css.encode())

    #     display = self.get_display()
    #     Gtk.StyleContext.add_provider_for_display(display, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    # def increase_font(self, action, param):
    #     self.font_size += 1
    #     self.apply_font()

    # def decrease_font(self, action, param):
    #     if self.font_size > 4:
    #         self.font_size -= 1
    #         self.apply_font()

# -----------------------------------------------------------
# open file

    # open dialog box
    def open_fn(self, action, param):
        open_dialog = Gtk.FileDialog()
        open_dialog.set_title("Open File")
        open_dialog.open(self, None, self.open_actual)

    # what actually happens when you open a file
    def open_actual(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is None:
                return

            path = file.get_path()
            self.file_path = path            # get path

            self.open_file_path(path)

        except Exception as e:
            print("Open failed: ", e)

# -----------------------------------------------------------
# open specific file path

    def open_file_path(
        self,
        path
    ):

        with open(path, "r") as f:
            text = f.read()

        self.buffer.set_text(text)
        self.file_path = path
        self.last_saved_text = text
        self.is_modified = False
        self.update_title()

# open settings window
    def open_settings(self, action, param):
        
        # actually opening it
        if not hasattr(self, "settings_window") or self.settings_window is None:
            self.settings_window = settings_popup(self)
            settings_sync.sync_wrap_dropdown(self)

            # when closed
            self.settings_window.connect("close-request", self.hide_settings)

        self.settings_window.present()

# close settings window
    def hide_settings(self, window):
        window.set_visible(False)
        return True

# if unsaved changes, show star in title bar
    def on_text_changed(self, buffer):

        text = buffer.get_text(
            buffer.get_start_iter(),
            buffer.get_end_iter(),
            True
        )

        self.is_modified = (
            text != self.last_saved_text
        )

        self.update_title()

# fn to update title bar dynamically
    def update_title(self):
        
        # if file is empty
        if self.file_path is None and not self.is_modified:
            title = "Empty — compose"

        # unsaved file
        elif self.file_path is None and self.is_modified:
            title = "Untitled ⁕ — compose"

        # if saved
        else:

            # getting file name
            import os
            if self.show_full_path:
                name = self.file_path
            else:
                name = os.path.basename(self.file_path)

            # unsaved changes
            if self.is_modified:
                title = f"{name} ⁕ — compose"
            # saved
            else:
                title = f"{name} — compose"

        self.set_title(title)

# shortcut keys for opening shortcut key window and opening spreadsheet

    # open keyboard shortcuts window

    def open_shortcuts(self, action, param):

        window = kb_shortcuts(self)

        window.present()



    # open scratch grid

    def open_spreadsheet(self, action, param):

        window = spreadsheet(self)

        window.present()

# -----------------------------------------------------------
# save session restore

    def save_session_restore(self):

        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        text = self.buffer.get_text(
            start,
            end,
            True
        )

        # empty buffer
        if text.strip() == "":
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            return

        # save session contents
        with open(self.session_file, "w") as f:
            f.write(text)

# -----------------------------------------------------------
# unsaved changes on close

    def on_close(self, window):

        # if nothing modified
        if not self.is_modified:
            return False

        # dialog
        dialog = Gtk.AlertDialog()

        dialog.set_message(
            "Save changes before closing?"
        )

        dialog.set_detail(
            "Your unsaved changes will be restored next time."
        )

        dialog.set_buttons([
            "Cancel",
            "Discard",
            "Save"
        ])

        dialog.set_cancel_button(0)
        dialog.set_default_button(2)

        dialog.choose(
            self,
            None,
            self.close_dialog_response
        )

        return True

# -----------------------------------------------------------
# close dialog button response

    def close_dialog_response(
        self,
        dialog,
        result
    ):

        response = dialog.choose_finish(result)

        # cancel
        if response == 0:
            return

        # discard
        elif response == 1:
            self.save_session_restore()
            self.destroy()

        # save
        elif response == 2:
            self.save_actual(None, None)
            self.destroy()

# -----------------------------------------------------------
# delete to beginning of line
# -----------------------------------------------------------

    def delete_to_line_start(self):

        insert_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )

        start_iter = insert_iter.copy()

        start_iter.set_line_offset(0)

        self.buffer.delete(
            start_iter,
            insert_iter
        )



    # -----------------------------------------------------------
    # delete to end of line
    # -----------------------------------------------------------

    def delete_to_line_end(self):

        insert_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )

        end_iter = insert_iter.copy()

        end_iter.forward_to_line_end()

        self.buffer.delete(
            insert_iter,
            end_iter
        )


# -------------------------------------------------------------
# end of "to_be_named_later"
# -------------------------------------------------------------

class the_actual_app(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # keybindings

        # keybinding for save ctrl+s
        self.set_accels_for_action("win.save", ["<Ctrl>s"])

        # keybinding for open ctrl+o
        self.set_accels_for_action("win.open", ["<Ctrl>o"])

        # keybindings for font size ctrl +/-
        self.set_accels_for_action("win.increase_font", ["<Ctrl>plus", "<Ctrl>equal"])
        self.set_accels_for_action("win.decrease_font", ["<Ctrl>minus"])

        # keybinding for opening settings window ctrl+,
        self.set_accels_for_action("win.settings", ["<Ctrl>comma"])

        # keybinding for toggle centered text ctrl+space
        self.set_accels_for_action("win.centered_text", ["<Ctrl>space"])

        # keybinding for opening shortcuts window ctrl+shift+?
        self.set_accels_for_action("win.shortcuts", ["<Ctrl>question"])

        # keybinding for opening temp spreadsheet ctrl+t
        self.set_accels_for_action("win.temp_spreadsheet", ["<Ctrl><Shift>t"])

        # keybinding for toggle cursor type insert
        self.set_accels_for_action("win.cursor_type", ["Insert"])

        # del to start/end of line alt+backspace/del
        # delete to start of line
        self.set_accels_for_action(
            "win.delete_to_line_start",
            ["<Alt>BackSpace"]
        )

        # delete to end of line
        self.set_accels_for_action(
            "win.delete_to_line_end",
            ["<Alt>Delete"]
        )


    def do_activate(self):

        # disp window
        win = to_be_named_later(self)
        win.present()
        self.add_window(win)


app = the_actual_app(application_id="com.example.compose")
app.run(None)
