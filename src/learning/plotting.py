import matplotlib.pyplot as plt

class plotter:
    def __init__(self):
        self.scores = []
        self.mean_scores = []

    def add_score(self, score):
        self.scores.append(score)

    def plot(self):

        self.percentages = [score.percentage_broken for score in self.scores]
        self.times = [score.time for score in self.scores]

        plt.clf()
        fig, ax1 = plt.subplots()

        x = range(1, len(self.percentages) + 1)

        color_left = 'tab:blue'
        color_right = 'tab:orange'

        line1 = ax1.plot(x, self.percentages, color=color_left, label='Percentage Broken')
        ax1.set_xlabel('Number of Games')
        ax1.set_ylabel('Percentage Broken (%)', color=color_left)
        ax1.tick_params(axis='y', labelcolor=color_left)
        ax1.set_ylim(0, 100)

        ax2 = ax1.twinx()
        line2 = ax2.plot(x, self.times, color=color_right, label='Time (s)')
        ax2.set_ylabel('Time (s)', color=color_right)
        ax2.tick_params(axis='y', labelcolor=color_right)
        ax2.set_ylim(bottom=0)

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')

        plt.title('Training Progress')
        plt.tight_layout()
        plt.pause(0.1)