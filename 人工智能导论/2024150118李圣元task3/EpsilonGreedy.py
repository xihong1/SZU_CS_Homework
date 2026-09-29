import numpy as np
import matplotlib.pyplot as plt

#多臂老虎机框架
class BernoulliBandit:
    #初始化
    def __init__(self,n_arms):
        self.n_arms = n_arms#臂数
        self.probs = np.random.uniform(size=n_arms)#初始化数字表示每一个机器的概率
        self.best_idx = np.argmax(self.probs)#最好的机器的索引
        self.best_prob = self.probs[self.best_idx]#最好的机器的概率
        self.value = np.zeros(n_arms)#记录当前已知的概率
        self.numbers = np.zeros(n_arms)#记录当前机器使用的次数
        self.regrets = []#逐步记录后悔值
        (self.regret)=0.0#总的后悔值
        self.instant_rewards = []#记录每一步的奖励值

    #获取当前奖励0 or 1
    def get_reward(self, chosen_arm):
        return 1 if np.random.random() < self.probs[chosen_arm] else 0

    #更新后悔值
    def update_regard(self, chosen_arm):
        self.regret += self.best_prob - self.probs[chosen_arm]
        self.regrets.append(self.regret)
    @property
    def cum_reward(self):
        return np.cumsum(self.instant_rewards)

#epsilon贪心
class EpsilonGreedy():
    def __init__(self,bandit: BernoulliBandit,epsilon):
        self.bandit = bandit
        self.epsilon = epsilon
        self.bandit.value = np.full(self.bandit.n_arms, 1.0)

    #选择机器臂
    def choose_arm(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.bandit.n_arms)
        else:
            return np.argmax(self.bandit.value)

    #更新当前概率以及选择的次数
    def update(self,chosen_arm,reward):
        self.bandit.numbers[chosen_arm] += 1
        n=self.bandit.numbers[chosen_arm]
        self.bandit.value[chosen_arm]=(n - 1) / n * self.bandit.value[chosen_arm] + reward / n

    #运行程序
    def run(self,n_steps):
        for _ in range(n_steps):
            chosen_arm = self.choose_arm()
            r=self.bandit.get_reward(chosen_arm)
            self.bandit.instant_rewards.append(r)
            self.update(chosen_arm,r)
            self.bandit.update_regard(chosen_arm)


#绘制图像
def draw_reward_regret(agent, label):
    fig, (ax_reg, ax_rew) = plt.subplots(1, 2, figsize=(12, 4))
    t = np.arange(1, len(agent.bandit.regrets) + 1)
    ax_reg.plot(t, agent.bandit.regrets, color='r', linewidth=1.5)
    ax_reg.set_xlabel('Time steps')
    ax_reg.set_ylabel('Cumulative regret', color='r')
    ax_reg.set_title(f'{label} - Regret')
    ax_reg.grid(True, alpha=0.3)
    ax_rew.plot(t, agent.bandit.cum_reward, color='b', linewidth=1.5)
    ax_rew.set_xlabel('Time steps')
    ax_rew.set_ylabel('Cumulative reward', color='b')
    ax_rew.set_title(f'{label} - Reward')
    ax_rew.grid(True, alpha=0.3)
    fig.suptitle(f'{agent.bandit.n_arms}-armed bandit', fontsize=14, y=1.02)
    fig.tight_layout()
    plt.savefig(f'{label}_combined.png', dpi=300, bbox_inches='tight')
    plt.show()


def draw_multi_epsilon_results(agents, eps_vals):
    fig, (ax_reg, ax_rew) = plt.subplots(1, 2, figsize=(14, 5))
    colors = ['r', 'g', 'b', 'm', 'c','purple']
    for idx, (agent, eps) in enumerate(zip(agents, eps_vals)):
        t = np.arange(1, len(agent.bandit.regrets) + 1)
        color = colors[idx % len(colors)]
        ax_reg.plot(t, agent.bandit.regrets, color=color, linewidth=1.5,
                    label=f'ε={eps}')
        ax_rew.plot(t, agent.bandit.cum_reward, color=color, linewidth=1.5,
                    label=f'ε={eps}')
    ax_reg.set_xlabel('Time steps')
    ax_reg.set_ylabel('Cumulative regret')
    ax_reg.set_title('Regret Comparison')
    ax_reg.legend(loc='upper left')
    ax_reg.grid(True, alpha=0.3)
    ax_rew.set_xlabel('Time steps')
    ax_rew.set_ylabel('Cumulative reward')
    ax_rew.set_title('Reward Comparison')
    ax_rew.legend(loc='upper left')
    ax_rew.grid(True, alpha=0.3)
    fig.suptitle(f'{agents[0].bandit.n_arms}-armed bandit - Multiple ε Comparison',
                 fontsize=14, y=1.02)
    fig.tight_layout()
    plt.savefig('multi_epsilon_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

np.random.seed(1)
if __name__ == '__main__':
    n_steps = 5000
    n_arms = 10
    eps_vals = [0.0,1e-4,0.01,0.1,0.25,0.5]
    agents = []
    for eps in eps_vals:
        bandit = BernoulliBandit(n_arms)
        agent = EpsilonGreedy(bandit, eps)
        agent.run(n_steps)
        agents.append(agent)
    # 一次性绘制所有结果
    draw_multi_epsilon_results(agents, eps_vals)
    # bandit = BernoulliBandit(n_arms)
    # np.random.seed(1)
    # eps = EpsilonGreedy(bandit, eps_val)
    # eps.run(n_steps)
    # draw_reward_regret(eps, f'ε-greedy ({eps_val})')