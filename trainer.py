import random
import copy

class BikeGenome:
    """AI光轮基因类"""
    def __init__(self, dx=None, dy=None):
        # 基因表示初始移动方向
        self.dx = dx if dx is not None else (5 if random.random() > 0.5 else -5)
        self.dy = dy if dy is not None else 0
    
    def mutate(self):
        """基因突变"""
        if random.random() < 0.25:  # 25%概率变异
            self.dx = 5 if random.random() > 0.5 else -5
            self.dy = 0
        return self

class BikeRaceTrainer:
    """AI光轮训练器"""
    def __init__(self):
        self.current_gen = 1
        self.max_score = 0
        self.score_history = []
    
    def evolve_generation(self, ai_pop):
        """进化下一代"""
        self.current_gen += 1
        
        # 选择最佳个体
        best = max(ai_pop, key=lambda x: x.score)
        self.max_score = max(self.max_score, best.score)
        self.score_history.append(best.score)
        
        # 繁衍变异
        pop_num = len(ai_pop)
        new_pop = []
        
        for _ in range(pop_num):
            # 复制最佳个体
            new_bike = copy.deepcopy(best)
            
            # 应用基因突变
            genome = BikeGenome(new_bike.dx, new_bike.dy)
            mutated_genome = genome.mutate()
            new_bike.dx = mutated_genome.dx
            new_bike.dy = mutated_genome.dy
            
            # 重置状态
            new_bike.trail.clear()
            new_bike.alive = True
            new_bike.score = 0
            new_pop.append(new_bike)
        
        # 更新种群
        for i in range(len(ai_pop)):
            ai_pop[i] = new_pop[i]
