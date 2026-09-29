import numpy as np
import matplotlib.pyplot as plt
from EpsilonGreedy import BernoulliBandit

class Thompsonsampling:
    def __init__(self, bandit: BernoulliBandit):
        self.bandit = bandit
        self.alphas = np.ones(bandit.n_arms)
        self.betas = np.ones(bandit.n_arms)
        self.bandit.value = np.full(self.bandit.n_arms, 1.0)

    def choose_arm(self):
        samples = np.random.beta(self.alphas, self.betas)
        return np.argmax(samples)

    def update(self, chosen_arm, reward):
        self.alphas[chosen_arm] += reward
        self.betas[chosen_arm] += 1 - reward
        self.bandit.numbers[chosen_arm] += 1
        n = self.bandit.numbers[chosen_arm]
        self.bandit.numbers[chosen_arm] = (
            (n - 1) / n * self.bandit.numbers[chosen_arm] + reward / n
        )
    def run(self, n_steps):
        for _ in range(n_steps):
            arm = self.choose_arm()
            r = self.bandit.get_reward(arm)
            self.bandit.instant_rewards.append(r)
            self.update(arm, r)
            self.bandit.update_regard(arm)

# ---------------- 画图 ----------------
def draw_reward_and_regret(agent, label):
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

# ---------------- 主入口 ----------------
if __name__ == '__main__':
    np.random.seed(1)
    n_steps = 5000
    n_arms = 10
    bandit = BernoulliBandit(n_arms)
    np.random.seed(1)
    thompson = Thompsonsampling(bandit)
    thompson.run(n_steps)
    draw_reward_and_regret(thompson, 'Thompson sampling')