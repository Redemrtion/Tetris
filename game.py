# 游戏主逻辑:
# 一个静态的BlockGroup和一个下落的BlockGroup
# 下落的和静态产生碰撞,下落的就合并到静态的里
# 静态的BlockGroup会从下往上判断是否有一整行填充的方块,播放消去动画,直到找不到整行的为止
# 静态的BlockGroup达到一定高度就游戏失败


import pygame,sys
from pygame.locals import *
from const import *
from block import *
from blockGroup import *
import random

class Game(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.surface = surface
        self.fixedBlockGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_SIZE_W,BLOCK_SIZE_H,[], self.getRelPos())       # 创建下落的和固定的方块组的实例
        self.dropBlockGroup = None 
        self.gameoverImage = pygame.image.load("E:/Python/Study/Game/俄罗斯方块/pic/GameOver.bmp")                     # 失败判定
        self.isGameover = False
        self.scoreFont = pygame.font.SysFont(None, 60)                                                                # 积分
        self.score = 0
        self.nextBlockGroup = None                                                                                    # 下一个下落方块组的生成和数据存储
        self.generateNextBlockGroup()
        self.background2 = pygame.image.load("E:/Python/Study/Game/俄罗斯方块/pic/background2.jpeg")                   # 背景的设置
        self.background2 = pygame.transform.scale(self.background2, (808, 600))
        self.background1 = pygame.image.load("E:/Python/Study/Game/俄罗斯方块/pic/background1.jpeg")
        self.background1 = pygame.transform.scale(self.background1, (800, 600))
        self.lines = pygame.image.load("E:/Python/Study/Game/俄罗斯方块/pic/lines.bmp")

    # 根据提前生成的方块组来生成下落方块组
    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0,GAME_COL/2-1)
        self.generateNextBlockGroup()

    # 提前生成的方块组(用于右上角下一个方块提醒)
    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, GAME_COL+2)
        self.nextBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_SIZE_W, BLOCK_SIZE_H, conf, self.getRelPos())

    # 实现碰撞检测
    def willcollid(self):
        # 建立哈希表
        hash = {}
        allIndexs = self.fixedBlockGroup.getBlockIndex()
        # 哈希表存储固定方块组每个方块的位置
        for idx in allIndexs:
            hash[idx] = 1
        # 获取下落方块组下一时刻的位置
        dropIndexs = self.dropBlockGroup.getNextBlockIndex()
        # 前往哈希表查询
        for dropIndex in dropIndexs:
            # 找到返回True,落到底也返回True
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= GAME_ROW:
                return True
        return False

    # 游戏更新
    def update(self):
        # 检测是否重开
        self.restart()
        # 检测游戏是否结束
        if self.isGameover:
            return
        self.checkGameover()
        # 方块组的更新
        self.fixedBlockGroup.update()
        if self.fixedBlockGroup.IsElimiating():
            return
        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()
        #　碰撞相除的更新
        if self.willcollid():
            blocks = self.dropBlockGroup.getBlocks()
            for blk in blocks:
                self.fixedBlockGroup.addBlocks(blk)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            self.fixedBlockGroup.processEliminate()
        # 分数的更新
        self.score = self.fixedBlockGroup.bgScore 

    # 游戏渲染
    def draw(self):
        # 背景的设置及渲染
        self.backgroundRect2 = self.background2.get_rect()
        self.backgroundRect2.centerx = GAME_SIZE_W*0.80
        self.backgroundRect2.centery = GAME_SIZE_H/2
        self.backgroundRect1 = self.background1.get_rect()
        self.backgroundRect1.centerx = GAME_SIZE_W*0.10
        self.backgroundRect1.centery = GAME_SIZE_H/2
        self.surface.blit(self.background2, self.backgroundRect2)
        self.surface.blit(self.background1, self.backgroundRect1)
        self.linesRect = self.lines.get_rect()
        self.linesRect.centerx = GAME_SIZE_W*0.5
        self.linesRect.centery = GAME_SIZE_H/2
        self.surface.blit(self.lines, self.linesRect)
        # 方块组的渲染
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        # 下一个方块组提示的渲染
        self.nextBlockGroup.draw(self.surface)
        # 游戏结束画面的渲染
        if self.isGameover:
            rect = self.gameoverImage.get_rect()
            rect.centerx=GAME_SIZE_W/2
            rect.centery=GAME_SIZE_H/2
            self.surface.blit(self.gameoverImage, rect)
        # 分数的渲染  
        scoreTextImage = self.scoreFont.render('Score:'+str(self.score),True,(0,0,0))
        self.surface.blit(scoreTextImage, (175, 30))

    # 获取绝对位置
    def getRelPos(self):
        return (440,50)
    
    # 检查是否游戏结束
    def checkGameover(self):
        allIndex = self.fixedBlockGroup.getBlockIndex()
        for idx in allIndex:
            if idx[0] < 2:
                self.isGameover = True

    # 检查是否要重开
    def restart(self):
        pressed=pygame.key.get_pressed()
        if pressed[K_SPACE]:
            self.isGameover = False
            self.fixedBlockGroup.clearBlocks()
            self.score = 0
            self.fixedBlockGroup.bgScore = 0