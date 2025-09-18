import matplotlib.pyplot as plt

class plotter:
    def __init__(self):
        self.percentages = []
        self.times = []
        self.mean_scores = []

    def add_score(self, score):
        self.percentages.append(score.percentage_broken)
        self.times.append(score.time)

    def plot(self):
        if not self.percentages or not self.times:
            return

        x = range(1, len(self.percentages) + 1)

        # First time: create figure and lines
        if not hasattr(self, "_plot_initialized"):
            plt.ion()
            self.fig, self.ax1 = plt.subplots()
            self.ax2 = self.ax1.twinx()

            color_left = 'tab:blue'
            color_right = 'tab:orange'

            (self.line_percentages,) = self.ax1.plot(x, self.percentages, color=color_left, label='Percentage Broken')
            (self.line_times,) = self.ax2.plot(x, self.times, color=color_right, label='Time (s)')

            self.ax1.set_xlabel('Number of Games')
            self.ax1.set_ylabel('Percentage Broken (%)', color='tab:blue')
            self.ax1.tick_params(axis='y', labelcolor='tab:blue')
            self.ax1.set_ylim(0, 100)

            self.ax2.set_ylabel('Time (s)', color='tab:orange')
            self.ax2.tick_params(axis='y', labelcolor='tab:orange')
            self.ax2.set_ylim(bottom=0, top=max(self.times) * 1.1 if self.times else 1)

            lines = [self.line_percentages, self.line_times]
            labels = [l.get_label() for l in lines]
            self.ax1.legend(lines, labels, loc='upper left')

            self.fig.suptitle('Training Progress')
            self.fig.tight_layout()
            self._plot_initialized = True
        else:
            # Update existing lines
            self.line_percentages.set_data(x, self.percentages)
            self.line_times.set_data(x, self.times)

            # Update limits
            self.ax1.set_xlim(1, len(self.percentages))
            # y-limits: keep 0-100 for percentages, autoscale time axis
            self.ax2.set_ylim(bottom=0, top=max(self.times) * 1.1 if self.times else 1)
            self.ax2.autoscale_view()


        # Redraw
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        plt.pause(0.001)