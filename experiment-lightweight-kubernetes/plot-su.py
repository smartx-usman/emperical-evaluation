import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Subplots layout
no_of_rows = 3
no_of_cols = 4
# sharex = 'col'
sharex = 'none'
sharey = 'none'
legend_columns = 4
figure_width = 8.0  # inches
#figure_height = 4.0  # inches for single row charts
#figure_height = 6.0  # inches for two row charts
figure_height = 7.0  # inches for four row charts

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)


def cpu_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
              label, color):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', origin='unix')
    df['value'] = (100 - df['idle'])

    print(df.dtypes)

    # for node in ('worker1', 'worker2', 'observability1'):
    #    df_app = df[df['host'] == node]
    #    df_final = df_app[["timestamp", "host", "value"]]

    #    print(df_final.head(2))
    #    print(len(df_app))

    my_plot_object.timeline_plot(df=df, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                title=title, x_label=x_label, y_label=y_label,
                y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set, set_x_label=set_x_label, color=color)


def memory_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
                 label, color):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', origin='unix')
    df['value'] = (df['kbmemused'] / 1000)

    print(df.dtypes)

    my_plot_object.timeline_plot(df=df, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                title=title, x_label=x_label, y_label=y_label,
                y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set, set_x_label=set_x_label, color=color)


def disk_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
               label, color):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    df['value'] = (df['p_util'])

    print(df.dtypes)

    my_plot_object.timeline_plot(df=df, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                title=title, x_label=x_label, y_label=y_label,
                y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set, set_x_label=set_x_label, color=color)


def network_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set,
                  set_x_label, label, color):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])
    df['value'] = (df['rxkB/s'])

    print(df.dtypes)

    my_plot_object.timeline_plot(df=df, x_col="time", y_col="value", label=label, axs_row=axs_row, axs_col=axs_col,
                title=title, x_label=x_label, y_label=y_label,
                y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set, set_x_label=set_x_label, color=color)


