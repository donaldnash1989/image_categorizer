import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ..interfaces.services import ICategoryService
from ..config import AppConfig

class SettingsView(ttk.Frame):
    def __init__(self, parent, category_service: ICategoryService, config: AppConfig, on_changed):
        super().__init__(parent)
        self._svc = category_service
        self._config = config
        self._on_changed = on_changed

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Label(self, text="Categories", font=("TkDefaultFont", 12, "bold"))
        header.grid(row=0, column=0, sticky="w", padx=6, pady=(6,0))

        self._list = tk.Listbox(self, height=10)
        self._list.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

        btns = ttk.Frame(self)
        btns.grid(row=2, column=0, sticky="e", padx=6, pady=(0,6))
        ttk.Button(btns, text="Add", command=self._add).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete", command=self._delete).pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        self._list.delete(0, tk.END)
        for name in self._svc.get_categories():
            self._list.insert(tk.END, name)

    def _add(self):
        name = simpledialog.askstring("Add Category", "New category name:", parent=self)
        if not name:
            return
        self._svc.add_category(name)
        self.refresh()
        self._on_changed()

    def _delete(self):
        sel = self._list.curselection()
        if not sel:
            return
        name = self._list.get(sel[0])
        ok = self._svc.delete_category(name)
        if not ok:
            messagebox.showerror("Cannot Delete", f"Category '{name}' is not empty.")
        self.refresh()
        self._on_changed()
