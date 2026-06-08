import pygame
import random
import sys

# --- 初始化设置 ---
pygame.init()

# 屏幕参数
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("霓虹猎手：量子核心 (AI/人机 双模式)")

# 颜色定义 (R, G, B)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# 玩家设置
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 100
player_speed = 7

# 障碍物设置
obstacle_width = 60
obstacle_height = 20
obstacle_list = []
base_obstacle_speed = 4  # 稍微降低基础速度，让前期更好存活

# 分数与状态
score = 0
clock = pygame.time.Clock()
game_over = False

# 【核心新增】AI 经验成长系统
ai_experience = 0
ai_reaction_threshold = 200  # 初始反应距离调大（200），保证前期不撞
current_speed = base_obstacle_speed 

# 【新增】模式控制：'AI' 为自动模式，'PLAYER' 为手动模式
game_mode = 'AI' 

# 字体设置
try:
    font = pygame.font.Font(None, 55)
    small_font = pygame.font.Font(None, 30)
except:
    font = pygame.font.SysFont('arial', 55)
    small_font = pygame.font.SysFont('arial', 30)

def draw_player(x, y):
    pygame.draw.rect(screen, NEON_BLUE, (x, y, player_size, player_size))
    pygame.draw.rect(screen, (0, 100, 100), (x-2, y-2, player_size+4, player_size+4), 2)

def draw_obstacles(obs_list):
    for obs in obs_list:
        pygame.draw.rect(screen, NEON_PINK, (obs[0], obs[1], obstacle_width, obstacle_height))

def show_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global obstacle_list, score, ai_experience, ai_reaction_threshold, current_speed, player_x, game_over, game_mode
    obstacle_list.clear()
    score = 0
    ai_experience = 0
    ai_reaction_threshold = 200
    current_speed = base_obstacle_speed
    player_x = WIDTH // 2 - player_size // 2
    game_over = False
    game_mode = 'AI'  # 重置后默认回到 AI 模式

# --- 游戏主循环 ---
while True:
    screen.fill(BLACK)
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
            # 【新增】按 M 键可以在游戏进行中切换模式
            if event.key == pygame.K_m and not game_over:
                game_mode = 'PLAYER' if game_mode == 'AI' else 'AI'
                # 切换到手动模式时，重置玩家位置
                if game_mode == 'PLAYER':
                    player_x = WIDTH // 2 - player_size // 2

    if not game_over:
        # 1. 积累经验，AI 变聪明（仅在 AI 模式下生效）
        if game_mode == 'AI':
            ai_experience += 1
            # 每存活 60 帧（约1秒），AI 变聪明一点
            if ai_experience % 60 == 0:
                if ai_reaction_threshold > 40:  # 反应距离最小为40，防止卡进墙里
                    ai_reaction_threshold -= 3  # 每次减少的幅度变小，让成长更平滑
                current_speed = min(base_obstacle_speed + ai_experience // 600, 12) # 速度上限设为12，保证能玩30秒以上

        # 2. 生成障碍物
        if len(obstacle_list) < 5:
            spawn_rate = 2 + (ai_experience // 800) if game_mode == 'AI' else 2
            if random.randint(1, 100) < spawn_rate:
                obs_x = random.randint(0, WIDTH - obstacle_width)
                obstacle_list.append([obs_x, -obstacle_height])

        # 3. 移动障碍物
        for obs in obstacle_list[:]:
            obs[1] += current_speed
            if obs[1] > HEIGHT:
                obstacle_list.remove(obs)
                score += 10

        # 4. 玩家/AI 移动逻辑
        if game_mode == 'AI':
            # AI 自动躲避逻辑
            for obs in obstacle_list:
                if obs[1] + obstacle_height > player_y and obs[1] < player_y + player_size:
                    distance_to_obs = abs((obs[0] + obstacle_width // 2) - (player_x + player_size // 2))
                    if distance_to_obs < ai_reaction_threshold:
                        if player_x + player_size // 2 < obs[0] + obstacle_width // 2:
                            player_x -= player_speed
                        else:
                            player_x += player_speed
        else:
            # 【新增】玩家手动控制逻辑（左、右方向键）
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
        
        # 限制玩家在屏幕内
        player_x = max(0, min(player_x, WIDTH - player_size))

        # 5. 碰撞检测
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for obs in obstacle_list:
            obs_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
            if player_rect.colliderect(obs_rect):
                game_over = True

    # --- 绘制画面 ---
    draw_player(player_x, player_y)
    draw_obstacles(obstacle_list)
    
    # 显示分数和状态
    show_text(f"Score: {score}", font, WHITE, 10, 10)
    
    # 显示当前模式
    mode_text = "Mode: AI" if game_mode == 'AI' else "Mode: PLAYER"
    mode_color = NEON_BLUE if game_mode == 'AI' else YELLOW
    show_text(mode_text, small_font, mode_color, 10, 60)

    # 如果在 AI 模式，显示 AI 经验数据
    if game_mode == 'AI':
        show_text(f"AI 经验: {ai_experience // 60} 级", small_font, NEON_BLUE, 10, 90)
        show_text(f"反应阈值: {ai_reaction_threshold}", small_font, NEON_BLUE, 10, 120)
    else:
        show_text("按 [左/右] 键移动", small_font, YELLOW, 10, 90)

    show_text("按 [M] 键切换模式", small_font, WHITE, WIDTH - 220, 10)

    if game_over:
        show_text("GAME OVER", font, RED, WIDTH//2 - 120, HEIGHT//2 - 50)
        show_text("按 R 键重新开始", small_font, WHITE, WIDTH//2 - 100, HEIGHT//2 + 20)

    pygame.display.flip()
    clock.tick(60)
