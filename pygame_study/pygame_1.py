import pygame
import sys

# pygame初期化
pygame.init()

# ウィンドウの大きさを設定
size = (700, 500)
screen = pygame.display.set_mode(size)

# ゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 背景色を塗る
    screen.fill((0, 0, 255))

    # 画面を更新
    pygame.display.flip()
