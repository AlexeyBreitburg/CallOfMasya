import period
import period.core.public as pub
from PIL import Image
from time import time
from random import randint, choice


def hero(x, y, state):
    period.draw.bitmap(xy=(x, y), bitmap=pub.hero_picture, fill=True)


def create_enemy():
    while True:
        position = [128, randint(12, 50), 0]
        if [position[0], position[1]] not in [[item[0], item[1]] for item in pub.enemies]:
            break
    pub.enemies.append(position)


@period.on_start
def on_load():
    pub.health = 3
    pub.score = 0

    # Главный герой и его начальные координаты
    pub.hero_picture = Image.open('maska.png')
    pub.hero_x = 2
    pub.hero_y = 24
    pub.hero_speed = 1
    
    # Пули
    pub.bullets = []
    pub.bullet_speed = 3
    pub.shoot_interval = 0.8
    pub.shoot_time = time()

    # Враги
    pub.enemy_sprites = [
        Image.open('mouse1.png'),
        Image.open('mouse2.png')
    ]
    pub.enemies = []
    pub.enemy_speed = 0.4


@period.on_tick
def on_frame():
    period.draw.icon(xy=(113, 3), icon=period.core.font.icons[
        'battery-full' if pub.health == 3 else 'battery-half' if pub.health == 2 else 'battery-quarter' if pub.health == 1 else 'battery-empty'
    ], size=8, fill=True)
    period.draw.text(xy=(3, 1), text=f'Score: {pub.score}', fill=True)

    # Перемещение главного героя
    buttons = period.button.get_pressed()
    hero_speed = pub.hero_speed

    if period.button.center in buttons:
        hero_speed *= 1.5
    if period.button.up in buttons and pub.hero_y > 12:
        pub.hero_y -= hero_speed
    if period.button.down in buttons and pub.hero_y < 48:
        pub.hero_y += hero_speed
    if period.button.left in buttons and pub.hero_x > 0:
        pub.hero_x -= hero_speed
    if period.button.right in buttons and pub.hero_x < 32:
        pub.hero_x += hero_speed

    # Рисуем главного героя
    hero(pub.hero_x, pub.hero_y, 'alive')

    # Стрельба
    if period.button.first in buttons and pub.shoot_time < time():
        pub.bullets.append([pub.hero_x + 15, pub.hero_y + 5])
        pub.shoot_time = time() + pub.shoot_interval

    for item in pub.bullets:
        pub.bullets[pub.bullets.index(item)][0] += pub.bullet_speed
        if item[0] > 128:
            pub.bullets.remove(item)
            continue
        period.draw.line(xy=(item[0], item[1], item[0] + 3, item[1]), fill=True)

    # Враги
    if len(pub.enemies) == 0: create_enemy()
    for enemy in pub.enemies.copy():
        if enemy[0] < -8:
            pub.health -= 1
            if pub.health <= 0:
                period.graphics.alert(text='Вы проиграли!')
                period.util.delay(5)

                pub.enemies.clear()
                pub.bullets.clear()

                pub.health = 3
                pub.score = 0
                pub.hero_x = 2
                pub.hero_y = 24
                break

            pub.enemies.remove(enemy)
            continue

        pub.enemies[pub.enemies.index(enemy)][2] = 0 if enemy[2] == 1 else 1
        pub.enemies[pub.enemies.index(enemy)][0] -= pub.enemy_speed

        period.draw.bitmap(xy=[enemy[0], enemy[1]], bitmap=pub.enemy_sprites[enemy[2]], fill=True)

        for bullet in pub.bullets.copy():
            if bullet[0] >= enemy[0] and bullet[1] in range(enemy[1], enemy[1] + 9):
                pub.bullets.remove(bullet)
                pub.enemies.remove(enemy)
                pub.score += 1

                if pub.enemy_speed < 1.5: pub.enemy_speed += 0.005
                if pub.shoot_interval > 0.2: pub.shoot_interval -= 0.005
                if choice([True, False, False]):
                    for _ in range(randint(2, 3)):
                        create_enemy()
                break

if __name__ == '__main__':
    period.run_app()
