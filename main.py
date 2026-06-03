import pygame
import sys
from game import GameEngine
from trainer import BikeRaceTrainer
from dashboard import Dashboard

def main():
    # 初始化Pygame
    pygame.init()
    W, H = 800, 600
    PANEL_W = 380
    SCREEN_W = W + PANEL_W
    
    screen = pygame.display.set_mode((SCREEN_W, H))
    pygame.display.set_caption("AI极速光轮｜遗传进化训练")
    clock = pygame.time.Clock()
    
    # 创建游戏引擎、训练器和仪表盘
    game_engine = GameEngine(W, H)
    trainer = BikeRaceTrainer()
    dashboard = Dashboard(W, H, PANEL_W)
    
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_EQUALS:  # +加速
                    game_engine.game_speed = min(game_engine.game_speed + 1, 20)
                if event.key == pygame.K_MINUS:   # -减速
                    game_engine.game_speed = max(game_engine.game_speed - 1, 1)
                if event.key == pygame.K_SPACE:
                    game_engine.reset_world()
        
        # 更新游戏状态
        game_state = game_engine.update()
        
        # 检查是否需要进化
        if game_state['all_ai_dead']:
            trainer.evolve_generation(game_engine.ai_pop)
            dashboard.update_plot(trainer.score_history)
        
        # 渲染
        screen.fill((5, 8, 22))  # BG color
        
        # 绘制游戏区域
        game_engine.draw_game_area(screen)
        
        # 绘制仪表盘
        dashboard_data = {
            'generation': trainer.current_gen,
            'max_score': trainer.max_score,
            'alive_count': sum(1 for ai in game_engine.ai_pop if ai.alive),
            'game_speed': game_engine.game_speed
        }
        dashboard.draw(screen, dashboard_data)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
