import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from settings_mgr import save_settings

# fn defns

# -----------------------------------------------------------
# apply font size

def apply_font_size(app, size):

    # lower bound
    if size < 4:
        size = 4

    # runtime state
    app.font_size = size
    # update settings dict
    app.settings["font_size"] = size
    # update json
    save_settings(app.settings)

    # css
    css = f"""
    textview {{
        font-family: "DM Mono Light";
        font-size: {size}pt;
    }}
    """
    provider = Gtk.CssProvider()
    provider.load_from_data( css.encode() )
    display = app.get_display()
    Gtk.StyleContext.add_provider_for_display(
        display,
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    # sync to gui
    sync_font_size_entry(app)

# -----------------------------------------------------------
# increase font

def increase_font(app):
    apply_font_size(app, app.font_size + 1)

# -----------------------------------------------------------
# decrease font

def decrease_font(app):
    apply_font_size(app, app.font_size - 1)

# syncing gui settings window entry field placeholder text
# -----------------------------------------------------------
# update font size entry

def sync_font_size_entry(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    if not hasattr(app.settings_window, "font_size_entry"):
        return

    app.settings_window.font_size_entry.set_text(str(app.font_size))

# -----------------------------------------------------------
# apply font size from entry

def apply_font_size_from_entry(app, entry):

    text = entry.get_text()
    if not text.isdigit():
        return
    size = int(text)

    if size <= 0:
        return

    apply_font_size(app, size)

# -----------------------------------------------------------
# increase font + sync entry

def increase_font_and_sync(app):
    increase_font(app)
    sync_font_size_entry(app)


# -----------------------------------------------------------
# decrease font + sync entry

def decrease_font_and_sync(app):
    decrease_font(app)
    sync_font_size_entry(app)

# -----------------------------------------------------------
# apply wrap mode

def apply_wrap_mode(app, mode):

    # settings dict
    app.settings["wrap_mode"] = mode
    # save json
    save_settings(app.settings)
    # mode mapping
    wrap_modes = {
        "none":
            Gtk.WrapMode.NONE,
        "word":
            Gtk.WrapMode.WORD,
        "character":
            Gtk.WrapMode.CHAR
    }

    # apply wrap
    app.textview.set_wrap_mode(
        wrap_modes[mode]
    )


# -----------------------------------------------------------
# sync wrap dropdown

def sync_wrap_dropdown(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return

    dropdown = app.settings_window.wrap_dropdown
    mode = app.settings["wrap_mode"]

    mapping = {

        "none": 0,
        "word": 1,
        "character": 2
    }
    dropdown.set_selected(
        mapping[mode]
    )


# -----------------------------------------------------------
# apply wrap from dropdown

def apply_wrap_from_dropdown(app, dropdown):

    index = dropdown.get_selected()
    mapping = {

        0: "none",
        1: "word",
        2: "character"
    }
    mode = mapping[index]
    apply_wrap_mode(
        app,
        mode
    )

# -----------------------------------------------------------
# apply centered text

def apply_centered_text(app, enabled):

    # settings dict
    app.settings["centered_text"] = enabled
    # save json
    save_settings(app.settings)

    # centered
    if enabled:
        left_margin = 300
        right_margin = 300

    # normal
    else:
        left_margin = 40
        right_margin = 40

    # apply margins
    app.textview.set_left_margin(
        left_margin
    )
    app.textview.set_right_margin(
        right_margin
    )


# -----------------------------------------------------------
# sync centered text checkbox

def sync_center_checkbox(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    checkbox = app.settings_window.center_check

    checkbox.set_active(
        app.settings["centered_text"]
    )


# -----------------------------------------------------------
# apply centered text from checkbox

def apply_centered_from_checkbox(app, checkbox):
    enabled = checkbox.get_active()
    apply_centered_text(
        app,
        enabled
    )

# -----------------------------------------------------------
# toggle centered text keybinding

def toggle_centered_text(app):
    enabled = not app.settings["centered_text"]
    apply_centered_text(
        app,
        enabled
    )
    sync_center_checkbox(app)

# -----------------------------------------------------------
# cursor type

# apply cursor type

def apply_cursor_type(app, cursor_type):

    # settings dict
    app.settings["cursor_type"] = cursor_type

    # save json
    save_settings(app.settings)

    # line cursor
    if cursor_type == "line":
        app.textview.set_overwrite(False)
    # block cursor
    elif cursor_type == "block":
        app.textview.set_overwrite(True)

# sync cursor dropdown

def sync_cursor_dropdown(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    dropdown = app.settings_window.cursor_type_dropdown

    mapping = {

        "block": 0,
        "line": 1
    }
    dropdown.set_selected(
        mapping[
            app.settings["cursor_type"]
        ]
    )

# apply cursor from dropdown

def apply_cursor_from_dropdown(app, dropdown):

    index = dropdown.get_selected()
    mapping = {

        0: "block",
        1: "line"
    }
    cursor_type = mapping[index]

    apply_cursor_type(
        app,
        cursor_type
    )

# toggle cursor type

def toggle_cursor_type(app):

    current = app.settings["cursor_type"]

    if current == "line":
        new = "block"
    else:
        new = "line"
    apply_cursor_type(
        app,
        new
    )

    sync_cursor_dropdown(app)


# -----------------------------------------------------------
# cursor blink

def apply_cursor_blink(app, enabled):

    # settings dict
    app.settings["cursor_blink"] = enabled
    # save json
    save_settings(app.settings)
    # gtk settings
    settings = Gtk.Settings.get_default()

    settings.set_property(
        "gtk-cursor-blink",
        enabled
    )


# sync cursor blink checkbox

def sync_cursor_blink_checkbox(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    checkbox = app.settings_window.cursor_blink_check

    checkbox.set_active(
        app.settings["cursor_blink"]
    )

# apply cursor blink from checkbox

def apply_cursor_blink_from_checkbox(
    app,
    checkbox
):

    enabled = checkbox.get_active()

    apply_cursor_blink(
        app,
        enabled
    )


# -----------------------------------------------------------
# full path in title

def apply_full_path_in_title(app, enabled):

    # settings dict
    app.settings["show_full_path"] = enabled
    # save json
    save_settings(app.settings)
    # runtime state
    app.show_full_path = enabled

    # update title
    app.update_title()

# sync full path checkbox

def sync_full_path_checkbox(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    checkbox = app.settings_window.title_path_check
    checkbox.set_active(
        app.settings["show_full_path"]
    )

# apply full path from checkbox

def apply_full_path_from_checkbox(
    app,
    checkbox
):

    enabled = checkbox.get_active()
    apply_full_path_in_title(
        app,
        enabled
    )


# -----------------------------------------------------------
# window size

def apply_window_size(app, width, height):

    # invalid sizes
    if width <= 0 or height <= 0:
        return

    # settings dict
    app.settings["win_width"] = width
    app.settings["win_height"] = height
    # save json
    save_settings(app.settings)

    # apply size
    app.set_default_size(
        width,
        height
    )

# sync window size entries

def sync_window_size_entries(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    window = app.settings_window

    window.win_width_entry.set_text(
        str(app.settings["win_width"])
    )
    window.win_height_entry.set_text(
        str(app.settings["win_height"])
    )

# apply window width from entry

def apply_window_width_from_entry(
    app,
    entry
):

    text = entry.get_text()
    if not text.isdigit():
        return
    width = int(text)

    apply_window_size(
        app,
        width,
        app.settings["win_height"]
    )

# apply window height from entry

def apply_window_height_from_entry(
    app,
    entry
):

    text = entry.get_text()
    if not text.isdigit():
        return
    height = int(text)

    apply_window_size(
        app,
        app.settings["win_width"],
        height
    )

# width buttons

def increase_window_width(app):

    apply_window_size(
        app,
        app.settings["win_width"] + 10,
        app.settings["win_height"]
    )
    sync_window_size_entries(app)

def decrease_window_width(app):

    apply_window_size(
        app,
        app.settings["win_width"] - 10,
        app.settings["win_height"]
    )
    sync_window_size_entries(app)

# height buttons

def increase_window_height(app):

    apply_window_size(
        app,
        app.settings["win_width"],
        app.settings["win_height"] + 10
    )
    sync_window_size_entries(app)

def decrease_window_height(app):

    apply_window_size(
        app,
        app.settings["win_width"],
        app.settings["win_height"] - 10
    )
    sync_window_size_entries(app)

# -----------------------------------------------------------
# apply startup behavior

def apply_startup_behavior(app, behavior):

    app.settings["startup_behavior"] = behavior
    save_settings(app.settings)

# apply startup behavior from dropdown

def apply_startup_from_dropdown(
    app,
    dropdown
):

    index = dropdown.get_selected()
    mapping = {

        0: "empty",
        1: "last_saved",
        2: "restore"
    }
    behavior = mapping[index]

    apply_startup_behavior(
        app,
        behavior
    )

# sync startup dropdown

def sync_startup_dropdown(app):

    if not hasattr(app, "settings_window"):
        return
    if app.settings_window is None:
        return
    dropdown = app.settings_window.startup_open_dropdown
    mapping = {

        "empty": 0,
        "last_saved": 1,
        "restore": 2
    }

    dropdown.set_selected(

        mapping[
            app.settings["startup_behavior"]
        ]
    )

# -----------------------------------------------------------
# save method

def apply_save_method(app, method):

    app.settings["save_method"] = method
    save_settings(app.settings)

# apply save method from dropdown

def apply_save_method_from_dropdown(
    app,
    dropdown
):

    index = dropdown.get_selected()
    mapping = {

        0: "dialog",
        1: "manual"
    }

    apply_save_method(
        app,
        mapping[index]
    )

# -----------------------------------------------------------
# default directory

def apply_default_dir(
    app,
    directory
):

    app.settings["default_dir"] = directory
    save_settings(app.settings)


# -----------------------------------------------------------
# default extension

def apply_default_extension(
    app,
    extension
):

    # remove the dot
    extension = extension.strip()
    extension = extension.replace(".", "")
    app.settings["default_extension"] = extension
    save_settings(app.settings)


# -----------------------------------------------------------
# missing dirs behavior

def apply_missing_dirs(
    app,
    behavior
):

    app.settings["missing_dirs"] = behavior
    save_settings(app.settings)

# -----------------------------------------------------------
# default extension enabled

def apply_default_extension_toggle(
    app,
    enabled
):

    app.settings["default_extension_yn"] = enabled
    save_settings(app.settings)

