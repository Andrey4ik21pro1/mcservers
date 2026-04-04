from textual.app import App
from textual.widgets import DataTable, Input, Label, Footer, Header
from textual.binding import Binding
from textual.containers import Horizontal

COLUMNS = [
    ("Name", "string"),
    ("IP Address", "string"),
    ("Icon", "icon"),
    ("Textures", "tristate"),
]

TEXTURE_STATES = [None, 1, 0]
TEXTURE_LABELS = {None: "?", 1: "✓", 0: "✗"}

class Editor(App):

    BINDINGS = [
        Binding("a", "add_row", "Add row"),
        Binding("d", "delete_row", "Del row"),
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, nbt):
        super().__init__()
        self.nbt = nbt
        self.data = [row[:] for row in nbt.rows]
        self._initial_data = [row[:] for row in nbt.rows]
        self.editing = False

    @property
    def is_changed(self):
        return self.data != self._initial_data

    @staticmethod
    def fmt(value, col_type):
        if col_type == "tristate":
            return TEXTURE_LABELS[value]
        if col_type == "icon":
            return "View"
        return str(value)

    def compose(self):
        yield Header()
        table = DataTable()
        table.cursor_type = "cell"
        table.zebra_stripes = True
        table.styles.padding = (0, 2)
        yield table
        with Horizontal(id="statusbar"):
            yield Label("", id="status-label")
            yield Input(id="edit-input")
        yield Footer()

    def on_mount(self):
        self.table = self.query_one(DataTable)
        self.query_one("#statusbar").display = False
        self._fill_table()

    def _fill_table(self):
        if not self.table.columns:
            self.table.add_column("#", width=2)
            for name, _ in COLUMNS:
                self.table.add_column(name)

        self.table.clear()
        for i, row in enumerate(self.data):
            rendered = [self.fmt(v, COLUMNS[j][1]) for j, v in enumerate(row)]
            self.table.add_row(str(i + 1), *rendered, key=str(i))

    def on_data_table_cell_selected(self, event):
        r, c = event.coordinate.row, event.coordinate.column - 1
        if c < 0: return

        col_type = COLUMNS[c][1]
        val = self.data[r][c]

        if col_type == "tristate":
            self.data[r][c] = TEXTURE_STATES[(TEXTURE_STATES.index(val) + 1) % 3]
            self.table.update_cell_at(event.coordinate, TEXTURE_LABELS[self.data[r][c]])

        else:
            self.editing = True
            self._edit_coord = (r, c)

            self.table.disabled = True
            label_text = f" {COLUMNS[c][0]}: "

            self.query_one("#status-label").update(label_text)
            self.query_one("#edit-input").value = str(val or "")
            self.query_one("#statusbar").display = True
            self.query_one("#edit-input").focus()

    def on_input_submitted(self, event):
        r, c = self._edit_coord
        val = event.value.strip()

        self.data[r][c] = val

        col_type = COLUMNS[c][1]
        display_value = self.fmt(val, col_type)

        self.table.update_cell_at((r, c + 1), display_value)
        self._close_edit()

    def _close_edit(self):
        self.editing = False
        self.query_one("#statusbar").display = False

        self.table.disabled = False
        self.table.focus()

    def action_add_row(self):
        if self.editing: return
        new_row = []
        for _, col_type in COLUMNS:
            if col_type == "tristate":
                new_row.append(None)
            else:
                new_row.append("")

        self.data.append(new_row)

        idx = len(self.data)
        rendered = [self.fmt(v, COLUMNS[j][1]) for j, v in enumerate(new_row)]
        self.table.add_row(str(idx), *rendered, key=str(idx-1))

        self.table.move_cursor(row=idx - 1)

    def action_delete_row(self):
        if self.editing: return
        row_idx = self.table.cursor_row
        if self.data and row_idx >= 0:
            row_key = list(self.table.rows.keys())[row_idx]
            del self.data[row_idx]

            self.table.remove_row(row_key)

            for i in range(row_idx, len(self.data)):
                self.table.update_cell_at((i, 0), str(i + 1))

            if self.data:
                new_idx = min(row_idx, len(self.data) - 1)
                self.table.move_cursor(row=new_idx)

    def action_cancel(self):
        if self.editing:
            self._close_edit()

    def action_quit(self):
        if self.is_changed:
            self.nbt.save(self.data)
        self.exit()