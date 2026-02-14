import os
import sys
import arcade
from game import constants


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(__file__))


class TextureManager:
    def __init__(self):
        self.textures = {}
        self.load_all()

    def load_all(self):
        base_path = get_base_path()
        assets_path = os.path.join(base_path, "game", "assets", "images")

        files = {
            "turret": "tyrel.png",
            "core": "baza.png",
            "projectile": "pyla.png",
            "enemy_basic": "Brad-Pitt.png",
            "enemy_fast": "ninza.png",
            "enemy_tank": "padge.png",
            "coin": "moneta.png"
        }

        for name, filename in files.items():
            filepath = os.path.join(assets_path, filename)

            if os.path.exists(filepath):
                try:
                    self.textures[name] = arcade.load_texture(filepath)
                except:
                    self.textures[name] = self.make_fallback(name)
            else:
                self.textures[name] = self.make_fallback(name)

    def make_fallback(self, name):
        colors = {
            "turret": constants.TURRET_COLOR,
            "core": constants.CORE_COLOR,
            "projectile": constants.PROJECTILE_COLOR,
            "enemy_basic": constants.ENEMY_COLOR,
            "enemy_fast": (255, 150, 50),
            "enemy_tank": (100, 50, 150),
            "coin": (255, 215, 0)
        }

        color = colors.get(name, (255, 255, 255))
        return arcade.SpriteSolidColor(100, 100, color).texture

    def get(self, name):
        return self.textures.get(name, None)


texture_manager = TextureManager()