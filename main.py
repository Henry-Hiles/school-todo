#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, Checkbox
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive

class TodoItem(Horizontal):
    def __init__(self, todo_text: str):
        super().__init__()
        self.todo_text = todo_text
        self.completed = False
        self.label = Static(todo_text, id="label")
        self.checkbox = Button("☐", id="checkbox")

    def compose(self) -> ComposeResult:
        yield self.checkbox
        yield self.label
        yield Button("×", id="delete", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "checkbox":
            self.completed = not self.completed
            self.checkbox.label = "☑" if self.completed else "☐"
            self.checkbox.variant = "success" if self.completed else "default"
            self.label.styles.text_style = "strike" if self.completed else "none"
        elif event.button.id == "delete":
            self.remove()

class TodoApp(App):
    CSS = """
		Horizontal  {
			height: auto;
		}

		#input_row {
			margin: 1;

			& Input {
				width: 1fr;
			}

			& Button  {
				width: 10%;
			}
		}

		#todo_list > Horizontal {
			& #checkbox, #delete {
				height: auto;
				padding: 0;
				margin: 0 1;
				min-width: 1;
				border: none;
			}

			& Static {
				width: 1fr;
				padding-bottom: 1;
			}
		}
    """

    def on_mount(self) -> None:
        self.theme = "nord"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="input_row"):
            yield Input(placeholder="Add a todo...", id="todo_input")
            yield Button("Add", id="add_button", variant="primary")
        yield Vertical(id="todo_list")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_button":
            input_box = self.query_one("#todo_input", Input)
            todo = input_box.value.strip()
            if todo:
                self.query_one("#todo_list", Vertical).mount(TodoItem(todo,))
                input_box.value = ""

TodoApp().run()
