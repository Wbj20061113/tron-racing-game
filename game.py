import pygame, sys, random, copy
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# 窗口基础

W, H = 800, 600
PANEL_W = 380  # 右侧仪表盘宽度
SCREEN_W = W + PANEL_W
screen = pygame.display.set_mode((SCREEN_W, H))
pygame.display.set_caption("AI极速光轮｜遗传进化训练")
clock = pygame.time.Clock()

# 配色

BG = (5,8,22)
PLAYER_COL = (0,215,255)
TRAIL_COL = (0,125,190)
AI_COL = (255,75,195)
PANEL_BG = (20,25,40)
TEXT_COL = (230,230,230)

size = 8
speed = 5
gen = 1          # 当前世代
max_score = 0    # 历史最高分
score_list = []  # 分数折线数据
game_speed = 1   # 变速倍率

# AI个体类

class BikeAI:
    def __init__(self):
        self.x = random.randint(100,W-100)
        self.y = random.randint(100,H-100)
        self.dx = speed if random.random()>0.5 else -speed
        self.dy = 0
        self.trail = []
        self.alive = True
        self.score = 0

# 初始化种群

pop_num = 6
ai_pop = [BikeAI() for _ in range(pop_num)]

# 玩家

px,py = W//2, H//2
pdx,pdy = speed,0
p_trail = []
game_over = False

def reset_world():
    global px,py,pdx,pdy,p_trail,game_over
    px,py = W//2,H//2
    pdx,pdy = speed,0
    p_trail.clear()
    game_over = False
    for ai in ai_pop:
        ai.x = random.randint(80,W-80)
        ai.y = random.randint(80,H-80)
        ai.dx = speed if random.random()>0.5 else -speed
        ai.dy = 0
        ai.trail.clear()
        ai.alive = True

# 进化：优胜劣汰+变异

def evolution():
    global gen,max_score
    gen += 1
    # 选存活最优个体
    best = max(ai_pop, key=lambda x:x.score)
    max_score = max(max_score, best.score)
    score_list.append(best.score)
    # 繁衍变异
    new_pop = []
    for _ in range(pop_num):
        new_bike = copy.deepcopy(best)
        # 随机变异方向
        if random.random()<0.25:
            new_bike.dx = speed if random.random()>0.5 else -speed
            new_bike.dy = 0
        new_bike.trail.clear()
        new_bike.alive = True
        new_bike.score = 0
        new_pop.append(new_bike)
    ai_pop[:] = new_pop

# 生成分数折线图

def make_plot():
    plt.style.use('dark_background')
    fig,ax = plt.subplots(figsize=(3.6,2.2),dpi=100)
    ax.plot(score_list, c="#00d8ff", linewidth=2)
    ax.set_title("历代最高分走势", c="white", fontsize=9)
    ax.set_xlabel("世代",c="white",fontsize=8)
    ax.set_ylabel("分数",c="white",fontsize=8)
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

plot_surf = make_plot()

while True:
    # 事件
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if e.key == pygame.K_EQUALS: # +加速
                game_speed = min(game_speed+1,20)
            if e.key == pygame.K_MINUS: # -减速
                game_speed = max(game_speed-1,1)
            if e.key == pygame.K_SPACE:
                reset_world()

# 多倍速循环
for _ in range(game_speed):
    # 玩家操控
    k = pygame.key.get_pressed()
    if k[pygame.K_UP] and pdy != speed:
        pdx,pdy = 0,-speed
    if k[pygame.K_DOWN] and pdy != -speed:
        pdx,pdy = 0,speed
    if k[pygame.K_LEFT] and pdx != speed:
        pdx,pdy = -speed,0
    if k[pygame.K_RIGHT] and pdx != -speed:
        pdx,pdy = speed,0
    p_trail.append((px,py))
    px += pdx
    py += pdy
    # 玩家碰撞
    if px<0 or px>W-size or py<0 or py>H-size or (px,py) in p_trail[:-6]:
        reset_world()

    # AI逻辑
    all_dead = True
    for ai in ai_pop:
        if not ai.alive:continue
        all_dead = False
        ai.trail.append((ai.x,ai.y))
        ai.x += ai.dx
        ai.y += ai.dy
        ai.score += 1
        # 碰壁转向
        if ai.x<=0 or ai.x>=W-size: ai.dx = -ai.dx
        if ai.y<=0 or ai.y>=H-size: ai.dy = -ai.dy
        # 撞轨迹淘汰
        if (ai.x,ai.y) in p_trail or (ai.x,ai.y) in ai.trail[:-5]:
            ai.alive = False
    # 全部AI阵亡→进化下一代
    if all_dead:
        evolution()
        plot_surf = make_plot()
        reset_world()

# 绘制画面
screen.fill(BG)
# 游戏区
for x,y in p_trail:
    pygame.draw.rect(screen,TRAIL_COL,(x,y,size,size))
for ai in ai_pop:
    for x,y in ai.trail:
        pygame.draw.rect(screen,AI_COL,(x,y,size,size))
pygame.draw.rect(screen,PLAYER_COL,(px,py,size,size))
for ai in ai_pop:
    if ai.alive:
        pygame.draw.rect(screen,AI_COL,(ai.x,ai.y,size,size))

# 右侧仪表盘
pygame.draw.rect(screen,PANEL_BG,(W,0,PANEL_W,H))
font = pygame.font.SysFont("simhei",22)
info = [
    f"当前世代：{gen}",
    f"运行倍速：{game_speed}x [+/-调速]",
    f"历史最高分：{max_score}",
    f"存活AI数量：{sum(1 for i in ai_pop if i.alive)}",
    "ESC退出 | 空格重置"
]
for idx,txt in enumerate(info):
    s = font.render(txt,True,TEXT_COL)
    screen.blit(s,(W+15,20+idx*32))
# 粘贴折线图
screen.blit(plot_surf,(W+12,220))

pygame.display.flip()
clock.tick(60)
