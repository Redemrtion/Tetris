# 框架代码
# 完全不需要去关心实际游戏逻辑
# 以后想做第二个游戏可以直接复用这部分代码
import pygame,sys
from pygame.locals import *
from const import *
from game import *

# 创建游戏
pygame.init()
# 创建画布
DISPLAYSURF = pygame.display.set_mode(size=(GAME_SIZE_W,GAME_SIZE_H))
# 创建游戏类
game = Game(DISPLAYSURF)

# 主循环
# 调用pygame更新函数一直更新
while True:
    # 设置退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # 游戏类状态更新
    game.update()
    # 去除残影
    DISPLAYSURF.fill((0,0,0))
    # 游戏类渲染
    game.draw()
    # 更新
    pygame.display.update()