# 存放方块的类
import pygame,sys
import random
from pygame.locals import *
from const import *
from utils import *


class Block(pygame.sprite.Sprite):

    # 方块初始化
    def __init__(self,blockType,baseRowIdx,baseColIdx,blockShape,blockRot,blockGroupIdx,width,height,relPos):
        super().__init__()  
        self.blockType = blockType          # 方块的类型
        self.baseRowIdx = baseRowIdx        # 方块的基准行下标
        self.baseColIdx = baseColIdx        # 方块的基准列下标
        self.blockShape = blockShape        # 方块的形状
        self.blockRot = blockRot            # 方块的旋转下标
        self.blockGroupIdx = blockGroupIdx  # 方块在组中的下标
        self.width = width                  # 方块的宽度
        self.height = height                # 方块的高度
        self.relPos = relPos                # 方块的真实位置
        self.blink = False                  # 方块的闪烁状态(用于消除时的闪烁)
        self.blinkCount = 0                 # 方块的闪烁次数(用于消除时的闪烁)
        self.loadImage()                    # 加载方块图片
        self.updateImagePos()               # 更新方块图片的位置

    # 加载方块图片
    def loadImage(self):
        # 确定加载的方块
        self.image = pygame.image.load(BLOCK_RES[self.blockType])
        # 设置方块的大小
        self.image = pygame.transform.smoothscale(self.image, (BLOCK_SIZE_W, BLOCK_SIZE_H))

    # 更新方块图片的位置
    def updateImagePos(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.relPos[0] + self.width * self.colIdx
        self.rect.top = self.relPos[1] + self.height * self.rowIdx

    # 实现下落
    def drop(self):
        # 基准行坐标+1
        self.baseRowIdx += 1

    # 获取每个方块当前的坐标(用于实现碰撞)
    def getIndex(self):
        return (int(self.rowIdx),int(self.colIdx))

    # 获取每个方块下落后的坐标(用于实现碰撞)
    def getNextIndex(self):
        return (int(self.rowIdx + 1),int(self.colIdx))
    
    # 设置左右移动和左右边界判定(用于实现方块组的移动)
    def isLeftBound(self):
        return self.colIdx == 0
    
    def isRightBound(self):
        return self.colIdx == GAME_COL-1

    def doLeft(self):
        self.baseColIdx -= 1

    def doRight(self):
        self.baseColIdx += 1 

    # 定义旋转(用于实现方块组的旋转)
    def doRotate(self):
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockShape]):
            self.blockRot = 0
        self.updateImagePos()

    # 获取相对横纵坐标
    def getBlockConfigIndex(self):
        return BLOCK_SHAPE[self.blockShape][self.blockRot][self.blockGroupIdx]
    
    # 获取绝对横纵坐标
    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockConfigIndex()[0]
    
    @property
    def colIdx(self):
        return self.baseColIdx + self.getBlockConfigIndex()[1]
    
    # 开始闪烁
    def startBlink(self):
            self.blink = True
            self.blinkTime = getCurrentTime()

    # 更新闪烁次数
    def update(self):
        if self.blink:
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime/30) 
           

    # 判断是否在闪烁
    def isBlink(self):
        return self.blink

    # 设置下一个方块组的横纵坐标
    def setBaseIndex(self, baseRowIdx, baseColIdx):
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx

    # 方块渲染
    def draw(self,surface):
        self.updateImagePos()
        # 处于闪烁状态并且闪烁状态奇数不绘制
        # 来实现闪烁效果
        if self.blink and self.blinkCount % 2 == 1:
            return
        surface.blit(self.image, self.rect)    








