from scripts.obj import Obj
from scripts.scene import Scene

class GameOver(Scene):
    def __init__(self):
        super().__init__()
        self.bg = Obj("assets/gameOver.png", [self.all_sprites])