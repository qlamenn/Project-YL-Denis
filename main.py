import arcade
from game.views.start_view import StartView


def main():
    window = arcade.Window(
        width=1920,
        height=1080,
        title="Базовая Защита",
        fullscreen=True,
        resizable=False
    )

    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()