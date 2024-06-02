# 存放常量
class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    CYAN = 5
    PURPLE = 6
    BLOCKMAX = 7

# 添加方块组类型
class BlockGroupType:
    FIXED = 0
    DROP = 1

# 存放不同方块的地址
BLOCK_RES = {
    BlockType.RED : "E:/Python/Study/Game/俄罗斯方块/pic/red.png",
    BlockType.ORANGE : "E:/Python/Study/Game/俄罗斯方块/pic/orange.png",
    BlockType.YELLOW : "E:/Python/Study/Game/俄罗斯方块/pic/yellow.png",
    BlockType.GREEN : "E:/Python/Study/Game/俄罗斯方块/pic/green.png",
    BlockType.BLUE : "E:/Python/Study/Game/俄罗斯方块/pic/blue.png",
    BlockType.CYAN : "E:/Python/Study/Game/俄罗斯方块/pic/cyan.png",
    BlockType.PURPLE : "E:/Python/Study/Game/俄罗斯方块/pic/purple.png"
}

# 定义游戏区域 17行 10列
GAME_ROW = 17
GAME_COL = 10
GAME_SIZE_W = 1200
GAME_SIZE_H = 600

# 定义方块的大小
BLOCK_SIZE_W = 32
BLOCK_SIZE_H = 32

# 存储方块组状态
# 第一维表示形状
# 第三维表示旋转的情况
# 第三维表示局部坐标
BLOCK_SHAPE = [
    [((0,0), (0,1), (1,0), (1,1)), ],      # 方形
    [((0,0), (0,1), (0,2), (0,3)), ((0,0), (1,0), (2,0), (3,0)) ],      # 长条
    [((0,0), (0,1), (1,1), (1,2)), ((0,1), (1,0), (1,1), (2,0)) ],      # z字形
    [((0,1), (1,0), (1,1), (1,2)), ((0,1), (1,1), (1,2), (2,1)), ((1,0), (1,1), (1,2), (2,1)), ((0,1), (1,1), (1,0), (2,1)) ] ,      # 飞机形
]
