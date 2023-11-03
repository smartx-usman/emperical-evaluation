import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('mode.chained_assignment', None)

# Subplots layout
no_of_rows = 4
no_of_cols = 2
sharex = 'col'
sharey = 'none'
legend_columns = 4
figure_width = 8.0  # inches
figure_height = 6.5  # inches

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)


def cpu_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
              label, color, service):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])

    df['value'] = df['cpu']
    df_app = df[df['command'] == service.lower()]

    # Select specific columns and create a new DataFrame
    selected_columns = ['time', 'value', 'command']
    df_selected = df_app[selected_columns]

    # Group by "command" and "timestamp" columns and sum the "value" column
    result_df = df_selected.groupby(['command', 'time'])['value'].sum().reset_index()
    print(df_selected.head(10))
    print(result_df.head(10))

    # Create an index column. Multiply index by 5 to convert to seconds
    result_df['index'] = range(len(result_df))  # Using range
    result_df['time_seconds'] = result_df["index"] * 5  # Time interval

    my_plot_object.time_instance_plot(df=result_df, x_col="time_seconds", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
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

    # Select specific columns and create a new DataFrame
    selected_columns = ['time', 'value', 'command']
    df_selected = df_app[selected_columns]

    # Group by "command" and "timestamp" columns and sum the "value" column
    result_df = df_selected.groupby(['command', 'time'])['value'].sum().reset_index()

    # Create an index column. Multiply index by 5 to convert to seconds
    result_df['index'] = range(len(result_df))  # Using range
    result_df['time_seconds'] = result_df["index"] * 5  # Time interval

    my_plot_object.time_instance_plot(df=result_df, x_col="time_seconds", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                                 title=title, x_label=x_label, y_label=y_label,
                                 y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set,
                                 set_x_label=set_x_label, color=color)


def process_data():
    #services = ['Etcd/K8s-dqlite', 'Kube-apiserver', 'Kubelet', 'Containerd']
    microk8s_services = ['K8s-dqlite', 'Kubelite', 'Kubelite', 'Containerd', 'calico-node']
    k0s_services = ['Etcd', 'Kube-apiserver', 'Kubelet', 'Containerd']
    k3s_services = ['Etcd', 'Kube-apiserver', 'Kubelet', 'Containerd']
    openshift_services = ['Etcd', 'Kube-apiserver', 'Kubelet', 'Containerd']

    for distribution in ('Microk8s', 'abc'):
        if distribution == 'Microk8s':
            color = 'tab:blue'
            path = files_path[0]
            call_plot(path=path, distribution=distribution, color=color, services=microk8s_services)

        elif distribution == 'K0s':
            color = 'tab:orange'
            path = files_path[1]

            call_plot(path=path, distribution=distribution, color=color, services=k0s_services)

        elif distribution == 'K3s':
            color = 'tab:gray'

        elif distribution == 'OpenShift':
            color = 'tab:olive'

        else:
            continue


def call_plot(path, distribution, color, services):
    cpu_usage(input_file=f'{path}/pu_cpu_master.csv', axs_row=0, axs_col=0,
              title=f'Store Service (CPU)',
              x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=15, legend_set=False,
              set_x_label=True, label=distribution, color=color, service=services[0])

    memory_usage(input_file=f'{path}/pu_memory_master.csv', axs_row=0, axs_col=1,
                 title=f'Store Service (Memory)',
                 x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=900,
                 legend_set=False, set_x_label=True, label=distribution, color=color, service=services[0])

    cpu_usage(input_file=f'{path}/pu_cpu_master.csv', axs_row=1, axs_col=0,
              title=f'API Service (CPU)',
              x_label="Timestamp", y_label="Usage (%)", y_lim_start=0, y_lim_end=25, legend_set=False,
              set_x_label=True, label=distribution, color=color, service=services[1])

    memory_usage(input_file=f'{path}/pu_memory_master.csv', axs_row=1, axs_col=1,
                 title=f'API Service (Memory)',
                 x_label="Timestamp", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=1000,
                 legend_set=False, set_x_label=True, label=distribution, color=color, service=services[1])

    cpu_usage(input_file=f'{path}/pu_cpu_worker1.csv', axs_row=2, axs_col=0,
              title=f'{services[2]} Service (CPU)',
              x_label="Timestamp (sec)", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
              set_x_label=True, label=distribution, color=color, service=services[2])

    memory_usage(input_file=f'{path}/pu_memory_worker1.csv', axs_row=2, axs_col=1,
                 title=f'{services[2]} Service (Memory)',
                 x_label="Timestamp (sec)", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=256,
                 legend_set=False, set_x_label=True, label=distribution, color=color, service=services[2])

    cpu_usage(input_file=f'{path}/pu_cpu_worker1.csv', axs_row=3, axs_col=0,
              title=f'{services[3]} Service (CPU)',
              x_label="Timestamp (sec)", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
              set_x_label=True, label=distribution, color=color, service=services[3])

    memory_usage(input_file=f'{path}/pu_memory_worker1.csv', axs_row=3, axs_col=1,
                 title=f'{services[3]} Service (Memory)',
                 x_label="Timestamp (sec)", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=256,
                 legend_set=True, set_x_label=True, label=distribution, color=color, service=services[3])

    # cpu_usage(input_file=f'{path}/pu_cpu_master.csv', axs_row=4, axs_col=0,
    #           title=f'Network Service (CPU)',
    #           x_label="Timestamp (sec)", y_label="Usage (%)", y_lim_start=0, y_lim_end=10, legend_set=False,
    #           set_x_label=True, label=distribution, color=color, service=services[4])
    #
    # memory_usage(input_file=f'{path}/pu_memory_master.csv', axs_row=4, axs_col=1,
    #              title=f'Network Service (Memory)',
    #              x_label="Timestamp (sec)", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=900,
    #              legend_set=False, set_x_label=True, label=distribution, color=color, service=services[4])


# Define variables
workers = 3  # 1, 2, 3, 4, 5
replicas = 3  # 1, 3
run = 1
deployment = 'pod'  # 'pod' or 'deployment'
files_path = [f'microk8s/pu_{workers}worker_{run}run', f'k0s/pu_{workers}worker_{run}run']

process_data()

plt.savefig(f'figures/pu_{deployment}_{workers}worker.png', dpi=800)
