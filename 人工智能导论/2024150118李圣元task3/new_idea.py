import numpy as np
import matplotlib.pyplot as plt

class BernoulliBandit:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.probs = np.random.uniform(size=n_arms)
        self.best_idx = np.argmax(self.probs)
        self.best_prob = self.probs[self.best_idx]
        self.instant_rewards = []
        self.regrets = []
        self.regret = 0.0
        self.n_pulls = np.zeros(n_arms, dtype=int)

    def get_reward(self, chosen):
        return 1 if np.random.random() < self.probs[chosen] else 0

    def update_regret(self, chosen):
        self.regret += self.best_prob - self.probs[chosen]
        self.regrets.append(self.regret)

    @property
    def cum_reward(self):
        return np.cumsum(self.instant_rewards)


class EpsilonGreedy:
    def __init__(self, bandit: BernoulliBandit, epsilon):
        self.bandit = bandit
        self.epsilon = epsilon
        self.values = np.full(self.bandit.n_arms, 1.0)
        self.counts = np.zeros(self.bandit.n_arms)

    def choose_arm(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.bandit.n_arms)
        else:
            return np.argmax(self.values)

    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] = (n - 1) / n * self.values[arm] + reward / n

    def run(self, n_steps):
        for _ in range(n_steps):
            arm = self.choose_arm()
            r = self.bandit.get_reward(arm)
            self.bandit.instant_rewards.append(r)
            self.update(arm, r)
            self.bandit.update_regret(arm)


class GroupedProbabilityAgent:
    def __init__(self, bandit: BernoulliBandit, alpha=0.1):
        self.bandit = bandit
        self.n = bandit.n_arms
        self.alpha = alpha

        self.selection_probs = np.full(self.n, 1.0 / self.n)#概率
        self.exp_counts = np.zeros(self.n)#选中次数
        self.exp_wins = np.zeros(self.n)#获奖次数
        self.probs_history = [self.selection_probs.copy()]
    #将概率归一化
    def _safe_renorm(self):
        s = self.selection_probs.sum()
        if s <= 0:
            self.selection_probs = np.full(self.n, 1.0 / self.n)
        else:
            self.selection_probs = np.maximum(self.selection_probs, 1e-12)
            self.selection_probs = self.selection_probs / self.selection_probs.sum()
    #更新概率
    def _multiplicative_update(self, arm, reward):
        if reward == 1:
            self.selection_probs[arm] *= (1 + self.alpha)
        else:
            self.selection_probs[arm] *= max(0.0, (1 - self.alpha))
        self._safe_renorm()
        self.probs_history.append(self.selection_probs.copy())
    #初始化探索
    def initial_exploration(self):
        for arm in range(self.n):
            for _ in range(self.n):
                r = self.bandit.get_reward(arm)
                self.bandit.instant_rewards.append(r)
                self.bandit.n_pulls[arm] += 1
                self.bandit.update_regret(arm)
                self.exp_counts[arm] += 1
                self.exp_wins[arm] += r
                self._multiplicative_update(arm, r)
                self.probs_history.append(self.selection_probs.copy())

        # empirical = np.zeros(self.n)
        # mask = self.exp_counts > 0
        # empirical[mask] = self.exp_wins[mask] / self.exp_counts[mask]
        # empirical += 1e-6
        # empirical /= empirical.sum()
        # self.selection_probs = empirical
        # self.probs_history.append(self.selection_probs.copy())
    #分组
    def make_groups(self):
        order = np.argsort(-self.selection_probs)
        base = self.n // 3
        if base == 0:
            groups = [[i] for i in order]
        else:
            g1 = list(order[:base])
            g2 = list(order[base:2 * base])
            g3 = list(order[2 * base:])
            groups = [g1, g2, g3]

        group_probs = np.array([self.selection_probs[g].sum() if len(g) > 0 else 0.0 for g in groups])
        group_probs = group_probs / (group_probs.sum() + 1e-9)
        return groups, group_probs
    #第二步
    def grouped_phase(self, steps):
        groups, group_probs = self.make_groups()
        num_groups = len(groups)
        for _ in range(steps):
            g_idx = np.random.choice(np.arange(num_groups), p=group_probs)
            group = groups[g_idx]
            arm = np.random.choice(group)
            r = self.bandit.get_reward(arm)
            self.bandit.instant_rewards.append(r)
            self.bandit.n_pulls[arm] += 1
            self.exp_counts[arm] += 1
            self.exp_wins[arm] += r
            self._multiplicative_update(arm, r)
            self.bandit.update_regret(arm)
            groups, group_probs = self.make_groups()
    #最后一步
    def final_phase(self, steps):
        for _ in range(steps):
            arm = np.random.choice(np.arange(self.n), p=self.selection_probs)
            r = self.bandit.get_reward(arm)
            self.bandit.instant_rewards.append(r)
            self.bandit.n_pulls[arm] += 1
            self.exp_counts[arm] += 1
            self.exp_wins[arm] += r
            self._multiplicative_update(arm, r)
            self.bandit.update_regret(arm)

    def run(self, n_steps):
        steps1 = min(self.n * self.n, n_steps)
        steps2 = min(self.n * self.n, max(0, n_steps - steps1))
        steps3 = max(0, n_steps - steps1 - steps2)

        if steps1 > 0:
            self.initial_exploration()
        if steps2 > 0:
            self.grouped_phase(steps2)
        if steps3 > 0:
            self.final_phase(steps3)


