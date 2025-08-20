# Photo Categorizer v2 (Tkinter, SOLID, Modular)

Adds:
- **Collision detection** popup (modal) showing both images, with click-to-keep, and a **Rename** field/button.
- **Red Delete** button with modal confirmation.
- **Remaining count** of images in root (bottom-right), populated on load and after actions.

Run:
```bash
pip install -r requirements.txt
pythonw app.pyw  # use pythonw to avoid opening a console window on Windows
```

## Image resizing quality vs. speed

`PillowImageLoader` uses Pillow's ``BILINEAR`` filter by default which is
considerably faster than ``LANCZOS`` while keeping reasonable quality.
For highest quality at the cost of performance, construct the loader with
``Image.LANCZOS``; for maximum speed use ``Image.NEAREST``. Example:

```python
from PIL import Image
from image_categorizer.infrastructure import PillowImageLoader

img_loader = PillowImageLoader(resample=Image.LANCZOS)
```
