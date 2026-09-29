import numpy as np
import matplotlib.pyplot as plt
from EpsilonGreedy import BernoulliBandit
class UCB:
    def __init__(self, bandit: BernoulliBandit, c=1.0):
        self.bandit = bandit
        self.bandit.value = np.full(self.bandit.n_arms,1.0)
        self.c = c
        self.t = 0

    def choose_arm(self):
        self.t += 1
        ucb_vals = self.bandit.value.copy()
        for i in range(self.bandit.n_arms):
            exploration_bonus = self.c * np.sqrt(np.log(self.t) /(2* self.bandit.numbers[i]+1))
            ucb_vals[i] = self.bandit.value[i] + exploration_bonus
        return np.argmax(ucb_vals)

    def update(self, arm, reward):
        self.bandit.numbers[arm] += 1
        n = self.bandit.numbers[arm]
        self.bandit.value[arm] = (n - 1) / n * self.bandit.value[arm] + reward / n

    def run(self, n_steps):
        for _ in range(n_steps):
            chosen_arm = self.choose_arm()
            r = self.bandit.get_reward(chosen_arm)
            self.bandit.instant_rewards.append(r)
            self.update(chosen_arm, r)
            self.bandit.update_regard(chosen_arm)

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

def draw_multi_UCB_results(agents, c_vals):
    fig, (ax_reg, ax_rew) = plt.subplots(1, 2, figsize=(14, 5))
    colors = ['r', 'g', 'b', 'm', 'c','purple']
    for idx, (agent, c) in enumerate(zip(agents, c_vals)):
        t = np.arange(1, len(agent.bandit.regrets) + 1)
        color = colors[idx % len(colors)]
        ax_reg.plot(t, agent.bandit.regrets, color=color, linewidth=1.5,
                    label=f'c={c}')
        ax_rew.plot(t, agent.bandit.cum_reward, color=color, linewidth=1.5,
                    label=f'c={c}')
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
    fig.suptitle(f'{agents[0].bandit.n_arms}-armed bandit - Multiple c Comparison',
                 fontsize=14, y=1.02)
    fig.tight_layout()
    plt.savefig('multi_UCB_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
np.random.seed(1)
# ---------------- 主入口 ----------------
if __name__ == '__main__':
    n_steps = 5000
    n_arms = 10
    c_values=[0.0,0.25,0.5,0.75,1.0]
    agents = []
    for c in c_values:
        bandit = BernoulliBandit(n_arms)
        agent = UCB(bandit, c)
        agent.run(n_steps)
        agents.append(agent)
    draw_multi_UCB_results(agents, c_values)
    # bandit = BernoulliBandit(n_arms)
    # np.random.seed(1)
    # ucb_agent = UCB(bandit)
    # ucb_agent.run(n_steps)
    # draw_reward_and_regret(ucb_agent, 'UCB')