def plot_compare(agents, labels, title_prefix):
    plt.figure(figsize=(12, 4))
    for agent, label in zip(agents, labels):
        t = np.arange(1, len(agent.bandit.regrets) + 1)
        plt.plot(t, agent.bandit.regrets, linewidth=1.5, label=label)
    plt.xlabel("Time")
    plt.ylabel("Cumulative Regret")
    plt.title(f"{title_prefix} - Regret")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 4))
    for agent, label in zip(agents, labels):
        cum = agent.bandit.cum_reward
        t = np.arange(1, len(cum) + 1)
        plt.plot(t, cum, linewidth=1.5, label=label)
    plt.xlabel("Time")
    plt.ylabel("Cumulative Reward")
    plt.title(f"{title_prefix} - Reward")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


#对比epsilon贪心和我的算法的优劣性
def experiment_compare_all():
    np.random.seed(1)
    n_steps = 5000
    n_arms = 10
    eps_list_greedy = [ 0.1]
    alpha_list = [0.05, 0.1, 0.2]
    agents = []
    labels = []

    for eps in eps_list_greedy:
        bandit = BernoulliBandit(n_arms)
        agent = EpsilonGreedy(bandit, eps)
        agent.run(n_steps)
        agents.append(agent)
        labels.append(f"EpsGreedy ε={eps}")

    for alpha in alpha_list:
            bandit = BernoulliBandit(n_arms)
            agent = GroupedProbabilityAgent(bandit, alpha=alpha)
            agent.run(n_steps)
            agents.append(agent)
            labels.append(f"Grouped α={alpha}")

    plot_compare(agents, labels, "All Algorithms Comparison")
#在不同步数与臂数组合下，后悔值与奖励值的值
def experiment_param_scan():
    np.random.seed(1)

    n_arms_list = [5, 10, 20]
    n_steps_list = [2000, 5000, 10000]

    alpha = 0.1

    results = []

    for n_arms in n_arms_list:
        for n_steps in n_steps_list:
            bandit = BernoulliBandit(n_arms)
            agent = GroupedProbabilityAgent(bandit, alpha=alpha)
            agent.run(n_steps)

            # 新增：计算平均指标
            avg_regret = bandit.regrets[-1] / n_steps
            avg_reward = bandit.cum_reward[-1] / n_steps

            results.append({
                "n_arms": n_arms,
                "n_steps": n_steps,
                "avg_regret": avg_regret,
                "avg_reward": avg_reward
            })

    # 新增：统一展示所有组合的对比图
    plot_summary_across_configs(results)



def plot_summary_across_configs(results):

    plt.figure(figsize=(12,5))
    # 左图：平均后悔值
    plt.subplot(1,2,1)
    for r in results:
        label = f"{r['n_arms']} arms, {r['n_steps']} steps"
        plt.scatter(r["n_steps"], r["avg_regret"], s=80)
        plt.text(r["n_steps"], r["avg_regret"], label, fontsize=9)
    plt.xlabel("Steps")
    plt.ylabel("Average Regret (Regret / Steps)")
    plt.title("Average Regret Across Arm/Step Configurations")
    plt.grid(alpha=0.3)
    # 右图：平均奖励
    plt.subplot(1,2,2)
    for r in results:
        label = f"{r['n_arms']} arms, {r['n_steps']} steps"
        plt.scatter(r["n_steps"], r["avg_reward"], s=80)
        plt.text(r["n_steps"], r["avg_reward"], label, fontsize=9)
    plt.xlabel("Steps")
    plt.ylabel("Average Reward (TotalReward / Steps)")
    plt.title("Average Reward Across Arm/Step Configurations")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Running comparison experiment...")
    experiment_compare_all()

    print("Running parameter scan for your algorithm...")
    experiment_param_scan()