def process_node_data():
    for node in ('master', 'worker1', 'worker2', 'worker3'):
        if node == 'master':
            color = 'tab:blue'
            cpu_usage(input_file=f'{files_path}/output_su_{node}_2.csv', axs_row=0, axs_col=0, title="",
                      x_label="Timestamp", y_label="CPU Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=False, label=node, color=color)

            memory_usage(input_file=f'{files_path}/output_su_{node}_4.csv', axs_row=0, axs_col=1, title="",
                         x_label="Timestamp", y_label="Memory Usage (MBytes)", y_lim_start=0, y_lim_end=2400,
                         legend_set=False,
                         set_x_label=False, label=node, color=color)

            disk_usage(input_file=f'{files_path}/output_su_{node}_6.csv', axs_row=0, axs_col=2, title="",
                       x_label="Timestamp", y_label="Disk Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=False, label=node, color=color)

            network_usage(input_file=f'{files_path}/output_su_{node}_0.csv', axs_row=0, axs_col=3, title="",
                          x_label="Timestamp", y_label="Network Usage (Rx KBytes/s)", y_lim_start=0, y_lim_end=1000,
                          legend_set=True,
                          set_x_label=False, label=node, color=color)
        elif node == 'worker1':
            color = 'tab:orange'
            cpu_usage(input_file=f'{files_path}/output_su_{node}_2.csv', axs_row=1, axs_col=0,
                      title="",
                      x_label="Timestamp", y_label="CPU Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=False, label=node, color=color)

            memory_usage(input_file=f'{files_path}/output_su_{node}_4.csv', axs_row=1, axs_col=1,
                         title="",
                         x_label="Timestamp", y_label="Memory Usage (MBytes)", y_lim_start=0, y_lim_end=2048,
                         legend_set=False,
                         set_x_label=False, label=node, color=color)

            disk_usage(input_file=f'{files_path}/output_su_{node}_6.csv', axs_row=1, axs_col=2,
                       title="",
                       x_label="Timestamp", y_label="Disk Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=False, label=node, color=color)

            network_usage(input_file=f'{files_path}/output_su_{node}_0.csv', axs_row=1, axs_col=3,
                          title="",
                          x_label="Timestamp", y_label="Network Usage (Rx KBytes/s)", y_lim_start=0, y_lim_end=1000,
                          legend_set=True,
                          set_x_label=False, label=node, color=color)
        elif node == 'worker2':
            color = 'tab:gray'
            cpu_usage(input_file=f'{files_path}/output_su_{node}_2.csv', axs_row=1, axs_col=0,
                      title="",
                      x_label="Timestamp", y_label="CPU Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=False, label=node, color=color)

            memory_usage(input_file=f'{files_path}/output_su_{node}_4.csv', axs_row=1, axs_col=1,
                         title="",
                         x_label="Timestamp", y_label="Memory Usage (MBytes)", y_lim_start=0, y_lim_end=2048,
                         legend_set=False,
                         set_x_label=False, label=node, color=color)

            disk_usage(input_file=f'{files_path}/output_su_{node}_6.csv', axs_row=1, axs_col=2,
                       title="",
                       x_label="Timestamp", y_label="Disk Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=False, label=node, color=color)

            network_usage(input_file=f'{files_path}/output_su_{node}_0.csv', axs_row=1, axs_col=3,
                          title="",
                          x_label="Timestamp", y_label="Network Usage (Rx KBytes/s)", y_lim_start=0, y_lim_end=1000,
                          legend_set=True,
                          set_x_label=False, label=node, color=color)
        elif node == 'worker3':
            color = 'tab:olive'
            cpu_usage(input_file=f'{files_path}/output_su_{node}_2.csv', axs_row=1, axs_col=0,
                      title="",
                      x_label="Timestamp", y_label="CPU Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=False, label=node, color=color)

            memory_usage(input_file=f'{files_path}/output_su_{node}_4.csv', axs_row=1, axs_col=1,
                         title="",
                         x_label="Timestamp", y_label="Memory Usage (MBytes)", y_lim_start=0, y_lim_end=2048,
                         legend_set=False,
                         set_x_label=False, label=node, color=color)

            disk_usage(input_file=f'{files_path}/output_su_{node}_6.csv', axs_row=1, axs_col=2,
                       title="",
                       x_label="Timestamp", y_label="Disk Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=False, label=node, color=color)

            network_usage(input_file=f'{files_path}/output_su_{node}_0.csv', axs_row=1, axs_col=3,
                          title="",
                          x_label="Timestamp", y_label="Network Usage (Rx KBytes/s)", y_lim_start=0, y_lim_end=1000,
                          legend_set=True,
                          set_x_label=False, label=node, color=color)
        elif node == 'simulation1':
            color = 'tab:cyan'
            cpu_usage(input_file=f'{files_path}/output_su_{node}_2.csv', axs_row=1, axs_col=0,
                      title="",
                      x_label="Timestamp", y_label="CPU Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=False, label=node, color=color)

            memory_usage(input_file=f'{files_path}/output_su_{node}_4.csv', axs_row=1, axs_col=1,
                         title="",
                         x_label="Timestamp", y_label="Memory Usage (MBytes)", y_lim_start=0, y_lim_end=2048,
                         legend_set=False,
                         set_x_label=False, label=node, color=color)

            disk_usage(input_file=f'{files_path}/output_su_{node}_6.csv', axs_row=1, axs_col=2,
                       title="",
                       x_label="Timestamp", y_label="Disk Usage (Percent)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=False, label=node, color=color)

            network_usage(input_file=f'{files_path}/output_su_{node}_0.csv', axs_row=1, axs_col=3,
                          title="",
                          x_label="Timestamp", y_label="Network Usage (Rx KBytes/s)", y_lim_start=0, y_lim_end=1000,
                          legend_set=True,
                          set_x_label=False, label=node, color=color)
        else:
            continue


def process_distribution_data(node_id):
    #for distribution in ('Microk8s', 'K0s', 'K3s', 'Openshift'):
    for distribution in ('Microk8s', 'K0s', 'K3s'):
        if distribution == 'Microk8s':
            color = 'tab:blue'
            path = files_path[0]
            axs_row = 0
        elif distribution == 'K0s':
            color = 'tab:orange'
            path = files_path[1]
            axs_row = 1
        elif distribution == 'K3s':
            color = 'tab:gray'
            path = files_path[2]
            axs_row = 2
        elif distribution == 'OpenShift':
            color = 'tab:olive'
            path = files_path[3]
            axs_row = 3
        else:
            continue

        if node_id == 'workers':
            color = ''
            for node in ('worker1', 'worker2', 'worker3'):
                cpu_usage(input_file=f'{path}/output_su_{node}_2.csv', axs_row=axs_row, axs_col=0, title="",
                          x_label="Timestamp", y_label="CPU (%)", y_lim_start=0, y_lim_end=100, legend_set=False,
                          set_x_label=True, label=f'{distribution}-{node}', color=color)

                memory_usage(input_file=f'{path}/output_su_{node}_4.csv', axs_row=axs_row, axs_col=1, title="",
                             x_label="Timestamp", y_label="Memory (MBytes)", y_lim_start=0, y_lim_end=2048,
                             legend_set=False,
                             set_x_label=True, label=f'{distribution}-{node}', color=color)

                disk_usage(input_file=f'{path}/output_su_{node}_6.csv', axs_row=axs_row, axs_col=2, title="",
                           x_label="Timestamp", y_label="Disk (%)", y_lim_start=0, y_lim_end=100, legend_set=False,
                           set_x_label=True, label=f'{distribution}-{node}', color=color)

                network_usage(input_file=f'{path}/output_su_{node}_0.csv', axs_row=axs_row, axs_col=3, title="",
                              x_label="Timestamp", y_label="Net (Rx KBytes/s)", y_lim_start=0, y_lim_end=1500,
                              legend_set=True,
                              set_x_label=True, label=f'{distribution}-{node}', color=color)
        else:
            cpu_usage(input_file=f'{path}/output_su_{node_id}_2.csv', axs_row=axs_row, axs_col=0, title="",
                      x_label="Timestamp", y_label="CPU (%)", y_lim_start=0, y_lim_end=100, legend_set=False,
                      set_x_label=True, label=distribution, color=color)

            memory_usage(input_file=f'{path}/output_su_{node_id}_4.csv', axs_row=axs_row, axs_col=1, title="",
                         x_label="Timestamp", y_label="Memory (MBytes)", y_lim_start=0, y_lim_end=3500,
                         legend_set=False,
                         set_x_label=True, label=distribution, color=color)

            disk_usage(input_file=f'{path}/output_su_{node_id}_6.csv', axs_row=axs_row, axs_col=2, title="",
                       x_label="Timestamp", y_label="Disk (%)", y_lim_start=0, y_lim_end=100, legend_set=False,
                       set_x_label=True, label=distribution, color=color)

            network_usage(input_file=f'{path}/output_su_{node_id}_0.csv', axs_row=axs_row, axs_col=3, title="",
                          x_label="Timestamp", y_label="Net (Rx KBytes/s)", y_lim_start=0, y_lim_end=1500,
                          legend_set=True,
                          set_x_label=True, label=distribution, color=color)


# Define variables
deployment = 'deployment'  # 'pod' or 'deployment'
workers = 3  # 1, 2, 3, 4, 5
replicas = 1  # 1, 3
run = 3  # 1, 3

#distribution = 'k0s'  # 'baseline' or 'microk8s' or 'k0s' or 'k3s' or 'openshift'
#files_path = f'microk8s/{deployment}_{workers}worker_{run}run'
#files_path = f'k0s/dp_{replicas}replica_{workers}worker'
#files_path = f'k0s/{deployment}_{workers}worker_{run}run'
# process_node_data()

#for node in ('master', 'worker1'):
node = 'master'  # master or worker1 or workers
files_path = [f'microk8s/{deployment}_{workers}worker_{run}run',
              f'k0s/{deployment}_{workers}worker_{run}run',
              f'k3s/{deployment}_{workers}worker_{run}run',
              f'openshift/{deployment}_{workers}worker_{run}run']

process_distribution_data(node)
plt.savefig(f'figures/su_{deployment}_{workers}worker_{run}run_{node}.png', dpi=800)

# Define baseline values
# baseline_cpu = 0.3  # Example baseline CPU usage percentage
# baseline_memory = 134  # Example baseline memory usage percentage
# baseline_disk = 0.38  # Example baseline disk usage percentage
# baseline_network = 0.05  # Example baseline network usage (KB/s)
# axs[0, 0].axhline(y=baseline_cpu, color='r', linestyle='--', label='CPU Baseline')
# axs[0, 1].axhline(y=baseline_memory, color='g', linestyle='--', label='Memory Baseline')
# axs[1, 0].axhline(y=baseline_disk, color='b', linestyle='--', label='Disk Baseline')
# axs[1, 1].axhline(y=baseline_network, color='purple', linestyle='--', label='Network Baseline')

#plt.savefig(f'figures/su_dp_{workers}worker_{replicas}replica_latency_{distribution}.png', dpi=800)
#plt.savefig(f'figures/su_dp_{workers}worker_{replicas}replica_latency_{distribution}.png', dpi=800)
