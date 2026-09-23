# Importing PyGObject; lets us access libraries such as GTK
import gi
from datetime import date

# Configures GTK version for PyGObject
gi.require_version("Gtk", "4.0")

# From PyGObject's repository of library bindings, get Gtk module/API
from gi.repository import Gtk


# Class for event data
class Event:

    def __init__(self, title, date):
        self.title = title
        self.date = date


# Class for creating a box for event data

class EventWidget(Gtk.Box):

    def __init__(self, event, window, upcoming=False):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )

        self.window = window
        self.event = event
        self.upcoming = upcoming

        if self.upcoming:
            self.add_css_class("upcoming-card")
        else:
            self.add_css_class("normal-event")

        if not self.upcoming:
            timeline = TimelineWidget()

        # Setting up date labels and their container

        day_label = Gtk.Label(
            label=event.date.strftime("%d")
        )

        month_label = Gtk.Label(
            label=event.date.strftime("%b").upper()
        )

        year_label = Gtk.Label(
            label=event.date.strftime("%Y")
        )

        date_box  = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )

        date_box.append(day_label)
        date_box.append(month_label)
        date_box.append(year_label)

        day_label.set_halign(Gtk.Align.START)
        month_label.set_halign(Gtk.Align.START)
        year_label.set_halign(Gtk.Align.START)


        # Event Name Info setup

        title_label = Gtk.Label(label=event.title)
        title_label.set_halign(Gtk.Align.START)

        # CSS classes setup
        day_label.add_css_class("event-day")
        month_label.add_css_class("event-month")
        year_label.add_css_class("event-year")
        title_label.add_css_class("event-title")

        if self.upcoming:
            day_label.add_css_class("upcoming")
            month_label.add_css_class("upcoming")
            year_label.add_css_class("upcoming")
            title_label.add_css_class("upcoming")


        info_box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing=2
        )

        if not self.upcoming:
            info_box.add_css_class("normal-event-info")

        info_box.append(title_label)
        info_box.set_hexpand(True)
        

        self.delete_button = Gtk.Button(label="Delete")
        self.delete_button.set_sensitive(False)
        self.delete_button.set_visible(False)
        self.delete_button.add_css_class("event-delete")
        self.delete_button.connect("clicked", self.on_delete_clicked)

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.VERTICAL
        )
        separator.add_css_class("event-divider")
        if not self.upcoming:
            separator.add_css_class("normal-event-divider")

        date_box.set_valign(Gtk.Align.CENTER)
        info_box.set_valign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.FILL)

        if not self.upcoming:
            self.append(timeline)
            
        self.append(date_box)
        self.append(separator)
        self.append(info_box)
        self.append(self.delete_button)

    def on_delete_clicked(self, button):
        self.window.remove_event(self.event)





class EventFormWidget(Gtk.Box):

    def __init__(self, window):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4
        )

        self.window = window
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Event title")
        self.append(self.title_entry)

        self.date_calendar = Gtk.Calendar()
        self.append(self.date_calendar)

        self.add_button = Gtk.Button(label="Add")
        self.cancel_button = Gtk.Button(label="Cancel")

        self.add_button.connect("clicked", self.on_add_clicked)
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        self.append(self.add_button)
        self.append(self.cancel_button)


    def _validate(self):
        title = self.title_entry.get_text()
        if not title:
            return False
        return True

    def get_event_data(self):
        title = self.title_entry.get_text()
        calendar_date = self.date_calendar.get_date()
        event_date = date(
            calendar_date.get_year(),
            calendar_date.get_month(),
            calendar_date.get_day_of_month()
        )

        return Event(title, event_date)

    def _clear_form(self):
        self.title_entry.set_text("")

    def on_add_clicked(self, button):
        if self._validate():
            event = self.get_event_data()
            self.window.add_event(event)
            self.window.storage.save_events(self.window.events)
            self._clear_form()
            self.window.stack.set_visible_child_name("events")

    def on_cancel_clicked(self, button):
        self.window.stack.set_visible_child_name("events")



class TimelineWidget(Gtk.Box):

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )

        self.add_css_class("timeline")

        self.set_vexpand(True)

        overlay = Gtk.Overlay()

        line = Gtk.Box()
        line.add_css_class("timeline-line")
        line.set_halign(Gtk.Align.CENTER)
        line.set_valign(Gtk.Align.FILL)

        dot = Gtk.Label(label="●")

        dot.set_halign(Gtk.Align.CENTER)
        dot.set_valign(Gtk.Align.START)

        overlay.set_child(line)
        overlay.add_overlay(dot)

        self.append(overlay)