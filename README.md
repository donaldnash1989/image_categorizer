# Photo Categorizer (Tkinter, SOLID, Modular)

A desktop app to quickly sort photos into category folders. It’s intentionally modular and adheres to SOLID principles.
- **Platform:** Python 3.10+
- **UI:** Tkinter
- **Imaging:** Pillow (PIL)

## Features
- Select a **root directory** on startup.
- Automatically uses **subfolders of the root** as **categories**.
- Creates a **dynamic button** for each category. Clicking a button moves the **currently displayed image** into that category folder.
- **Settings** tab to add or delete categories (deletion blocked if the folder contains files).
- Image display **preserves aspect ratio** and auto-scales on window resize.
- If an image fails to load, all category buttons are **disabled** immediately.

## Install
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```

On launch you'll be prompted to choose a **root directory**. The app will then:
1. Scan the root for subfolders (categories).
2. Create a button for each category.
3. Load the **first image** found directly in the root (sorted by name).

## Notes
- Supported image extensions: `.jpg .jpeg .png .bmp .gif .tiff .webp`
- Deleting a category is only allowed when its folder is empty.
- The app is structured around interfaces and dependency inversion. The `app.py` is the composition root.
