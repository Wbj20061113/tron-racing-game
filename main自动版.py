import pygame
import random
import sys

# --- 初始化设置 ---
pygame.init()

# 屏幕参数
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("霓虹猎手：量子核心 (Trainer AI版)")

# 颜色定义 (R, G, B)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0) # 【新增】用于显示 Trainer 状态的颜色

# 玩家设置
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 100
player_speed = 7

# 障碍物设置
obstacle_width = 60
obstacle_height = 20
obstacle_list = []
obstacle_speed = 5

# 分数与状态
score = 0
clock = pygame.time.Clock()
game_over = False

# ================= 【新增】Trainer 全局状态 =================
is_god_mode = False       # 无敌模式
score_multiplier = 1      # 分数倍率
ai_enabled = True         # AI 自动驾驶开关

# 【关键修复】使用 Pygame 内置默认字体
try:
    font = pygame.font.Font(None, 55)
    small_font = pygame.font.Font(None, 30) # 【新增】小字体，用于提示
except:
    font = pygame.font.SysFont('arial', 55)
    small_font = pygame.font.SysFont('arial', 30)

def draw_player(x, y):
    pygame.draw.rect(screen, NEON_BLUE, (x, y, player_size, player_size))
    # 简单的发光效果
    pygame.draw.rect(screen, (0, 100, 100), (x-2, y-2, player_size+4, player_size+4), 2)

def draw_obstacles(obs_list):
    for obs in obs_list:
        pygame.draw.rect(screen, RED, (obs[0], obs[1], obs[2], obs[3]))

def draw_score(score):
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])

# ================= 【新增】绘制 Trainer 状态提示 =================
def draw_trainer_status():
    status_list = []
    if is_god_mode: status_list.append("GOD MODE [G]")
    if score_multiplier > 1: status_list.append(f"{score_multiplier}X SCORE [M]")
    if not ai_enabled: status_list.append("MANUAL [A]") # 如果关了AI，显示手动模式
    
    if status_list:
        status_text = small_font.render(" | ".join(status_list), True, YELLOW)
        screen.blit(status_text, (10, 40)) # 放在分数下面一点


def game_loop():
    global player_x, player_y, score, obstacle_speed, game_over
    global is_god_mode, score_multiplier, ai_enabled # 【新增】声明要修改的全局变量

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # ================= 【新增】监听键盘切换 Trainer =================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # G键：无敌模式
                    is_god_mode = not is_god_mode
                elif event.key == pygame.K_m:  # M键：5倍分数
                    score_multiplier = 5 if score_multiplier == 1 else 1
                elif event.key == pygame.K_a:  # A键：开启/关闭AI
                    ai_enabled = not ai_enabled

        # --- AI 逻辑 (加入了开关判断) ---
        if ai_enabled:
            closest_obs = None
            min_dist = float('inf')

            for obs in obstacle_list:
                dist = (player_y) - (obs[1] + obs[3])
                if 0 < dist < 300 and abs((obs[0] + obs[2]/2) - (player_x + player_size/2)) < 100:
                    if dist < min_dist:
                        min_dist = dist
                        closest_obs = obs

            if closest_obs:
                target_x = closest_obs[0] + closest_obs[2] / 2
                current_center = player_x + player_size / 2
                if current_center < target_x - 10:
                    player_x += player_speed
                elif current_center > target_x + 10:
                    player_x -= player_speed
        
        # 【新增】如果关闭了AI，允许玩家用方向键手动操作
        if not ai_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_x -= player_speed
            if keys[pygame.K_RIGHT]: player_x += player_speed

        # 边界限制
        if player_x < 0: player_x = 0
        if player_x > WIDTH - player_size: player_x = WIDTH - player_size

        # --- 生成障碍物 ---
        if len(obstacle_list) < 5 and random.randint(0, 20) == 1:
            start_x = random.randrange(0, WIDTH - obstacle_width)
            obstacle_list.append([start_x, -obstacle_height, obstacle_width, obstacle_height])

        # --- 移动障碍物 & 碰撞检测 ---
        for obs in obstacle_list[:]: 
            obs[1] += obstacle_speed 

            # 碰撞检测 (加入了 God Mode 判断)
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])

            if player_rect.colliderect(obs_rect):
                if not is_god_mode:  # 【修改】只有非无敌模式下才会 Game Over
                    game_over = True

            # 移除超出屏幕的障碍物并加分 (加入了 Multiplier 判断)
            if obs[1] > HEIGHT:
                obstacle_list.remove(obs)
                score += 10 * score_multiplier  # 【修改】基础分乘以倍率
                
                if score % 100 == 0: 
                    obstacle_speed += 0.5

        # --- 绘图 ---
        screen.fill(BLACK)
        draw_player(player_x, player_y)
        draw_obstacles(obstacle_list)
        draw_score(score)
        draw_trainer_status()  # 【新增】在画面上显示修改器状态

        pygame.display.update()
        clock.tick(60) # 【建议】把帧率从30改到60，游戏会更丝滑

    # 游戏结束画面
    screen.fill(BLACK)
    msg = font.render("GAME OVER", True, NEON_PINK)
    score_msg = font.render("Score: " + str(score), True, WHITE)
    screen.blit(msg, [WIDTH/2 - msg.get_width()/2, HEIGHT/2 - 50])
    screen.blit(score_msg, [WIDTH/2 - score_msg.get_width()/2, HEIGHT/2 + 20])
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
        pygame.time.wait(100)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
