import pygame
import sys
import random
import os

# --- 初始化设置 ---

pygame.init()

WIDTH, HEIGHT = 600, 800
FPS = 60

# 颜色定义

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)
GREEN = (0, 255, 0)
RED = (255, 51, 51)
CYAN = (0, 204, 255)
GRAY = (50, 50, 50)

# 游戏参数

PLAYER_SIZE = 40
OBS_SIZE = 50
BASE_SPEED = 7
SPAWN_RATE = 40  # 障碍物生成频率


class TrainGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("轨道躲避 - AI自动版")
        self.clock = pygame.time.Clock()

        # --- 核心修复：安全加载字体 ---
        try:
            font_path = "C:/Windows/Fonts/simhei.ttf"
            if not os.path.exists(font_path):
                font_path = "C:/Windows/Fonts/msyh.ttc"
            if not os.path.exists(font_path):
                raise FileNotFoundError
    
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 28)
            self.font_small = pygame.font.Font(font_path, 20)
        except Exception:
            print("未找到中文字体，将使用默认英文字体显示。")
            self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
            self.font_medium = pygame.font.SysFont("Arial", 28)
            self.font_small = pygame.font.SysFont("Arial", 20)
    
        self.reset_game()
    
    def reset_game(self):
        self.player_x = WIDTH // 2 - PLAYER_SIZE // 2
        self.player_y = HEIGHT - 100
        self.obstacles = []
        self.score = 0
        self.speed = BASE_SPEED
        self.is_paused = False
        self.is_game_over = False
        self.frame_count = 0
        self.is_ai_mode = False
    
    def spawn_obstacle(self):
        x = random.randint(0, WIDTH - OBS_SIZE)
        self.obstacles.append({"x": x, "y": -OBS_SIZE})
    
    def update(self):
        if self.is_paused or self.is_game_over:
            return
    
        self.frame_count += 1
    
        # AI 逻辑
        if self.is_ai_mode:
            self.run_ai_logic()
    
        # 障碍物移动与碰撞检测
        for obs in self.obstacles[:]:
            obs["y"] += self.speed
    
            player_rect = pygame.Rect(self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE)
            obs_rect = pygame.Rect(obs["x"], obs["y"], OBS_SIZE, OBS_SIZE)
    
            if player_rect.colliderect(obs_rect):
                self.is_game_over = True
    
            # --- 奖励机制修改：躲过一个障碍物加 10 分 ---
            if obs["y"] > HEIGHT:
                self.obstacles.remove(obs)
                self.score += 10
                # 难度随分数增加
                if self.score % 100 == 0:
                    self.speed += 0.5
    
        # 生成新障碍物
        if self.frame_count % SPAWN_RATE == 0:
            self.spawn_obstacle()
    
    def run_ai_logic(self):
        target_obs = None
        min_dist = float('inf')
    
        for obs in self.obstacles:
            if obs['y'] < self.player_y and (self.player_y - obs['y']) < 400:
                dist = self.player_y - obs['y']
                if dist < min_dist:
                    min_dist = dist
                    target_obs = obs
    
        move_speed = 8
        if target_obs:
            obs_center = target_obs['x'] + OBS_SIZE / 2
            player_center = self.player_x + PLAYER_SIZE / 2
    
            if abs(obs_center - player_center) < (OBS_SIZE + PLAYER_SIZE) / 2:
                if obs_center < player_center:
                    self.player_x += move_speed
                else:
                    self.player_x -= move_speed
            else:
                center_screen = WIDTH / 2
                if player_center < center_screen - 50:
                    self.player_x += move_speed * 0.5
                elif player_center > center_screen + 50:
                    self.player_x -= move_speed * 0.5
        else:
            center_screen = WIDTH / 2
            if self.player_x + PLAYER_SIZE/2 < center_screen:
                self.player_x += 2
            else:
                self.player_x -= 2
    
        self.player_x = max(0, min(WIDTH - PLAYER_SIZE, self.player_x))
    
    def draw(self):
        self.screen.fill(BLACK)
    
        # 绘制轨道背景线
        for i in range(0, HEIGHT, 40):
            offset = (self.frame_count * self.speed) % 40
            y = i + offset - 40
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y), 1)
    
        # 绘制玩家
        color = CYAN if self.is_ai_mode else GREEN
        pygame.draw.rect(self.screen, color, (self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE))
    
        # 绘制障碍物
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, RED, (obs["x"], obs["y"], OBS_SIZE, OBS_SIZE))
    
        # --- UI 绘制 ---
        # 1. 左上角：分数
        score_text = self.font_medium.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
    
        # 2. 右上角：模式标注 + 键盘说明
        if self.is_ai_mode:
            mode_text = "模式: AI 托管"
            mode_color = YELLOW
        else:
            mode_text = "模式: 玩家操控"
            mode_color = GREEN
    
        mode_surf = self.font_medium.render(mode_text, True, mode_color)
        self.screen.blit(mode_surf, (WIDTH - mode_surf.get_width() - 20, 20))
    
        # 键盘操作说明（右上角分行显示）
        tips = [
            "A / M: 切换模式",
            "R: 暂停 / 重开",
            "← →: 玩家移动"
        ]
        for i, tip in enumerate(tips):
            tip_surf = self.font_small.render(tip, True, GRAY)
            self.screen.blit(tip_surf, (WIDTH - tip_surf.get_width() - 20, 60 + i * 25))
    
        # 暂停或结束遮罩
        if self.is_paused or self.is_game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
    
            if self.is_game_over:
                go_text = self.font_large.render("游戏结束", True, RED)
                restart_text = self.font_medium.render("按 R 键重新开始", True, WHITE)
            else:
                go_text = self.font_large.render("已暂停", True, YELLOW)
                restart_text = self.font_medium.render("按 R 键继续", True, WHITE)
    
            self.screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.is_game_over:
                        self.reset_game()
                    else:
                        self.is_paused = not self.is_paused
    
                elif event.key in (pygame.K_a, pygame.K_m):
                    self.is_ai_mode = not self.is_ai_mode
    
        # 持续按键检测（仅玩家模式）
        if not self.is_paused and not self.is_game_over and not self.is_ai_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= 7
            if keys[pygame.K_RIGHT]:
                self.player_x += 7
    
        self.player_x = max(0, min(WIDTH - PLAYER_SIZE, self.player_x))
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        game = TrainGame()
        game.run()
    except Exception as e:
        print(f"发生错误: {e}")
        input("按回车键退出...")

