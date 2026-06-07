# trainer.py - 游戏修改器与状态管理模块

class Trainer:
    def __init__(self):
        # 初始化所有修改器状态为关闭/默认值
        self.is_god_mode = False       # 无敌模式
        self.score_multiplier = 1      # 分数倍率 (1, 5, 10...)
        self.ai_enabled = True         # AI 自动驾驶开关

    def toggle_god_mode(self):
        """切换无敌模式"""
        self.is_god_mode = not self.is_god_mode
        status = "开启" if self.is_god_mode else "关闭"
        print(f"[Trainer] 上帝模式已{status}")
        return self.is_god_mode

    def cycle_multiplier(self):
        """循环切换分数倍率 (1 -> 5 -> 10 -> 1)"""
        if self.score_multiplier == 1:
            self.score_multiplier = 5
        elif self.score_multiplier == 5:
            self.score_multiplier = 10
        else:
            self.score_multiplier = 1
        print(f"[Trainer] 分数倍率调整为: x{self.score_multiplier}")
        return self.score_multiplier

    def toggle_ai(self):
        """切换 AI 自动躲避模式"""
        self.ai_enabled = not self.ai_enabled
        status = "接管" if self.ai_enabled else "手动"
        print(f"[Trainer] 控制权已切换为: {status}模式")
        return self.ai_enabled

    def get_status_text(self):
        """生成用于屏幕显示的当前状态字符串列表"""
        status_list = []
        if self.is_god_mode:
            status_list.append("GOD MODE: ON")
        if self.score_multiplier > 1:
            status_list.append(f"SCORE x{self.score_multiplier}")
        if self.ai_enabled:
            status_list.append("AI PILOT: ACTIVE")
        else:
            status_list.append("MANUAL CONTROL")
        return status_list
