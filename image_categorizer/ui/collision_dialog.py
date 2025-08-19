import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from pathlib import Path
from typing import Optional
from ..interfaces.image_loader import IImageLoader

class CollisionDecision:
    def __init__(self, action: str, new_name: Optional[str] = None):
        self.action = action            # 'keep_source' | 'keep_target' | 'rename' | 'cancel'
        self.new_name = new_name

class CollisionDialog(tk.Toplevel):
    def __init__(self, parent, image_loader: IImageLoader, source_path: Path, target_path: Path):
        super().__init__(parent)
        self.title("File Name Collision")
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)
        self.geometry("1000x600")

        self._loader = image_loader
        self._source = source_path
        self._target = target_path
        self._result: CollisionDecision = CollisionDecision("cancel")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        left = ttk.Frame(self); left.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=10)
        right = ttk.Frame(self); right.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
        for f in (left, right):
            f.rowconfigure(0, weight=1); f.columnconfigure(0, weight=1)

        self._canvas_left = tk.Canvas(left, bg="#111111", highlightthickness=1, highlightbackground="#333")
        self._canvas_left.grid(row=0, column=0, sticky="nsew")
        self._canvas_right = tk.Canvas(right, bg="#111111", highlightthickness=1, highlightbackground="#333")
        self._canvas_right.grid(row=0, column=0, sticky="nsew")

        self._lbl_left = ttk.Label(left, text=f"Incoming (root): {self._source.name}")
        self._lbl_left.grid(row=1, column=0, sticky="ew", pady=(6,0))
        self._lbl_right = ttk.Label(right, text=f"Existing (category): {self._target.name}")
        self._lbl_right.grid(row=1, column=0, sticky="ew", pady=(6,0))

        bottom = ttk.Frame(self); bottom.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,10))
        bottom.columnconfigure(1, weight=1)
        ttk.Label(bottom, text="Rename to:").grid(row=0, column=0, sticky="w", padx=(0,6))
        self._entry = ttk.Entry(bottom)
        self._entry.grid(row=0, column=1, sticky="ew")
        self._btn_rename = ttk.Button(bottom, text="Rename", command=self._on_rename, state="disabled")
        self._btn_rename.grid(row=0, column=2, sticky="e", padx=(6,0))
        ttk.Label(bottom, text="(Click an image to choose which to keep)").grid(row=1, column=0, columnspan=3, sticky="w", pady=(6,0))

        self._entry.bind("<KeyRelease>", self._on_entry_change)
        self._canvas_left.bind("<Button-1>", lambda e: self._choose("keep_source"))
        self._canvas_right.bind("<Button-1>", lambda e: self._choose("keep_target"))

        self._img_left = None
        self._img_right = None
        self.bind("<Configure>", lambda e: self._redraw())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_entry_change(self, _):
        text = self._entry.get().strip()
        state = "normal" if text else "disabled"
        self._btn_rename.config(state=state)

    def _on_rename(self):
        name = self._entry.get().strip()
        if not name:
            return
        self._result = CollisionDecision("rename", new_name=name)
        self.destroy()

    def _choose(self, action: str):
        self._result = CollisionDecision(action)
        self.destroy()

    def _on_close(self):
        self._result = CollisionDecision("cancel")
        self.destroy()

    def _redraw(self):
        lw = max(1, self._canvas_left.winfo_width())
        lh = max(1, self._canvas_left.winfo_height())
        rw = max(1, self._canvas_right.winfo_width())
        rh = max(1, self._canvas_right.winfo_height())
        try:
            l_img = self._loader.load_and_fit(self._source, (lw, lh))
            r_img = self._loader.load_and_fit(self._target, (rw, rh))
            self._img_left = ImageTk.PhotoImage(l_img)
            self._img_right = ImageTk.PhotoImage(r_img)
            self._canvas_left.delete("all")
            self._canvas_right.delete("all")
            self._canvas_left.create_image((lw - self._img_left.width())//2, (lh - self._img_left.height())//2, anchor="nw", image=self._img_left)
            self._canvas_right.create_image((rw - self._img_right.width())//2, (rh - self._img_right.height())//2, anchor="nw", image=self._img_right)
        except Exception:
            pass

    @staticmethod
    def prompt(parent, image_loader: IImageLoader, source_path: Path, target_path: Path) -> "CollisionDecision":
        dlg = CollisionDialog(parent, image_loader, source_path, target_path)
        parent.wait_window(dlg)
        return dlg._result
