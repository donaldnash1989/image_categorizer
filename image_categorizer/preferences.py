from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


PREF_PATH = Path(__file__).resolve().parent / "data" / "preferences.json"


@dataclass
class Preferences:
    theme: Literal["light", "system", "dark"] = "system"


def load_preferences() -> Preferences:
    """Load preferences from disk.

    Returns default values when the file does not exist or is invalid.
    """
    try:
        with PREF_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return Preferences(theme=data.get("theme", "system"))
    except FileNotFoundError:
        return Preferences()
    except Exception:
        # If the file is corrupt, fall back to defaults
        return Preferences()


def save_preferences(prefs: Preferences) -> None:
    """Persist the provided preferences to disk."""
    PREF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PREF_PATH.open("w", encoding="utf-8") as fh:
        json.dump({"theme": prefs.theme}, fh)
