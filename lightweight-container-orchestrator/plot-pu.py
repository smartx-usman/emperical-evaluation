import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('mode.chained_assignment', None)

# Define experiment variables
workers = 1  # 1, 2, 3, 4, 5
run = 1
deployment = 'pod'  # 'pod' or 'deployment'
node = 'worker1'  # 'master1' or 'worker1'
color = 'Accent'

# Subplots layout
if node == 'master1':
    no_of_rows = 2
    no_of_cols = 4
    figure_width = 8.0
    figure_height = 5.0
else:
    no_of_rows = 2
    no_of_cols = 3
    figure_width = 8.0
    figure_height = 5.0

sharex = 'col'
sharey = 'row'
legend_columns = 1
#figure_width = 7.0  # for 4 rows
#figure_width = 5.0  # for 3 rows
#figure_height = 8.0 # for 4 rows
#figure_height = 6.0  # for 3 rows

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)



files_path = [f'k0s/pu_{workers}worker_{run}run',
              f'k3s/pu_{workers}worker_{run}run',
              f'microk8s/pu_{workers}worker_{run}run',
              f'microshift/pu_{workers}worker_{run}run']


def cpu_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
              set_y_label, label, color, services):
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

    print(stacked_df.head(5))

    my_plot_object.time_instance_stack_plot(df=stacked_df, axs_row=axs_row, axs_col=axs_col,
                                            title=title, x_label=x_label, y_label=y_label,
                                            y_lim_start=y_lim_start, y_lim_end=y_lim_end,
                                            legend_set=legend_set, legend_outside=False,
                                            set_x_label=set_x_label, set_y_label=set_y_label,
                                            color=color, services=services)


def memory_usage(input_file, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end, legend_set, set_x_label,
                 set_y_label, label, color, services):
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

    my_plot_object.time_instance_stack_plot(df=stacked_df, axs_row=axs_row, axs_col=axs_col,
                                            title=title, x_label=x_label, y_label=y_label,
                                            y_lim_start=y_lim_start, y_lim_end=y_lim_end,
                                            legend_set=legend_set, legend_outside=False,
                                            set_x_label=set_x_label, set_y_label=set_y_label,
                                            color=color, services=services)


def call_plot(path, distribution, color, services, function, axs_row, axs_col, legend, set_y_label=False):
    if function == 'cpu':
        if node == 'master1':
            y_lim_end = 100
        else:
            y_lim_end = 100
        cpu_usage(input_file=f'{path}/pu_cpu_{node}.csv', axs_row=axs_row, axs_col=axs_col,
                  title=f'{distribution}',
                  x_label="Time (sec)", y_label="CPU Usage (%)", y_lim_start=0, y_lim_end=y_lim_end,
                  legend_set=legend, set_x_label=True, set_y_label=set_y_label, label=distribution, color=color, services=services)

    if function == 'memory':
        if node == 'master1':
            y_lim_end = 4096
        else:
            y_lim_end = 2048
        memory_usage(input_file=f'{path}/pu_memory_{node}.csv', axs_row=axs_row, axs_col=axs_col,
                     title=f'',
                     x_label="Time (sec)", y_label="Memory Usage (MB)", y_lim_start=0, y_lim_end=y_lim_end,
                     legend_set=legend, set_x_label=True, set_y_label=set_y_label, label=distribution, color=color, services=services)


def process_data():
    if node == 'master1':
        distributions = ['K0s', 'K3s', 'Microk8s', 'Microshift']
    else:
        distributions = ['K0s', 'K3s', 'Microk8s']
    # microk8s_services = ['K8s-dqlite', 'Kubelite', 'Containerd', 'calico-node']
    # k0s_services = ['Etcd', 'Kube-apiserver', 'K0s', 'Kubelet', 'Containerd', 'calico-node']
    # k3s_services = ['k3s-server', 'k3s-agent', 'Containerd', 'flannel']
    # microshift_services = ['Microshift', 'Microshift-etcd', 'CRI-O', 'OVN-controller', 'OVNkube']

    if node == 'master1':
        k0s_services = ['etcd', 'kube-apiserver', 'k0s', 'calico-node']
        k3s_services = ['k3s-server']
        microk8s_services = ['k8s-dqlite', 'kubelite', 'calico-node']
        microshift_services = ['microshift', 'microshift-etcd', 'ovn-controller', 'ovnkube']
    else:
        k0s_services = ['kubelet', 'containerd', 'k0s', 'calico-node']
        k3s_services = ['k3s-agent', 'containerd']
        microk8s_services = ['kubelite', 'containerd', 'calico-node']
        microshift_services = ['Microshift', 'Microshift-etcd', 'CRI-O', 'OVN-controller', 'OVNkube']

    for distribution in distributions:
        if distribution == 'K0s':
            path = files_path[0]
            call_plot(path=path, distribution=distribution, color=color, services=k0s_services, function='cpu',
                      axs_row=0, axs_col=0, set_y_label=True, legend=True)
            call_plot(path=path, distribution=distribution, color=color, services=k0s_services, function='memory',
                      axs_row=1, axs_col=0, set_y_label=True, legend=False)
        elif distribution == 'K3s':
            path = files_path[1]
            call_plot(path=path, distribution=distribution, color=color, services=k3s_services, function='cpu',
                      axs_row=0, axs_col=1, legend=True)
            call_plot(path=path, distribution=distribution, color=color, services=k3s_services, function='memory',
                      axs_row=1, axs_col=1, legend=False)
        elif distribution == 'Microk8s':
            path = files_path[2]
            call_plot(path=path, distribution=distribution, color=color, services=microk8s_services, function='cpu',
                      axs_row=0, axs_col=2, legend=True)
            call_plot(path=path, distribution=distribution, color=color, services=microk8s_services, function='memory',
                      axs_row=1, axs_col=2, legend=False)

        elif distribution == 'Microshift':
            path = files_path[3]
            call_plot(path=path, distribution=distribution, color=color, services=microshift_services, function='cpu',
                      axs_row=0, axs_col=3, legend=True)
            call_plot(path=path, distribution=distribution, color=color, services=microshift_services,
                      function='memory',
                      axs_row=1, axs_col=3, legend=False)

        else:
            continue


process_data()
#plt.show()
plt.savefig(f'figures/pu_{deployment}_{workers}worker_{node}.png', dpi=600)
