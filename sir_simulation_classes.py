import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix
from tqdm import tqdm
import time


class SIR(object):
    def __init__(self, params):
        self.params = params
        np.random.seed(params['random_state'])
        self.pop_df = self.initiate_pop_df()
        self.t = np.arange(0, self.params['n_days'], 1. / self.params['iter_per_day'])

    def initiate_pop_df(self):
        """
        Initiating the population DataFrame.
        This DataFrame should contain all the needed information about each person
        :return:
        """
        status_list = []
        for status, n_status in self.params['init_status'].items():
            status_list.extend([status] * n_status)

        pop_df = pd.DataFrame({'status': status_list})
        pop_df['pos_x'] = np.random.random(len(pop_df)) * self.params['map_size']
        pop_df['pos_y'] = np.random.random(len(pop_df)) * self.params['map_size']
        if self.params['I_init_pos'] is not None:
            pop_df.loc[pop_df.status == 'I', ['pos_x', 'pos_y']] = self.params['I_init_pos']
        pop_df['direction'] = np.random.random(len(pop_df)) * 2 * np.pi
        pop_df['status'] = pop_df['status']. \
            astype('category').cat.set_categories(self.params['init_status'].keys())
        pop_df['days_in_status'] = 0  # how many days have passed since entering the current status
        pop_df['is_isolated'] = False
        return pop_df

    def run_sim(self, real_time_plot=False,
                frame_delay=0.001, status_colors=None, display=None):
        """
        main method that run the simulation, gathers the outputs and optionally plots
        :return: list of outputs (an element per each iteration
        """
        if status_colors is None:
            status_colors = {'S': 'b', 'I': 'r', 'R': 'g'}
        outputs = [self.get_outputs(t=self.t[0])]
        if real_time_plot:
            fig, ax = plt.subplots()
            plt.axis('equal')
        else:
            fig = ax = None

        for t in tqdm(self.t[1:]):
            self.sir_iter()
            outputs.append(self.get_outputs(t=t))
            if real_time_plot:
                plt.cla()
                fig, ax = self.plot_pop_locations(self.pop_df, status_colors, t,
                                                  fig=fig, ax=ax, xlim=[0, self.params['map_size']],
                                                  ylim=[0, self.params['map_size']])
                if display is not None:
                    display.clear_output(wait=True)
                    display.display(fig)
                    time.sleep(frame_delay)
                else:
                    plt.pause(frame_delay)

        return outputs

    def sir_iter(self):
        """
        Run a single iteration
        :return:
        """
        self.test_and_isolate()
        self.update_locations()
        self.update_status()

    @staticmethod
    def plot_pop_locations(pop_df, status_colors, t, fig=None, ax=None,
                           xlim=None, ylim=None):
        if fig is None:
            fig, ax = plt.subplots()
        ax.cla()
        if xlim is not None:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        for status, c in status_colors.items():
            ax.scatter(pop_df[pop_df.status == status].pos_x,
                       pop_df[pop_df.status == status].pos_y, c=c,
                       s=pop_df[pop_df.status == status].days_in_status, label=status)
        ax.plot(pop_df[pop_df.is_isolated].pos_x,
                pop_df[pop_df.is_isolated].pos_y, 'kx', label='isolated')
        ax.legend(loc=4)
        ax.set_title(f't = {t:.2f} [days]')
        return fig, ax

    def update_status(self):
        """
        Update the "status" and "days_in_status" columns of the DataFrame
        :return:
        """
        self.pop_df['days_in_status'] = \
            self.pop_df['days_in_status'] + 1 / self.params['iter_per_day']
        self.infect()
        self.remove()

    def infect(self):
        """
        Move people from 'S' to 'I' status
        :return:
        """
        # todo: find more efficient way to find nearest neighbor distance (consider using scipy.spatial.KDTree)
        i_and_not_isolated = (self.pop_df.status == 'I') & (~self.pop_df.is_isolated)
        s_and_not_isolated = (self.pop_df.status == 'S') & (~self.pop_df.is_isolated)
        i_pos = self.pop_df.loc[i_and_not_isolated, ['pos_x', 'pos_y']].values
        s_pos = self.pop_df.loc[s_and_not_isolated, ['pos_x', 'pos_y']].values
        dist_arr = distance_matrix(i_pos, s_pos)
        is_infected = np.any(dist_arr < self.params['infection_radius'], axis=0)
        infected_idx = s_and_not_isolated[s_and_not_isolated].index[is_infected]
        self.pop_df.loc[infected_idx, 'status'] = 'I'
        self.pop_df.loc[infected_idx, 'days_in_status'] = 0

    def remove(self):
        """
        Move people from 'I' to 'R' status
        :return:
        """
        # is_remove = (self.pop_df.status == 'I') & \
        #             (self.pop_df.days_in_status > self.params['infection_duration'])
        is_remove = (self.pop_df.status == 'I') & \
                    (np.random.random(len(self.pop_df)) < 1 / (self.params['infection_duration'] *
                                                               self.params['iter_per_day']))

        self.pop_df.loc[is_remove, 'status'] = 'R'
        self.pop_df.loc[is_remove, 'days_in_status'] = 0

    def test_and_isolate(self):
        """
        Sample the population for testing and isolate according to some rule.
        This should be a central part of the research
        :return:
        """
        # Sample random people and isolate the infected (assume the test accuracy is perfect)
        # todo: add FN and FP
        tested_df = self.pop_df.sample(round(self.params['tests_per_day'] / self.params['iter_per_day']))
        # notice the rounding might change the tests_per_day (negligible in large numbers)
        tested_positive_idx = tested_df[tested_df.status == 'I'].index
        self.pop_df.loc[tested_positive_idx, 'is_isolated'] = True

    def update_locations(self):
        # step_direction = np.random.random(len(self.pop_df)) * 2 * np.pi
        step_direction = self.pop_df.direction
        self.pop_df['pos_x'] = self.pop_df['pos_x'] + np.sin(step_direction) * self.params['step_size_iter']
        self.pop_df['pos_y'] = self.pop_df['pos_y'] + np.cos(step_direction) * self.params['step_size_iter']
        self.pop_df['pos_x'] = np.mod(self.pop_df['pos_x'], self.params['map_size'])
        self.pop_df['pos_y'] = np.mod(self.pop_df['pos_y'], self.params['map_size'])
        # todo: add boundaries to the map and avoid stepping outside of them

    def get_outputs(self, **kwargs):
        """
        Extract a dictionary of outputs from the DataFrame
        :return: dict
        """
        output = self.pop_df.status.value_counts().to_dict()
        output.update(kwargs)
        return output


def main():
    params = {
        'n_days': 60,
        'iter_per_day': 4,
        'init_status': {'S': 500, 'I': 10, 'R': 0},
        'I_init_pos': [500, 500],  # if None, infected people are randomly spread
        'map_size': 1000,
        'step_size_iter': 10,
        'random_state': 42,
        'infection_radius': 40,
        'infection_duration': 20,
        'tests_per_day': 510
    }
    sir = SIR(params)
    outputs = sir.run_sim(real_time_plot=True, frame_delay=0.000001)
    plt.figure().show()
    outputs_df = pd.DataFrame(outputs)
    plt.plot(outputs_df.t, outputs_df[list(params['init_status'].keys())])
    return outputs


if __name__ == '__main__':
    main()
