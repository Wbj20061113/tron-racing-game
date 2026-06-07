import pygame
import random
import sys
from trainer import Trainer  # 导入我们写的修改器模块

# --- 初始化设置 ---
pygame.init()

# 屏幕参数
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("霓虹猎手：量子核心 (v2.0 Modular)")

# 颜色定义
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0) # 用于显示Trainer状态

# 字体设置
try:
    font_large = pygame.font.Font(None, 55)
    font_small = pygame.font.Font(None, 30)
except:
    font_large = pygame.font.SysFont('arial', 55)
    font_small = pygame.font.SysFont('arial', 30)

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

# 游戏全局变量
score = 0
clock = pygame.time.Clock()
game_over = False

# 【实例化修改器】
my_trainer = Trainer()

def draw_player(x, y, is_god):
    color = YELLOW if is_god else NEON_BLUE # 无敌时变黄
    pygame.draw.rect(screen, color, (x, y, player_size, player_size))
    # 发光效果
    border_color = (200, 200, 0) if is_god else (0, 100, 100)
    pygame.draw.rect(screen, border_color, (x-2, y-2, player_size+4, player_size+4), 2)

def draw_obstacles(obs_list):
    for obs in obs_list:
        pygame.draw.rect(screen, RED, (obs[0], obs[1], obs[2], obs[3]))

def draw_ui(score, status_texts):
    # 绘制分数
    text_score = font_large.render(f"Score: {score}", True, WHITE)
    screen.blit(text_score, [10, 10])

    # 绘制 Trainer 状态 (右下角)
    y_offset = HEIGHT - 30
    for txt in reversed(status_texts): # 倒序排列，最新的在最下面
        t = font_small.render(txt, True, YELLOW)
        screen.blit(t, [WIDTH - t.get_width() - 10, y_offset])
        y_offset -= 25

def game_loop():
    global player_x, player_y, score, obstacle_speed, game_over

    while not game_over:
        # --- 事件监听 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Trainer 快捷键
                if event.key == pygame.K_g:
                    my_trainer.toggle_god_mode()
                elif event.key == pygame.K_m:
                    my_trainer.cycle_multiplier()
                elif event.key == pygame.K_a:
                    my_trainer.toggle_ai()

        # --- 玩家移动逻辑 ---
        keys = pygame.key.get_pressed()

        # 如果 AI 关闭，允许手动控制
        if not my_trainer.ai_enabled:
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
        else:
            # AI 自动躲避逻辑
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

        # 边界限制
        if player_x < 0: player_x = 0
        if player_x > WIDTH - player_size: player_x = WIDTH - player_size

        # --- 障碍物生成与移动 ---
        if len(obstacle_list) < 5 and random.randint(0, 20) == 1:
            start_x = random.randrange(0, WIDTH - obstacle_width)
            obstacle_list.append([start_x, -obstacle_height, obstacle_width, obstacle_height])

        for obs in obstacle_list[:]:
            obs[1] += obstacle_speed

            # 碰撞检测
            if not my_trainer.is_god_mode: # 只有非无敌模式才检测碰撞
                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
                obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])
                if player_rect.colliderect(obs_rect):
                    game_over = True

            # 移除并加分
            if obs[1] > HEIGHT:
                obstacle_list.remove(obs)
                # 应用倍率
                score += 10 * my_trainer.score_multiplier
                if score % 100 == 0:
                    obstacle_speed += 0.5

        # --- 绘图 ---
        screen.fill(BLACK)
        draw_player(player_x, player_y, my_trainer.is_god_mode)
        draw_obstacles(obstacle_list)
        draw_ui(score, my_trainer.get_status_text())

        pygame.display.update()
        clock.tick(60) # 提升流畅度到 60FPS

    # 游戏结束画面
    screen.fill(BLACK)
    msg = font_large.render("GAME OVER", True, NEON_PINK)
    score_msg = font_large.render(f"Final Score: {score}", True, WHITE)
    restart_msg = font_small.render("Press Any Key to Restart", True, WHITE)

    screen.blit(msg, [WIDTH/2 - msg.get_width()/2, HEIGHT/2 - 50])
    screen.blit(score_msg, [WIDTH/2 - score_msg.get_width()/2, HEIGHT/2 + 20])
    screen.blit(restart_msg, [WIDTH/2 - restart_msg.get_width()/2, HEIGHT/2 + 80])
    pygame.display.update()

    # 等待重启
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                # 重置游戏数据
                global player_x, score, obstacle_speed, obstacle_list, game_over
                player_x = WIDTH // 2 - player_size // 2
                score = 0
                obstacle_speed = 5
                obstacle_list = []
                game_over = False
                game_loop() # 递归调用重新开始

if __name__ == "__main__":
    game_loop()
