import pygame
import random
import sys

# --- 初始化设置 ---
pygame.init()

# 屏幕参数
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("霓虹猎手：量子核心 (AI 自动版)")

# 颜色定义 (R, G, B)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

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

# 【关键修复】使用 Pygame 内置默认字体，不再调用 SysFont，防止报错
try:
    font = pygame.font.Font(None, 55)
except:
    # 如果连默认字体都加载失败（极少见），强制指定一个路径或降级处理
    font = pygame.font.SysFont('arial', 55)

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

def game_loop():
    global player_x, player_y, score, obstacle_speed, game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- AI 逻辑 (自动躲避) ---
        # 寻找离玩家最近的障碍物
        closest_obs = None
        min_dist = float('inf')

        for obs in obstacle_list:
            # 计算障碍物底部到玩家顶部的距离
            dist = (player_y) - (obs[1] + obs[3])
            # 只关心还没完全过去的障碍物，且距离在一定范围内
            if 0 < dist < 300 and abs((obs[0] + obs[2]/2) - (player_x + player_size/2)) < 100:
                if dist < min_dist:
                    min_dist = dist
                    closest_obs = obs

        if closest_obs:
            target_x = closest_obs[0] + closest_obs[2] / 2  # 障碍物中心
            current_center = player_x + player_size / 2     # 玩家中心

            # 简单的左右移动逻辑
            if current_center < target_x - 10:
                player_x += player_speed
            elif current_center > target_x + 10:
                player_x -= player_speed

        # 边界限制
        if player_x < 0: player_x = 0
        if player_x > WIDTH - player_size: player_x = WIDTH - player_size

        # --- 生成障碍物 ---
        if len(obstacle_list) < 5 and random.randint(0, 20) == 1:
            start_x = random.randrange(0, WIDTH - obstacle_width)
            obstacle_list.append([start_x, -obstacle_height, obstacle_width, obstacle_height])

        # --- 移动障碍物 & 碰撞检测 ---
        for obs in obstacle_list[:]: # 遍历副本以便安全删除
            obs[1] += obstacle_speed # 向下移动

            # 碰撞检测 (简单的矩形碰撞)
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])

            if player_rect.colliderect(obs_rect):
                game_over = True

            # 移除超出屏幕的障碍物并加分
            if obs[1] > HEIGHT:
                obstacle_list.remove(obs)
                score += 10
                if score % 100 == 0: # 每100分加速
                    obstacle_speed += 0.5

        # --- 绘图 ---
        screen.fill(BLACK)
        draw_player(player_x, player_y)
        draw_obstacles(obstacle_list)
        draw_score(score)

        pygame.display.update()
        clock.tick(30) # 控制帧率

    # 游戏结束画面
    screen.fill(BLACK)
    msg = font.render("GAME OVER", True, NEON_PINK)
    score_msg = font.render("Score: " + str(score), True, WHITE)
    screen.blit(msg, [WIDTH/2 - msg.get_width()/2, HEIGHT/2 - 50])
    screen.blit(score_msg, [WIDTH/2 - score_msg.get_width()/2, HEIGHT/2 + 20])
    pygame.display.update()

    # 等待几秒后退出或按任意键退出
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
