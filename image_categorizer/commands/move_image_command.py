from dataclasses import dataclass
from ..interfaces.services import IImageService

@dataclass
class MoveImageCommand:
    image_service: IImageService
    category: str
    def execute(self):
        self.image_service.move_current_to_category(self.category)
