import pygame
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# 配色常量
PANEL_BG = (20, 25, 40)
TEXT_COL = (230, 230, 230)

class Dashboard:
    """仪表盘面板"""
    def __init__(self, game_width, game_height, panel_width):
        self.game_width = game_width
        self.game_height = game_height
        self.panel_width = panel_width
        self.plot_surface = None
        self.score_history = []

    def update_plot(self, score_history):
        """更新分数趋势图"""
        self.score_history = score_history
        self.plot_surface = self._make_plot()

    def _make_plot(self):
        """生成分数折线图"""
        if not self.score_history:
            return None
            
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(3.6, 2.2), dpi=100)
        ax.plot(self.score_history, c="#00d8ff", linewidth=2)
        ax.set_title("历代最高分走势", c="white", fontsize=9)
        ax.set_xlabel("世代", c="white", fontsize=8)
        ax.set_ylabel("分数", c="white", fontsize=8)
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw(self, screen, data):
        """绘制仪表盘"""
        # 绘制面板背景
        pygame.draw.rect(
            screen, 
            PANEL_BG, 
            (self.game_width, 0, self.panel_width, self.game_height)
        )
        
        # 字体
        font = pygame.font.SysFont("simhei", 22)
        
        # 显示信息
        info = [
            f"当前世代：{data['generation']}",
            f"运行倍速：{data['game_speed']}x [+/-调速]",
            f"历史最高分：{data['max_score']}",
            f"存活AI数量：{data['alive_count']}",
            "ESC退出 | 空格重置"
        ]
        
        for idx, text in enumerate(info):
            rendered_text = font.render(text, True, TEXT_COL)
            screen.blit(rendered_text, (self.game_width + 15, 20 + idx * 32))
        
        # 绘制折线图
        if self.plot_surface:
            screen.blit(self.plot_surface, (self.game_width + 12, 220))
