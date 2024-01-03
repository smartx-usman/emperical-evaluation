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
legend_columns = 1
figure_width = 8.0  # inches
figure_height = 7.0  # inches

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)

# Define experiment variables
workers = 1  # 1, 2, 3, 4, 5
run = 1
deployment = 'pod'  # 'pod' or 'deployment'
node = 'master1'  # 'master1' or 'worker1'
color = 'tab20'

files_path = [f'k0s/pu_{workers}worker_{run}run',
              f'k3s/pu_{workers}worker_{run}run',
              f'microk8s/pu_{workers}worker_{run}run',
              f'microshift/pu_{workers}worker_{run}run']


def cpu_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
              label, color, services):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])

    # Concatenate DataFrames
    concatenated_df = pd.DataFrame()

    for service in services:
        df['value'] = df['cpu']

        df_app = df[df['command'] == service.lower()]

        if not df_app.empty:
            # Select specific columns and create a new DataFrame
            selected_columns = ['time', 'value', 'command']
            df_selected = df_app[selected_columns]

            # Group by "command" and "timestamp" columns and sum the "value" column
            result_df = df_selected.groupby(['command', 'time'])['value'].sum().reset_index()

            # Create an index column. Multiply index by 5 to convert to seconds
            result_df['index'] = range(len(result_df))  # Using range
            result_df['time_seconds'] = result_df["index"] * 5  # Time interval

            # Concatenate all the dataframes together
            concatenated_df = pd.concat([concatenated_df, result_df], ignore_index=True)

    # Create a DataFrame for stacked plot
    stacked_df = concatenated_df.pivot_table(index='time_seconds', columns='command', values='value',
                                             aggfunc='sum').fillna(0).cumsum(axis=1)

    my_plot_object.time_instance_stack_plot(df=stacked_df, axs_row=axs_row, axs_col=axs_col,
                                            title=title, x_label=x_label, y_label=y_label,
                                            y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set,
                                            set_x_label=set_x_label, color=color)


def memory_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
                 label, color, services):
    """Plot CPU Usage"""
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['timestamp'])

    # Concatenate DataFrames
    concatenated_df = pd.DataFrame()

    for service in services:
        df['value'] = (df['rss'] / 1000)
        df_app = df[df['command'] == service.lower()]

        if not df_app.empty:
            # Select specific columns and create a new DataFrame
            selected_columns = ['time', 'value', 'command']
            df_selected = df_app[selected_columns]

            # Group by "command" and "timestamp" columns and sum the "value" column
            result_df = df_selected.groupby(['command', 'time'])['value'].sum().reset_index()

            # Create an index column. Multiply index by 5 to convert to seconds
            result_df['index'] = range(len(result_df))  # Using range
            result_df['time_seconds'] = result_df["index"] * 5  # Time interval

            # Concatenate all the dataframes together
            concatenated_df = pd.concat([concatenated_df, result_df], ignore_index=True)

    # Create a DataFrame for stacked plot
    stacked_df = concatenated_df.pivot_table(index='time_seconds', columns='command', values='value',
                                             aggfunc='sum').fillna(0).cumsum(axis=1)

    #print(stacked_df.head(4))
    my_plot_object.time_instance_stack_plot(df=stacked_df, axs_row=axs_row, axs_col=axs_col,
                                            title=title, x_label=x_label, y_label=y_label,
                                            y_lim_start=y_lim_start, y_lim_end=y_lim_end, legend_set=legend_set,
                                            set_x_label=set_x_label, color=color)


def call_plot(path, distribution, color, services, function, axs_row, axs_col, legend):
    if function == 'cpu':
        cpu_usage(input_file=f'{path}/pu_cpu_{node}.csv', axs_row=axs_row, axs_col=axs_col,
                  title=f'{distribution} Services (CPU)',
                  x_label="Time (sec)", y_label="Usage (%)", y_lim_start=0, y_lim_end=60,
                  legend_set=legend, set_x_label=True, label=distribution, color=color, services=services)

    if function == 'memory':
        memory_usage(input_file=f'{path}/pu_memory_{node}.csv', axs_row=axs_row, axs_col=axs_col,
                     title=f'{distribution} Services (Memory)',
                     x_label="Time (sec)", y_label="Usage (MBytes)", y_lim_start=0, y_lim_end=4096,
                     legend_set=legend, set_x_label=True, label=distribution, color=color, services=services)


def process_data():
    # services = ['Etcd/K8s-dqlite', 'Kube-apiserver', 'Kubelet', 'Containerd']
    microk8s_services = ['K8s-dqlite', 'Kubelite', 'Containerd', 'calico-node']
    k0s_services = ['Etcd', 'Kube-apiserver', 'K0s', 'Kubelet', 'Containerd', 'calico-node']
    k3s_services = ['k3s-server', 'k3s-agent', 'Containerd', 'flannel']
    microshift_services = ['Microshift', 'Microshift-etcd', 'CRI-O', 'OVN-controller', 'OVNkube']

    for distribution in ('K0s', 'K3s', 'Microk8s', 'Microshift'):
        if distribution == 'K0s':
            path = files_path[0]
            call_plot(path=path, distribution=distribution, color=color, services=k0s_services, function='cpu',
                      axs_row=0, axs_col=0, legend=False)
            call_plot(path=path, distribution=distribution, color=color, services=k0s_services, function='memory',
                      axs_row=0, axs_col=1, legend=True)

        elif distribution == 'K3s':
            path = files_path[1]
            call_plot(path=path, distribution=distribution, color=color, services=k3s_services, function='cpu',
                      axs_row=1, axs_col=0, legend=False)
            call_plot(path=path, distribution=distribution, color=color, services=k3s_services, function='memory',
                      axs_row=1, axs_col=1, legend=True)
        elif distribution == 'Microk8s':
            path = files_path[2]
            call_plot(path=path, distribution=distribution, color=color, services=microk8s_services, function='cpu',
                      axs_row=2, axs_col=0, legend=False)
            call_plot(path=path, distribution=distribution, color=color, services=microk8s_services, function='memory',
                      axs_row=2, axs_col=1, legend=True)

        elif distribution == 'Microshift':
            path = files_path[3]
            call_plot(path=path, distribution=distribution, color=color, services=microshift_services, function='cpu',
                      axs_row=3, axs_col=0, legend=False)
            call_plot(path=path, distribution=distribution, color=color, services=microshift_services, function='memory',
                      axs_row=3, axs_col=1, legend=True)

        else:
            continue


process_data()

plt.savefig(f'figures/pu_{deployment}_{workers}worker_{node}.png', dpi=800)
