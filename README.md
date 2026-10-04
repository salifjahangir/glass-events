# Glass Events

A lightweight GTK4 desktop widget for managing and displaying upcoming events.

Glass Events is a Python-based desktop event manager designed for Ubuntu GNOME. It provides a glass-style interface for viewing, adding, and deleting events, with persistent storage through a JSON file.

## Features

- GTK4-based graphical interface
- Displays upcoming events in chronological order
- Prominent card for the next upcoming event
- Timeline-style layout for subsequent events
- Scrollable event list
- Add events using a calendar interface
- Delete selected events
- Event data stored persistently in `events.json`
- Glass/translucent visual design
- Custom CSS styling
- Bungee font throughout the interface
- Fade effect at the bottom of the event list
- Automatic startup through GNOME autostart
- XWayland support for desktop-style window behavior

## Current Desktop Behavior

Glass Events normally runs as a GTK4 application under Wayland.

For desktop-widget behavior, it can also be launched through XWayland:

```bash
GDK_BACKEND=x11 python3 main.py
