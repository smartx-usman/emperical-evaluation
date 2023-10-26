import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

plt.rcParams["figure.figsize"] = [8.0, 6.5]
plt.rcParams["figure.autolayout"] = True

# Subplots layout
no_of_rows = 4
no_of_cols = 2
sharex = 'col'
sharey = 'none'
legend_columns = 4
figure_width = 8.0  # inches
figure_height = 5.5  # inches

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)


def cpu_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
              label, color, service):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    df['value'] = df['cpu']
    df_app = df[df['command'] == service.lower()]

    my_plot_object.timeline_plot(df=df_app, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                                 title=title, x_label=x_label, y_label=y_label,
                                 y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set,
                                 set_x_label=set_x_label, color=color)


def memory_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
                 label, color, service):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    df['value'] = (df['rss'] / 1000)
    df_app = df[df['command'] == service.lower()]

    my_plot_object.timeline_plot(df=df_app, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                                 title=title, x_label=x_label, y_label=y_label,
                                 y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set,
                                 set_x_label=set_x_label, color=color)


def process_data():
    services = ['Etcd', 'Kube-apiserver', 'Kubelet', 'Containerd']
    for distribution in ('Microk8s', 'K0s'):
        if distribution == 'Microk8s':
            color = 'tab:blue'

        elif distribution == 'K0s':
            color = 'tab:orange'
            path = files_path[0]

        elif distribution == 'K3s':
            color = 'tab:gray'

        elif distribution == 'OpenShift':
            color = 'tab:olive'

        else:
            continue

        cpu_usage(input_file=f'{path}/pu_cpu_master.csv', axs_row=0, axs_col=0, title=f'{services[0]} Service (CPU)',
                  x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
                  set_x_label=True, label=distribution, color=color, service=services[0])

        memory_usage(input_file=f'{path}/pu_memory_master.csv', axs_row=0, axs_col=1,
                     title=f'{services[0]} Service (Memory)',
                     x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=512,
                     legend_set=True, set_x_label=True, label=distribution, color=color, service=services[0])

        cpu_usage(input_file=f'{path}/pu_cpu_master.csv', axs_row=1, axs_col=0, title=f'{services[1]} Service (CPU)',
                  x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
                  set_x_label=True, label=distribution, color=color, service=services[1])

        memory_usage(input_file=f'{path}/pu_memory_master.csv', axs_row=1, axs_col=1,
                     title=f'{services[1]} Service (Memory)',
                     x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=512,
                     legend_set=False, set_x_label=True, label=distribution, color=color, service=services[1])

        cpu_usage(input_file=f'{path}/pu_cpu_worker1.csv', axs_row=2, axs_col=0, title=f'{services[2]} Service (CPU)',
                  x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
                  set_x_label=True, label=distribution, color=color, service=services[2])

        memory_usage(input_file=f'{path}/pu_memory_worker1.csv', axs_row=2, axs_col=1,
                     title=f'{services[2]} Service (Memory)',
                     x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=512,
                     legend_set=True, set_x_label=True, label=distribution, color=color, service=services[2])

        cpu_usage(input_file=f'{path}/pu_cpu_worker1.csv', axs_row=3, axs_col=0, title=f'{services[3]} Service (CPU)',
                  x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
                  set_x_label=True, label=distribution, color=color, service=services[3])

        memory_usage(input_file=f'{path}/pu_memory_worker1.csv', axs_row=3, axs_col=1,
                     title=f'{services[3]} Service (Memory)',
                     x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=512,
                     legend_set=False, set_x_label=True, label=distribution, color=color, service=services[3])


# Define variables
workers = 1  # 1, 2, 3, 4, 5
replicas = 3  # 1, 3
deployment = 'pod'  # 'pod' or 'deployment'
files_path = [f'microk8s/pu_{workers}worker_3run', f'k0s/pu_{workers}worker_3run']

process_data()

plt.savefig(f'figures/pu_{deployment}_{workers}worker.png', dpi=800)
