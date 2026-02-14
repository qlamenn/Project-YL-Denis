import arcade
import random
from game import constants
from game.texture_manager import texture_manager
from game.data_manager import data_manager


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.turret = None
        self.core = None
        self.core_collider = None
        self.enemies = None
        self.bullets = None
        self.money_list = None

        self.money = 0
        self.dead = False
        self.shop_open = False
        self.current_coins = 0

        self.physics = None
        self.left_down = False
        self.right_down = False
        self.shoot_down = False

        self.shoot_timer = 0
        self.spawn_timer = 0
        self.bonus_timer = 0
        self.bonus_on = False
        self.bonus_time = 10

        self.level = 1
        self.enemies_goal = 5
        self.enemies_made = 0

        self.core_sprites = None
        self.turret_sprites = None

    def setup(self):
        self.enemies = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.money_list = arcade.SpriteList()
        self.core_sprites = arcade.SpriteList()
        self.turret_sprites = arcade.SpriteList()

        core_tex = texture_manager.get("core")
        self.core = arcade.Sprite()
        self.core.texture = core_tex
        self.core.scale = constants.SCALE_CORE
        self.core.center_x = constants.SCREEN_WIDTH // 2
        self.core.center_y = constants.SCREEN_HEIGHT // 2
        self.core_hp = constants.CORE_HEALTH
        self.core_sprites.append(self.core)

        self.core_collider = arcade.Sprite()
        self.core_collider.texture = core_tex
        self.core_collider.scale = constants.SCALE_CORE
        self.core_collider.center_x = constants.SCREEN_WIDTH // 2
        self.core_collider.center_y = constants.SCREEN_HEIGHT // 2

        turret_tex = texture_manager.get("turret")
        self.turret = arcade.Sprite()
        self.turret.texture = turret_tex
        self.turret.scale = constants.SCALE_TURRET
        self.turret.center_x = constants.SCREEN_WIDTH // 2
        self.turret.center_y = 200
        self.turret_sprites.append(self.turret)

        self.physics = arcade.PhysicsEngineSimple(
            self.turret,
            arcade.SpriteList()
        )

        self.money = 0
        self.current_coins = 0
        self.dead = False
        self.shop_open = False
        self.bonus_on = False
        self.bonus_timer = 0
        self.shoot_timer = 0
        self.spawn_timer = 0
        self.level = 1
        self.enemies_goal = 5
        self.enemies_made = 0

        constants.ENEMY_SPEED_MULTIPLIER = 1.0

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(constants.BACKGROUND_COLOR)

        self.core_sprites.draw()
        self.turret_sprites.draw()
        self.enemies.draw()
        self.bullets.draw()
        self.money_list.draw()

        self.draw_gui()

        if self.dead:
            self.draw_gameover()
            if self.shop_open:
                self.draw_shop()

        if self.bonus_on:
            self.draw_bonus_msg()

    def draw_gui(self):
        bar_w = 400
        bar_h = 30
        bar_x = 50
        bar_y = constants.SCREEN_HEIGHT - 80

        arcade.draw_lrbt_rectangle_filled(
            bar_x,
            bar_x + bar_w,
            bar_y - bar_h / 2,
            bar_y + bar_h / 2,
            constants.HEALTH_BAR_BACKGROUND
        )

        cur_w = (self.core_hp / constants.CORE_HEALTH) * bar_w
        if cur_w > 0:
            arcade.draw_lrbt_rectangle_filled(
                bar_x,
                bar_x + cur_w,
                bar_y - bar_h / 2,
                bar_y + bar_h / 2,
                constants.HEALTH_BAR_COLOR
            )

        arcade.draw_text(
            f"Монетки: {self.money}",
            50, constants.SCREEN_HEIGHT - 140,
            constants.UI_COLOR, 36
        )

        arcade.draw_text(
            f"Здоровье: {self.core_hp}/{constants.CORE_HEALTH}",
            50, constants.SCREEN_HEIGHT - 190,
            constants.UI_COLOR, 28
        )

        wave_text = f"Волна: {self.level}"
        if self.bonus_on:
            wave_text += " (БОНУС!)"

        arcade.draw_text(
            wave_text,
            constants.SCREEN_WIDTH - 300, constants.SCREEN_HEIGHT - 140,
            constants.UI_COLOR, 36
        )

        if self.bonus_on:
            time_left = max(0, self.bonus_time - self.bonus_timer)
            arcade.draw_text(
                f"Осталось: {time_left:.1f} сек",
                constants.SCREEN_WIDTH - 300, constants.SCREEN_HEIGHT - 190,
                (255, 255, 0), 28
            )
        else:
            arcade.draw_text(
                f"Врагов: {len(self.enemies)}/{self.enemies_goal}",
                constants.SCREEN_WIDTH - 300, constants.SCREEN_HEIGHT - 190,
                constants.UI_COLOR, 28
            )

        control_text = "← → движение, ПРОБЕЛ огонь"
        if self.dead:
            control_text += ", M магазин, ESC выход"
        else:
            control_text += ", ESC выход"

        arcade.draw_text(
            control_text,
            50, 60,
            constants.UI_COLOR, 28
        )

    def draw_bonus_msg(self):
        arcade.draw_lrbt_rectangle_filled(
            constants.SCREEN_WIDTH // 2 - 300,
            constants.SCREEN_WIDTH // 2 + 300,
            constants.SCREEN_HEIGHT - 100,
            constants.SCREEN_HEIGHT - 50,
            (0, 100, 0, 200)
        )

        arcade.draw_text(
            "БОНУСНЫЙ РАУНД! Собирай монетки!",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT - 75,
            (255, 255, 0), 40,
            anchor_x="center"
        )

    def draw_gameover(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            constants.SCREEN_WIDTH,
            0,
            constants.SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "ИГРА ОКОНЧЕНА",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 + 150,
            (255, 50, 50), 120,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Монеток: {self.money}",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 + 50,
            constants.UI_COLOR, 80,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Всего монет: {data_manager.get_total_coins()}",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 - 50,
            (255, 215, 0), 60,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Волна: {self.level}",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 - 120,
            constants.UI_COLOR, 60,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Рекорд: {data_manager.get_high_score()}",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 - 190,
            (255, 100, 100), 50,
            anchor_x="center"
        )

        arcade.draw_text(
            "R рестарт, M магазин, ESC выход",
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2 - 280,
            constants.UI_COLOR, 50,
            anchor_x="center"
        )

    def draw_shop(self):
        w = 600
        h = 400
        x = constants.SCREEN_WIDTH // 2
        y = constants.SCREEN_HEIGHT // 2

        arcade.draw_lrbt_rectangle_filled(
            x - w // 2,
            x + w // 2,
            y - h // 2,
            y + h // 2,
            (30, 30, 50, 250)
        )

        arcade.draw_lrbt_rectangle_outline(
            x - w // 2,
            x + w // 2,
            y - h // 2,
            y + h // 2,
            (255, 215, 0), 5
        )

        arcade.draw_text(
            "МАГАЗИН",
            x,
            y + 150,
            (255, 215, 0), 60,
            anchor_x="center"
        )

        arcade.draw_text(
            "Скоро откроемся!",
            x,
            y,
            constants.UI_COLOR, 40,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC закрыть",
            x,
            y - 150,
            constants.UI_COLOR, 30,
            anchor_x="center"
        )

    def save_game_data(self):
        data_manager.add_coins(self.current_coins)
        data_manager.update_high_score(self.money)

    def on_update(self, delta):
        if self.dead:
            return

        if self.physics:
            self.physics.update()

        if self.left_down:
            self.turret.center_x -= constants.TURRET_SPEED
        if self.right_down:
            self.turret.center_x += constants.TURRET_SPEED

        edge = 150
        if self.turret.center_x < edge:
            self.turret.center_x = edge
        if self.turret.center_x > constants.SCREEN_WIDTH - edge:
            self.turret.center_x = constants.SCREEN_WIDTH - edge

        self.shoot_timer += delta
        self.spawn_timer += delta

        if self.bonus_on:
            self.bonus_timer += delta

            if self.spawn_timer > 0.5:
                self.spawn_coin()
                self.spawn_timer = 0

            if self.bonus_timer >= self.bonus_time:
                self.end_bonus()
        else:
            if self.spawn_timer > constants.SPAWN_INTERVAL and self.enemies_made < self.enemies_goal:
                self.spawn_enemy()
                self.spawn_timer = 0

            if len(self.enemies) == 0 and self.enemies_made >= self.enemies_goal:
                self.next_level()

        if self.shoot_down and self.shoot_timer > 0.3:
            self.shoot()
            self.shoot_timer = 0

        for bullet in self.bullets:
            bullet.center_y += constants.PROJECTILE_SPEED

            if bullet.bottom > constants.SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        for enemy in self.enemies:
            dx = self.core.center_x - enemy.center_x
            dy = self.core.center_y - enemy.center_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > 0:
                enemy.center_x += (dx / dist) * enemy.speed
                enemy.center_y += (dy / dist) * enemy.speed

            if arcade.check_for_collision(enemy, self.core_collider):
                self.core_hp -= enemy.damage
                enemy.remove_from_sprite_lists()

                if self.core_hp <= 0:
                    self.dead = True
                    self.save_game_data()

        for coin in self.money_list:
            dx = self.core.center_x - coin.center_x
            dy = self.core.center_y - coin.center_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > 0:
                coin.center_x += (dx / dist) * 3.0
                coin.center_y += (dy / dist) * 3.0

            if arcade.check_for_collision(coin, self.core_collider):
                coin.remove_from_sprite_lists()

            hit = arcade.check_for_collision_with_list(coin, self.bullets)
            if hit:
                coin.remove_from_sprite_lists()
                for bullet in hit:
                    bullet.remove_from_sprite_lists()
                    self.money += 10
                    self.current_coins += 10

        for bullet in self.bullets:
            hit = arcade.check_for_collision_with_list(bullet, self.enemies)

            if hit:
                bullet.remove_from_sprite_lists()
                for enemy in hit:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.remove_from_sprite_lists()
                        self.money += enemy.points
                        self.current_coins += enemy.points

    def shoot(self):
        tex = texture_manager.get("projectile")
        bullet = arcade.Sprite()
        bullet.texture = tex
        bullet.scale = constants.SCALE_PROJECTILE
        bullet.center_x = self.turret.center_x
        bullet.center_y = self.turret.center_y + 100
        self.bullets.append(bullet)

    def spawn_enemy(self):
        if self.enemies_made >= self.enemies_goal:
            return

        r = random.randint(1, 10)

        if r <= 6:
            enemy = self.make_basic()
        elif r <= 9:
            enemy = self.make_fast()
        else:
            enemy = self.make_tank()

        side = random.randint(1, 3)
        if side == 1:
            enemy.center_x = random.randint(-200, 0)
            enemy.center_y = random.randint(constants.SCREEN_HEIGHT // 2, constants.SCREEN_HEIGHT + 200)
        elif side == 2:
            enemy.center_x = random.randint(constants.SCREEN_WIDTH, constants.SCREEN_WIDTH + 200)
            enemy.center_y = random.randint(constants.SCREEN_HEIGHT // 2, constants.SCREEN_HEIGHT + 200)
        else:
            enemy.center_x = random.randint(200, constants.SCREEN_WIDTH - 200)
            enemy.center_y = constants.SCREEN_HEIGHT + 200

        self.enemies.append(enemy)
        self.enemies_made += 1

    def spawn_coin(self):
        tex = texture_manager.get("coin")
        if not tex:
            tex = arcade.SpriteSolidColor(30, 30, (255, 215, 0)).texture

        coin = arcade.Sprite()
        coin.texture = tex
        coin.scale = 0.15

        side = random.randint(1, 4)
        if side == 1:
            coin.center_x = random.randint(-100, 0)
            coin.center_y = random.randint(0, constants.SCREEN_HEIGHT)
        elif side == 2:
            coin.center_x = random.randint(constants.SCREEN_WIDTH, constants.SCREEN_WIDTH + 100)
            coin.center_y = random.randint(0, constants.SCREEN_HEIGHT)
        elif side == 3:
            coin.center_x = random.randint(0, constants.SCREEN_WIDTH)
            coin.center_y = random.randint(constants.SCREEN_HEIGHT, constants.SCREEN_HEIGHT + 100)
        else:
            coin.center_x = random.randint(0, constants.SCREEN_WIDTH)
            coin.center_y = random.randint(-100, 0)

        self.money_list.append(coin)

    def make_basic(self):
        tex = texture_manager.get("enemy_basic")
        enemy = arcade.Sprite()
        enemy.texture = tex
        enemy.scale = constants.SCALE_ENEMY_BASIC

        mult = getattr(constants, 'ENEMY_SPEED_MULTIPLIER', 1.0)
        enemy.speed = constants.ENEMY_SPEED * 1.3 * mult

        enemy.health = 1
        enemy.damage = 10
        enemy.points = 10
        enemy.type = "basic"
        return enemy

    def make_fast(self):
        tex = texture_manager.get("enemy_fast")
        enemy = arcade.Sprite()
        enemy.texture = tex
        enemy.scale = constants.SCALE_ENEMY_FAST

        mult = getattr(constants, 'ENEMY_SPEED_MULTIPLIER', 1.0)
        enemy.speed = constants.ENEMY_SPEED * 1.7 * mult

        enemy.health = 1
        enemy.damage = 5
        enemy.points = 15
        enemy.type = "fast"
        return enemy

    def make_tank(self):
        tex = texture_manager.get("enemy_tank")
        enemy = arcade.Sprite()
        enemy.texture = tex
        enemy.scale = constants.SCALE_ENEMY_TANK

        mult = getattr(constants, 'ENEMY_SPEED_MULTIPLIER', 1.0)
        enemy.speed = constants.ENEMY_SPEED * 0.65 * mult

        enemy.health = 5
        enemy.damage = 20
        enemy.points = 50
        enemy.type = "tank"
        return enemy

    def next_level(self):
        self.level += 1
        self.enemies_goal = 5 + self.level * 3
        self.enemies_made = 0

        constants.ENEMY_SPEED_MULTIPLIER += constants.ENEMY_SPEED_INCREASE

        if self.level % 4 == 0:
            self.start_bonus()

    def start_bonus(self):
        self.bonus_on = True
        self.bonus_timer = 0
        self.money_list = arcade.SpriteList()

    def end_bonus(self):
        self.bonus_on = False
        self.money_list = arcade.SpriteList()

    def on_key_press(self, key, mod):
        if key == arcade.key.ESCAPE:
            if self.dead and self.shop_open:
                self.shop_open = False
            else:
                arcade.exit()
            return

        if self.dead and key == arcade.key.M:
            self.shop_open = True
            return

        if self.dead and key == arcade.key.R:
            self.setup()
            return

        if key == arcade.key.LEFT:
            self.left_down = True
        elif key == arcade.key.RIGHT:
            self.right_down = True
        elif key == arcade.key.SPACE:
            self.shoot_down = True

    def on_key_release(self, key, mod):
        if key == arcade.key.LEFT:
            self.left_down = False
        elif key == arcade.key.RIGHT:
            self.right_down = False
        elif key == arcade.key.SPACE:
            self.shoot_down = False