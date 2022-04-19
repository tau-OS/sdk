from tau.render import render_diff, render_naive
from tau.vdom import to_vdom_constructor
import gi
from deepdiff import DeepDiff

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

Label = to_vdom_constructor(Gtk.Label)
Box = to_vdom_constructor(Gtk.Box)
Button = to_vdom_constructor(Gtk.Button)


# class BaseWidget:
#     pass


# def value():
#     return "value"


# class Widget(BaseWidget):
#     count = value(0)

#     def increment(self):
#         self.count += 1

#     def decrement(self):
#         self.count -= 1

#     def render(self):
#         return Box(
#             Label(label=str(self.count)),
#             Button(label="+", on_clicked=self.increment),
#             Button(label="-", on_clicked=self.decrement),
#         )

a = Label(label="0")

b = Label(label="10")

c = render_diff(render_naive(a), a, b)


print(render_naive(a))
print(render_naive(b))

print(c)

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_child(c)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
