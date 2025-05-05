import pygame
import math
import random

# 初始化Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORE_COLOR = (200, 160, 0)
# 新增常量，指定矿泉水瓶数量
BOTTLE_COUNT = 5

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("黄金矿工")
clock = pygame.time.Clock()

# 提前初始化字体，指定字体文件路径
# 修改字体加载方式为绝对路径（需要用户确认实际字体路径）
try:
    # 使用Windows系统自带的中文字体
    font_path = 'C:\\Windows\\Fonts\\simhei.ttf'  # 黑体字体路径
    font = pygame.font.Font(font_path, 36)
except Exception as e:
    print(f"字体加载失败: {e}")
    font = pygame.font.Font(None, 36)

# 钩子类
class Hook:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.length = 150
        self.angle = 0
        # 减慢钩子摇摆速度
        self.speed = 1  # 原速度为 2，现改为 1
        self.is_extending = False
        self.is_retracting = False
        self.caught_ore = None

    def draw(self):
        end_x = self.x + self.length * math.sin(math.radians(self.angle))
        end_y = self.y + self.length * math.cos(math.radians(self.angle))
        pygame.draw.line(screen, BLACK, (self.x, self.y), (end_x, end_y), 5)
        pygame.draw.circle(screen, BLACK, (int(end_x), int(end_y)), 10)
        if self.caught_ore:
            self.caught_ore.x = end_x - self.caught_ore.size // 2
            self.caught_ore.y = end_y - self.caught_ore.size // 2
            self.caught_ore.draw()

    def update(self):
        if not self.is_extending and not self.is_retracting:
            self.angle += self.speed
            if self.angle > 45 or self.angle < -45:
                self.speed = -self.speed
        elif self.is_extending:
            # 增加最大伸展长度
            if self.length < 600:  # 原最大长度为 400，现改为 600
                self.length += 5
            else:
                self.is_extending = False
                self.is_retracting = True
        elif self.is_retracting:
            if self.length > 150:  # 对应修改收回后的长度
                self.length -= 5
            else:
                self.is_retracting = False
                if self.caught_ore:
                    if self.caught_ore in ores:
                        ores.remove(self.caught_ore)
                    self.caught_ore = None

    def check_collision(self, ores):
        end_x = self.x + self.length * math.sin(math.radians(self.angle))
        end_y = self.y + self.length * math.cos(math.radians(self.angle))
        for ore in ores:
            if (end_x > ore.x and end_x < ore.x + ore.size and
                end_y > ore.y and end_y < ore.y + ore.size):
                self.caught_ore = ore
                return True
        return False

# 定义塑料瓶颜色
BOTTLE_COLOR = (100, 200, 255)

# 矿石类（现在代表塑料瓶）
class Ore:
    def __init__(self):
        # 增大矿泉水瓶大小，例如设置为 60
        self.size = 70
        # 修改 x 坐标的随机范围，让塑料瓶更靠近中间
        middle_width = WIDTH // 2
        half_range = 200  # 可以根据需要调整这个值
        self.x = random.randint(middle_width - half_range, middle_width + half_range - self.size)
        self.y = random.randint(200, HEIGHT - 50)
        try:
            # 加载图片
            self.image = pygame.image.load('shui.png')
            # 缩放图片到合适大小
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except pygame.error as e:
            print(f"加载 shui.png 失败: {e}")

    def draw(self):
        # 绘制图片
        if hasattr(self, 'image'):
            screen.blit(self.image, (self.x, self.y))

# 创建钩子对象
hook = Hook()

# 生成矿石列表，使用常量
ores = [Ore() for _ in range(BOTTLE_COUNT)]

# 定义河流颜色
RIVER_COLOR = (0, 100, 255)
# 定义波纹的参数
WAVE_LAYERS = 3  # 增加波纹层数
WAVE_SPEEDS = [1, 1.5, 2]  # 每层波纹的速度
WAVE_HEIGHTS = [10, 15, 20]  # 每层波纹的高度
WAVE_WIDTH = 20
WAVE_COUNT = WIDTH // WAVE_WIDTH

# 初始化每层波纹的偏移量
wave_offsets = [0] * WAVE_LAYERS

# 游戏主循环
running = True
wave_offsets = [0] * WAVE_LAYERS
game_paused = False

# 加载水的 PNG 图片
try:
    water_image = pygame.image.load('water.png')
    # 缩放图片以适应背景
    water_image = pygame.transform.scale(water_image, (WIDTH, HEIGHT - separator_y))
except pygame.error as e:
    print(f"加载 water.png 失败: {e}")

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_paused:
                # 按任意键退出游戏
                running = False
            elif event.key == pygame.K_SPACE and not hook.is_extending and not hook.is_retracting and not game_paused:
                hook.is_extending = True

    if not game_paused:
        screen.fill(WHITE)

        # 绘制分隔线
        separator_y = 100  # 可以根据需要调整分隔线的位置
        pygame.draw.line(screen, BLACK, (0, separator_y), (WIDTH, separator_y), 5)

        # 绘制水的背景图片
        screen.blit(water_image, (0, separator_y))

        # 移除绘制河流背景和波纹的代码
        # pygame.draw.rect(screen, RIVER_COLOR, (0, separator_y, WIDTH, HEIGHT - separator_y))

        # for layer in range(WAVE_LAYERS):
        #     wave_offset = wave_offsets[layer]
        #     wave_height = WAVE_HEIGHTS[layer]
        #     wave_speed = WAVE_SPEEDS[layer]
        #     for i in range(WAVE_COUNT):
        #         wave_x = i * WAVE_WIDTH + wave_offset
        #         wave_y = separator_y + (wave_height * math.sin((wave_x + wave_offset) * 0.03))
        #         wave_rect = pygame.Rect(wave_x, wave_y, WAVE_WIDTH, wave_height)
        #         alpha = int((math.sin((wave_x + wave_offset) * 0.03 + layer * 0.5) + 1) * 64)
        #         wave_surface = pygame.Surface((WAVE_WIDTH, wave_height))
        #         wave_surface.set_alpha(alpha)
        #         wave_surface.fill(RIVER_COLOR)
        #         screen.blit(wave_surface, wave_rect)
        #
        #     # 更新每层波纹的偏移量
        #     wave_offsets[layer] += wave_speed
        #     if wave_offsets[layer] > WAVE_WIDTH:
        #         wave_offsets[layer] = 0

        # 绘制并更新矿石
        for ore in ores:
            if ore not in [hook.caught_ore]:
                ore.draw()

        # 检查碰撞
        if hook.is_extending:
            if hook.check_collision(ores):
                hook.is_extending = False
                hook.is_retracting = True

        hook.update()
        hook.draw()

        # 检查是否所有塑料瓶都已被抓走
        if len(ores) == 0 and hook.caught_ore is None:
            game_paused = True
    else:
        screen.fill(WHITE)
        # 绘制分隔线
        pygame.draw.line(screen, BLACK, (0, separator_y), (WIDTH, separator_y), 5)

        # 绘制水的背景图片
        screen.blit(water_image, (0, separator_y))

        # 最后绘制文字
        if font:
            text = font.render("恭喜你帮助漓江捡走了所有白色污染", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            pygame.display.update()  # 强制刷新显示
        else:
            debug_text = pygame.font.SysFont(None, 36).render("字幕初始化失败", True, (255,0,0))
            screen.blit(debug_text, (WIDTH//2-100, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
