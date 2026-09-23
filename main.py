# Importing PyGObject; lets us access libraries such as GTK
import gi
from datetime import date
import json
import os

# Configures GTK version for PyGObject
gi.require_version("Gtk", "4.0")

# From PyGObject's repository of library bindings, get Gtk module/API
from gi.repository import Gtk, Gdk

from widget_conf import Event, EventWidget, EventFormWidget

# Class representing the main window
class GlassEventsWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)

        self.set_decorated(False)
        self.set_resizable(False)


        self.storage = EventStorage("events.json")
        self.events = self.storage.load_events()

        # Set window title and size
        self.set_title("Glass Events")
        self.set_default_size(400, 430)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        self.box.add_css_class("glass-window")

        # Create a header box and put Upcoming event and add button in it
        header = Gtk.CenterBox()

        title = Gtk.Label(label="Upcoming ")
        title.add_css_class("upcoming-header")


        add_button = Gtk.Button(label="+")
        add_button.connect("clicked", self.build_add_event_form)
        add_button.add_css_class("add-button")

        header.set_start_widget(title)
        header.set_end_widget(add_button)

        self.box.append(header)

        # Box for holding event widgets
        self.events_box = Gtk.ListBox()
        
        self._refresh_events()

        self.events_box.set_sort_func(self.sort_events)

        self.events_box.connect("row-selected", self._on_row_selected)
        self.events_box.connect("row-activated", self._on_row_activated)

        self.events_box.add_css_class("events-list")
        
        # Create a scrollable window to hold the events self.box
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(False)
        scrolled.set_min_content_height(380)
        scrolled.set_max_content_height(380)
        scrolled.set_child(self.events_box)

        scrolled.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )
    

        # Stack allows using multiple views in same space
        self.stack = Gtk.Stack()
        self.stack.add_named(scrolled, "events")


        self.box.append(self.stack)

        # Overlay for gradient effect
        overlay = Gtk.Overlay()
        overlay.set_child(self.box)

        fade = Gtk.Box()
        fade.add_css_class("event-fade")
        fade.set_can_target(False)
        fade.set_halign(Gtk.Align.FILL)
        fade.set_valign(Gtk.Align.END)
        fade.set_vexpand(False)

        overlay.add_overlay(fade)

        self.set_child(overlay)

        self.set_child(overlay)


    def sort_events(self, row1, row2):
        event1 = row1.get_child()
        event2 = row2.get_child()

        if event1.event.date < event2.event.date:
            return -1
        elif event1.event.date > event2.event.date:
            return 1
        return 0

    def add_event(self, event):
        self.events.append(event)
        self._refresh_events()

    def build_add_event_form(self, button):
        if not hasattr(self, "add_event_form"):

            self.add_event_form = EventFormWidget(self)
            self.stack.add_named(self.add_event_form, "form")

        self.stack.set_visible_child_name("form")

    def remove_event(self, event):
        self.events.remove(event)
        self.storage.save_events(self.events)

        row = self.events_box.get_row_at_index(0)
        while row:
            self.events_box.remove(row)
            row = self.events_box.get_row_at_index(0)

        self._refresh_events()

        

    def _refresh_events(self):

        row = self.events_box.get_row_at_index(0)

        while row:
            self.events_box.remove(row)
            row = self.events_box.get_row_at_index(0)

        sorted_events = sorted(self.events, key=lambda event: event.date)

        for index, event in enumerate(sorted_events):
            if index == 0:
                event_widget = EventWidget(event, self, upcoming=True)
            else:
                event_widget = EventWidget(event, self)

            self.events_box.append(event_widget)

    def _on_row_selected(self, list_box, row):
        for index in range(len(self.events)):
            current_row = list_box.get_row_at_index(index)

            if current_row is None:
                continue

            event_widget = current_row.get_child()
            event_widget.delete_button.set_sensitive(current_row is row)
            event_widget.delete_button.set_visible(current_row is row)

    def _on_row_activated(self, list_box, row):
        if list_box.get_selected_row() is row:
            list_box.unselect_row(row)

class EventStorage:

    def __init__(self, filename):
        self.filename = filename

    def load_events(self):
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r") as file:
            data = json.load(file)

        events = []

        for item in data:
            event = Event(
                item["title"],
                date.fromisoformat(item["date"])
            )

            events.append(event)

        return events


    def save_events(self, events):
        data = []

        for event in events:
            data.append({
                "title": event.title,
                "date": event.date.isoformat()
            })

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def delete_event(self, event):
        pass



class Application(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="com.glassevents.App")
    

    def do_activate(self):
        self.load_css()

        window = GlassEventsWindow(self)
        window.present()

    def load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_path("style.css")

        display = Gdk.Display.get_default()

        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )


# Create the application
app = Application()
app.run(None)





