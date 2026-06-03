import pygame
import random

# 配色常量
PLAYER_COL = (0, 215, 255)
TRAIL_COL = (0, 125, 190)
AI_COL = (255, 75, 195)

class BikeAI:
    def __init__(self, x=None, y=None, dx=None, dy=None):
        self.x = x if x is not None else random.randint(100, W-100)
        self.y = y if y is not None else random.randint(100, H-100)
        self.dx = dx if dx is not None else (speed if random.random() > 0.5 else -speed)
        self.dy = dy if dy is not None else 0
        self.trail = []
        self.alive = True
        self.score = 0

class GameEngine:
    def __init__(self, width, height):
        global W, H, size, speed
        W, H = width, height
        size = 8
        speed = 5
        
        # 游戏参数
        self.game_speed = 1
        
        # 初始化AI种群
        self.pop_num = 6
        self.ai_pop = [BikeAI() for _ in range(self.pop_num)]
        
        # 玩家初始化
        self.px, self.py = W // 2, H // 2
        self.pdx, self.pdy = speed, 0
        self.p_trail = []
        self.game_over = False

    def reset_world(self):
        """重置游戏世界"""
        self.px, self.py = W // 2, H // 2
        self.pdx, self.pdy = speed, 0
        self.p_trail.clear()
        self.game_over = False
        
        for ai in self.ai_pop:
            ai.x = random.randint(80, W-80)
            ai.y = random.randint(80, H-80)
            ai.dx = speed if random.random() > 0.5 else -speed
            ai.dy = 0
            ai.trail.clear()
            ai.alive = True

    def update(self):
        """更新游戏状态"""
        # 多倍速循环
        for _ in range(self.game_speed):
            # 玩家操控
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.pdy != speed:
                self.pdx, self.pdy = 0, -speed
            if keys[pygame.K_DOWN] and self.pdy != -speed:
                self.pdx, self.pdy = 0, speed
            if keys[pygame.K_LEFT] and self.pdx != speed:
                self.pdx, self.pdy = -speed, 0
            if keys[pygame.K_RIGHT] and self.pdx != -speed:
                self.pdx, self.pdy = speed, 0
            
            self.p_trail.append((self.px, self.py))
            self.px += self.pdx
            self.py += self.pdy
            
            # 玩家碰撞检测
            if (self.px < 0 or self.px > W - size or 
                self.py < 0 or self.py > H - size or 
                (self.px, self.py) in self.p_trail[:-6]):
                self.reset_world()

            # AI逻辑
            all_dead = True
            for ai in self.ai_pop:
                if not ai.alive:
                    continue
                all_dead = False
                ai.trail.append((ai.x, ai.y))
                ai.x += ai.dx
                ai.y += ai.dy
                ai.score += 1
                
                # 碰壁转向
                if ai.x <= 0 or ai.x >= W - size:
                    ai.dx = -ai.dx
                if ai.y <= 0 or ai.y >= H - size:
                    ai.dy = -ai.dy
                
                # 撞轨迹淘汰
                if ((ai.x, ai.y) in self.p_trail or 
                    (ai.x, ai.y) in ai.trail[:-5]):
                    ai.alive = False
            
            if all_dead:
                return {'all_ai_dead': True}
        
        return {'all_ai_dead': False}

    def draw_game_area(self, screen):
        """绘制游戏区域"""
        # 绘制玩家轨迹
        for x, y in self.p_trail:
            pygame.draw.rect(screen, TRAIL_COL, (x, y, size, size))
        
        # 绘制AI轨迹
        for ai in self.ai_pop:
            for x, y in ai.trail:
                pygame.draw.rect(screen, AI_COL, (x, y, size, size))
        
        # 绘制玩家
        pygame.draw.rect(screen, PLAYER_COL, (self.px, self.py, size, size))
        
        # 绘制存活的AI
        for ai in self.ai_pop:
            if ai.alive:
                pygame.draw.rect(screen, AI_COL, (ai.x, ai.y, size, size))
