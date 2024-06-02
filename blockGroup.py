# 存放方块组的类
import random
import pygame, sys
from const import *
from block import *
from pygame.locals import *
from utils import *


class BlockGroup(object):

    # 方块组初始化
    def __init__(self, blockGroupType,width, height, blockConfigList, relPos):
        super().__init__()
        self.blocks = []                        # 存储方块组内各方块的数据
        self.blockGroupType = blockGroupType    # 方块组的类别
        self.pressTime={}                       # 方块组
        self.dropInterval = 300                 # 方块下落的时间间隔
        self.isElimiating = False               # 判断是否需要消除
        self.time = 0                           # 时间(作为时间判断下落)
        self.eliminateTime = None               # 消除时的时间
        self.eliminateRow = None                # 消除的行
        self.bgScore = 0                        # 分数
        # 循环构建方块组的方块
        for config in blockConfigList:
            blk = Block(config['blockType'],config['rowIdx'],config['colIdx'],config['blockShape'],config['blockRot'],config['blockGroupIdx'],width,height,relPos)
            self.blocks.append(blk)
    
    # 生成构建方块组的配置
    def GenerateBlockGroupConfig(rowIdx, colIdx):
        shapeIdx = random.randint(0, len(BLOCK_SHAPE)-1)
        bType = random.randint(0, BlockType.BLOCKMAX-1)
        configList = []
        rotIdx = 0
        # 每个方块的配置
        for idx in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType' : bType,
                'blockShape' : shapeIdx,
                'blockGroupIdx' : idx,
                'rowIdx' : rowIdx,
                'colIdx' : colIdx,
                'blockRot' : rotIdx
            }
            configList.append(config)
        return configList

    # 方块组的更新
    def update(self):
        oldTime = self.time
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        # 实现下落方块组
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.time = curTime
                for b in self.blocks:
                    b.drop()
            self.keyDownHandler()
        # 实现方块更新(主要是闪烁)
        for blk in self.blocks:
            blk.update()
        # 实现消除效果
        if self.IsElimiating():
            while True:
                if getCurrentTime() - self.eliminateTime > 500:
                    # 存储消除行以外的方块
                    tmpBlocks = []
                    for blk in self.blocks:
                        # 消除行以外的方块
                        if blk.getIndex()[0] != self.eliminateRow:
                            # 消除行以上的方块
                            if blk.getIndex()[0] < self.eliminateRow:
                                blk.drop()
                            tmpBlocks.append(blk)
                    # 更新消除后全部方块的数据并加分
                    self.blocks = tmpBlocks
                    self.bgScore += 1
                # 防止同时消除，只记录了其中一个消除行
                for blk in self.blocks:
                    if blk.isBlink():
                        self.eliminateRow = blk.getIndex()[0]
                        break
                # 确保都消除了，脱离循环
                if not self.isExistBlink():    
                    self.setEliminate(False)
                    break

    # 方块组渲染
    def draw(self,surface):
        for b in self.blocks:
            b.draw(surface)

    #　获取该时刻和下一时刻的方块组内所有方块的坐标(用于判断是否碰撞)
    def getBlockIndex(self):
        return [block.getIndex()    for block in self.blocks]
    
    def getNextBlockIndex(self):
        return [block.getNextIndex()    for block in self.blocks]
    
    # 一些增删改的函数以备不时之需
    def getBlocks(self):
        return self.blocks
    
    def clearBlocks(self):
        self.blocks=[]

    def addBlocks(self, blk):
        self.blocks.append(blk)

    # 实现左右移动，加速下落和转向
    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            # 用于判断是否移动
            b = True
            for blk in self.blocks:
                if blk.isLeftBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doLeft()           
        if pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            # 用于判断是否移动
            b = True
            for blk in self.blocks:
                if blk.isRightBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doRight()       
        # 用于加速下落
        if pressed[K_DOWN]:
            self.dropInterval = 50
        else:
            self.dropInterval = 800
        # 用于转向
        if pressed[K_UP] and self.checkAndSetPressTime(K_UP):
            for blk in self.blocks:   
                blk.doRotate()

    # 检测上次按下的时间
    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
        self.pressTime[key] = getCurrentTime()
        return ret  

    # 消除
    def doEliminate(self, row):
        eliminateRow = {}
        # 将第row行的所有方块传入哈希表
        for col in range(0,GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1
        
        for blk in self.blocks:
            if eliminateRow.get(blk.getIndex()):
                blk.startBlink()

    # 检测是否需要消除
    def processEliminate(self):
        hash={}
        allIndexes = self.getBlockIndex()
        for idx in allIndexes:
            hash[idx] = 1
        # 从下往上判断每一行
        for row in range(GAME_ROW-1,-1,-1):
            full = True
            for col in range(0,GAME_COL):
                # 获得这个位置的坐标
                idx = (row, col)
                # 满了，说明这一行的每一列都能在哈希表找到
                # 没满，说明哈希表会有缺少，一旦没找到就说明没满
                if not hash.get(idx):
                    full = False
                    break
            # 找完一行检测一次
            # 有满的就消除，没满就继续检测
            if full:
                self.doEliminate(row)
                self.setEliminate(True)
                self.eliminateRow = row
                self.eliminateTime = getCurrentTime()

    # 为了便利设置的函数
    def setEliminate(self, el):
        self.isElimiating = el

    def IsElimiating(self):
        return self.isElimiating
    
    def isExistBlink(self):
        for blk in self.blocks:
            if blk.isBlink():
                return True
        return False
    
    # 确定下一个方块组的各个方块的坐标
    def setBaseIndexes(self, baseRow, baseCol):
        for blk in self.blocks:
            blk.setBaseIndex(baseRow,baseCol)