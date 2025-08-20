from __future__ import annotations

"""Theme support for the Tkinter user interface.

This module centralizes color definitions for light and dark themes and
provides a helper to apply those colors using ``ttk.Style``.  Other modules can
query the currently active colors via :func:`get_color`.
"""

from tkinter import ttk

# Color definitions ---------------------------------------------------------

LIGHT_THEME: dict[str, str] = {
    "background": "#f0f0f0",
    "foreground": "#000000",
    "button_background": "#e0e0e0",
    "button_foreground": "#000000",
    "danger_background": "#cc0000",
    "danger_active_background": "#990000",
    "danger_foreground": "#ffffff",
    "canvas_background": "#ffffff",
}

DARK_THEME: dict[str, str] = {
    "background": "#2b2b2b",
    "foreground": "#ffffff",
    "button_background": "#444444",
    "button_foreground": "#ffffff",
    "danger_background": "#cc0000",
    "danger_active_background": "#990000",
    "danger_foreground": "#ffffff",
    "canvas_background": "#333333",
}

# Keep track of the current theme colours.  Default to dark.
_current_theme: dict[str, str] = DARK_THEME


def set_theme(name: str) -> None:
    """Select the active theme by ``name`` (``"dark"`` or ``"light"``)."""
    global _current_theme
    _current_theme = DARK_THEME if name == "dark" else LIGHT_THEME


def get_color(key: str) -> str:
    """Return the colour associated with ``key`` in the current theme."""
    return _current_theme[key]


def apply_theme(root, name: str | None = None) -> None:
    """Apply the current theme to ``root`` using :class:`ttk.Style`.

    If ``name`` is provided the theme is first switched to that value before
    applying.
    """
    if name:
        set_theme(name)

    c = _current_theme
    style = ttk.Style(root)

    # Base colours
    root.configure(bg=c["background"])
    style.configure("TFrame", background=c["background"])
    style.configure("TLabel", background=c["background"], foreground=c["foreground"])

    # Buttons
    style.configure(
        "TButton",
        background=c["button_background"],
        foreground=c["button_foreground"],
    )
    style.map("TButton", background=[("active", c["button_background"])])

    # A special style for destructive actions
    style.configure(
        "Danger.TButton",
        background=c["danger_background"],
        foreground=c["danger_foreground"],
    )
    style.map("Danger.TButton", background=[("active", c["danger_active_background"])])

    # Notebook
    style.configure("TNotebook", background=c["background"])
    style.configure(
        "TNotebook.Tab",
        background=c["button_background"],
        foreground=c["foreground"],
    )
    style.map("TNotebook.Tab", background=[("selected", c["background"])])

    # Scrollbar
    style.configure(
        "TScrollbar",
        background=c["button_background"],
        troughcolor=c["background"],
    )
