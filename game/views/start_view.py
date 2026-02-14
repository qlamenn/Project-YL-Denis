import arcade
from game import constants
from game.game_window import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_color = constants.BACKGROUND_COLOR

    def on_show_view(self):
        arcade.set_background_color(self.bg_color)

    def on_draw(self):
        self.clear()

        w = self.window.width if self.window else constants.SCREEN_WIDTH
        h = self.window.height if self.window else constants.SCREEN_HEIGHT

        arcade.draw_text(
            "ЗАЩИТА БАЗЫ",
            w // 2,
            h // 2 + 150,
            arcade.color.WHITE,
            80,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "Защищай ядро от вражеских волн",
            w // 2,
            h // 2 + 50,
            arcade.color.LIGHT_GRAY,
            36,
            anchor_x="center"
        )

        arcade.draw_text(
            "Управление:",
            w // 2,
            h // 2 - 30,
            arcade.color.WHITE,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "← → - движение турели",
            w // 2,
            h // 2 - 90,
            arcade.color.LIGHT_GRAY,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "ПРОБЕЛ - стрельба",
            w // 2,
            h // 2 - 150,
            arcade.color.LIGHT_GRAY,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC - выход из игры",
            w // 2,
            h // 2 - 210,
            arcade.color.LIGHT_GRAY,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "M - магазин после проигрыша",
            w // 2,
            h // 2 - 270,
            arcade.color.LIGHT_GRAY,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите любую клавишу для начала игры",
            w // 2,
            h // 2 - 350,
            arcade.color.GOLD,
            40,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
            return

        game_view = GameView()
        self.window.show_view(game_view)