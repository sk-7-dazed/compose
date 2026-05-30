import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class spreadsheet(Gtk.Window):

    def __init__(self, parent):

        super().__init__()

        self.set_title("Temporary Spreadsheet — compose")
        self.set_transient_for(parent)
        self.set_default_size(900, 600)

        # =====================================
        # scrollable window

        scrollable_window = Gtk.ScrolledWindow()
        scrollable_window.set_hexpand(True)
        scrollable_window.set_vexpand(True)
        self.set_child(scrollable_window)

        # =====================================
        # grid

        grid = Gtk.Grid()
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        grid.set_margin_top(12)
        grid.set_margin_bottom(24)
        grid.set_margin_start(12)
        grid.set_margin_end(24)
        scrollable_window.set_child(grid)

        # =====================================
        # col headers

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for column, letter in enumerate(letters):

            label = Gtk.Label(label=letter)

            grid.attach(
                label,
                column + 1,
                0,
                1,
                1
            )

        # =====================================
        # rows + cells

        for row in range(1, 101):

            # row number label

            row_label = Gtk.Label(
                label=str(row)
            )

            grid.attach(
                row_label,
                0,
                row,
                1,
                1
            )

            # entry cells

            for column in range(26):

                entry = Gtk.Entry()

                entry.set_width_chars(10)

                grid.attach(
                    entry,
                    column + 1,
                    row,
                    1,
                    1
                )
