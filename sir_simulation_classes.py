import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix
from tqdm import tqdm


class SIR(object):
    def __init__(self, params):
        self.params = params
        np.random.seed(params['random_state'])
        self.pop_df = self.initiate_pop_df()
        self.t = np.arange(0, self.params['n_days'], 1./self.params['iter_per_day'])

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
        pop_df['direction'] = np.random.random(len(pop_df)) * 2 * np.pi
        pop_df['status'] = pop_df['status'].\
            astype('category').cat.set_categories(self.params['init_status'].keys())
        pop_df['days_in_status'] = 0  # how many days have passed since entering the current status
        pop_df['is_isolated'] = False
        return pop_df

    def run_sim(self, real_time_plot=False, frame_delay=0.001, status_colors=None):
        """
        main method that run the simulation, gathers the outputs and optionally plots
        :return: list of outputs (an element per each iteration
        """
        if status_colors is None:
            status_colors = {'S': 'b', 'I': 'r', 'R': 'g'}
        outputs = [self.get_outputs()]
        if real_time_plot:
            fig = plt.figure()
            fig.show()
        for _ in tqdm(self.t[1:]):
            self.sir_iter()
            outputs.append(self.get_outputs())
            if real_time_plot:
                plt.cla()
                plt.xlim(0, self.params['map_size'])
                plt.ylim(0, self.params['map_size'])
                self.plot_pop_locations(self.pop_df, status_colors, fig=fig)
                plt.pause(frame_delay)

        return outputs

    def sir_iter(self):
        """
        Run a single iteration
        :return:
        """
        self.update_locations()
        self.update_status()
        self.test_and_isolate()

    @staticmethod
    def plot_pop_locations(pop_df, status_colors, fig=None):
        if fig is None:
            fig = plt.figure()
        for status, c in status_colors.items():
            plt.scatter(pop_df[pop_df.status == status].pos_x,
                        pop_df[pop_df.status == status].pos_y, c=c,
                        s=pop_df[pop_df.status == status].days_in_status, label=status)
        plt.legend(loc=4)
        return fig

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
        # todo: take into account isolation
        # todo: find more efficient way to find nearest neighbor distance (consider using scipy.spatial.KDTree)
        dist_arr = distance_matrix(self.pop_df[['pos_x', 'pos_y']].values,
                                   self.pop_df[['pos_x', 'pos_y']].values)
        np.fill_diagonal(dist_arr, np.nan)
        is_infected = np.any(dist_arr < self.params['infection_radius'], axis=1)
        new_infections = is_infected & (self.pop_df.status == 'S')
        self.pop_df.loc[new_infections, 'status'] = 'I'
        self.pop_df.loc[new_infections, 'days_in_status'] = 0

    def remove(self):
        """
        Move people from 'I' to 'R' status
        :return:
        """
        # is_remove = (self.pop_df.status == 'I') & \
        #             (self.pop_df.days_in_status > self.params['infection_duration'])
        is_remove = (self.pop_df.status == 'I') & \
                    (np.random.random(len(self.pop_df)) < 1/(self.params['infection_duration'] *
                                                             self.params['iter_per_day']))

        self.pop_df.loc[is_remove, 'status'] = 'R'

    def test_and_isolate(self):
        """
        Sample the population for testing and isolate according to some rule.
        This should be a central part of the research
        :return:
        """
        pass

    def update_locations(self):
        step_direction = np.random.random(len(self.pop_df)) * 2 * np.pi
        self.pop_df['pos_x'] = self.pop_df['pos_x'] + np.sin(step_direction) * self.params['step_size_iter']
        self.pop_df['pos_y'] = self.pop_df['pos_y'] + np.cos(step_direction) * self.params['step_size_iter']
        self.pop_df['pos_x'] = np.mod(self.pop_df['pos_x'], self.params['map_size'])
        self.pop_df['pos_y'] = np.mod(self.pop_df['pos_y'], self.params['map_size'])
        # todo: add boundaries to the map and avoid stepping outside of them

    def get_outputs(self):
        """
        Extract a dictionary of outputs from the DataFrame
        :return: dict
        """
        return self.pop_df.status.value_counts().to_dict()


def main():
    params = {
        'n_days': 30,
        'iter_per_day': 4,
        'init_status': {'S': 1000, 'I': 10, 'R': 0},
        'map_size': 10000,
        'step_size_iter': 100,
        'random_state': 42,
        'infection_radius': 20,
        'infection_duration': 10
    }
    sir = SIR(params)
    outputs = sir.run_sim(real_time_plot=True, frame_delay=0.000001)
    # SIR.plot_pop_locations(sir.pop_df).show()
    plt.figure().show()
    plt.plot(sir.t, pd.DataFrame(outputs))
    return outputs


if __name__ == '__main__':
    main()
