import json
from pathlib import Path

# -------------------------------------------------
# defaults

CONFIG_DIR  = Path.home() / ".config" / "compose"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {

        # font
        "font_face" : "DM Mono",
        "font_size" : 14,

        # appearance
        "wrap_mode" : "word",
        "cursor_type" : "line",
        "cursor_blink" : False,
        "centered_text" : False,
        "show_full_path" : False,

        # save
        "save_method" : "manual",
        "default_dir" : "~/Docuents",
        "default_extension_yn" : True,
        "default_extension" : "txt",
        "missing_dirs" : "error",

        # startup behavior
        "startup_behavior" : "empty",
        "win_width"        : 1440,
        "win_height"       : 810

}

# -------------------------------------------------
# fn defns

# save settings from python dict to json

def save_settings(settings):

    # create config dir if it doesnt exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# -------------------------------------------------
# load settings from json to python dict

def load_settings():

    if not CONFIG_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(CONFIG_FILE, "r") as file:
        settings = json.load(file)

    return settings

# -------------------------------------------------
# reset fn

def reset_settings():
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()

