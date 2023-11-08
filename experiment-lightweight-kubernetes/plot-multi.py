import sys

import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Subplots layout
no_of_rows = 1
no_of_cols = 1
sharex = 'none'
sharey = 'none'
legend_columns = 2
figure_width = 8.0  # inches
figure_height = 4.0  # inches for single row charts
#figure_height = 6.0  # inches for two row charts
#figure_height = 5.0  # inches
#figure_height = 5.5  # inches


# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)


def seaborn_bar_plot_process():
    data_deployment = []
    data_rest = []

    latency_data_1replica = []
    throughput_data_1replica = []
    latency_data_3replica = []
    throughput_data_3replica = []

    if deployment == 'deployment':
        metrics = ['Median', 'Min', 'Max']
        #k8s_distributions = ['Microk8s', 'K0s', 'K3s', 'Openshift']
        k8s_distributions = ['Microk8s', 'K0s']
        operations_dep = ['create', 'list', 'update', 'scale', 'delete']
        data_deployment_values = [
            # Microk8s deployment API latency results (median, min, max)
            324.59, 66.11, 674.39, 4.79, 2.74, 55.72, 126.54, 16.25, 1154.42, 977.63, 77.24, 1743.81, 725.59, 403.09, 1980.99,
            # k0s deployment API latency results (median, min, max)
            74.524, 39.63, 351.01, 27.04, 2.49, 100.2, 55.98, 8.73, 114.37, 513.29, 9.30, 927.79, 12.25, 4.95, 993.11,
            # k3s deployment API latency results (median, min, max)
            400.87, 69.06, 700.09, 7.42, 2.19, 11.47, 84.5, 11.47, 988.61, 824.18, 97.72, 1284.52, 619.14, 214.00,
            1523.73,
            # Openshift deployment API latency results (median, min, max)
            250.87, 69.06, 620.09, 7.42, 2.19, 11.47, 84.5, 11.47, 988.61, 824.18, 97.72, 1284.52, 619.14, 214.00,
            1000.73
        ]
        pos = 0

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            for operation in operations_dep:
                for metric in metrics:
                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Operation': operation,
                        'Metric': metric,
                        'Value': data_deployment_values[pos]  # You can set the initial value as needed
                    }
                    # Append the dictionary to the list
                    data_deployment.append(data_dict)
                    pos += 1

    if deployment == 'other':
        metrics = ['Median', 'Min', 'Max']
        #k8s_distributions = ['Microk8s', 'K0s', 'K3s', 'Openshift']
        k8s_distributions = ['Microk8s', 'K0s', 'K3s']
        operations_rest = ['Namespace', 'Service', 'PV', 'PVC']
        data_rest_values = [
            # Microk8s deployment API latency results (median, min, max)
            4.59, 1.61, 6.68, 10.84, 1.41, 17.58, 4.33, 0.81, 6.70, 2.75, 0.48, 5.83,
            # k0s deployment API latency results (median, min, max)
            2.13, 1.58, 2.55, 6.89, 0.39, 13.24, 0.73, 0.14, 0.77, 0.62, 0.19, 1.12,
            # k3s deployment API latency results (median, min, max)
            1.28, 0.36, 1.96, 3.07, 0.52, 5.41, 0.47, 0.39, 0.86, 0.67, 0.23, 1.12,
            # Openshift deployment API latency results (median, min, max)
            250.872, 69.064, 620.099, 14.427, 8.191, 20.473, 200.5, 50.473, 700.618
        ]
        pos = 0

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            for operation in operations_rest:
                for metric in metrics:
                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Operation': operation,
                        'Metric': metric,
                        'Value': data_rest_values[pos]  # You can set the initial value as needed
                    }
                    # Append the dictionary to the list
                    data_rest.append(data_dict)
                    pos += 1

    if deployment == 'baseline':
        k8s_distributions = ['Baseline', 'Microk8s', 'K0s', 'K3s', 'Openshift']
        k8s_distributions = ['Baseline', 'Microk8s', 'K0s', 'K3s']
        cluster_nodes = ['master', 'worker1', 'worker2', 'worker3']
        metrics = ['CPU', 'Memory', 'Disk', 'Network']

        cpu_data, memory_data, disk_data, network_data = [[] for _ in range(4)]

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            for node in cluster_nodes:
                for metric in metrics:
                    # Calculate the mean of the metric
                    if distro == 'Baseline':
                        avg = calculate_metric_mean(file_path=f'system_usage_baseline/output_su_{node}', metric=metric)
                    elif distro == 'Microk8s':
                        avg = calculate_metric_mean(file_path=f'microk8s/system_usage_idle/output_su_{node}',
                                                    metric=metric)
                    elif distro == 'K0s':
                        avg = calculate_metric_mean(file_path=f'k0s/system_usage_idle/output_su_{node}', metric=metric)
                    elif distro == 'K3s':
                        avg = calculate_metric_mean(file_path=f'k3s/system_usage_idle/output_su_{node}', metric=metric)
                    else:
                        avg = calculate_metric_mean(file_path=f'openshift/system_usage_idle/output_su_{node}',
                                                    metric=metric)

                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Node': node,
                        'Metric': metric,
                        'Value': avg  # You can set the initial value as needed
                    }

                    # Append the dictionary to the list
                    if metric == 'CPU':
                        cpu_data.append(data_dict)
                    elif metric == 'Memory':
                        memory_data.append(data_dict)
                    elif metric == 'Disk':
                        disk_data.append(data_dict)
                    else:
                        network_data.append(data_dict)

    if deployment == 'dp-latency':
        #k8s_distributions = ['Microk8s', 'K0s', 'K3s', 'Openshift']
        k8s_distributions = ['Microk8s', 'K0s']
        requests = ['1000', '50000', '100000', '150000']
        metrics = ['Latency', 'Throughput']

        # format: microk8s-1000, microk8s-50000, microk8s-100000, microk8s-150000, k0s-1000, ...
        latency_values_1replica = [16.55, 21.15, 21.60, 21.47,
                                   25.86, 29.06, 27.46, 27.48,
                                   5, 5, 5, 5,
                                   5, 5, 5, 5]

        throughput_values_1replica = [484.69, 470.79, 431.94, 464.71,
                                      335.27, 343.93, 354.96, 352.75,
                                      111, 111, 111, 111,
                                      111, 111, 111, 111]

        latency_values_3replica = [5.53, 14.21, 16.21, 18.71,
                                   7.04, 17.74, 20.75, 24.29,
                                   2, 3, 4, 3,
                                   4, 5, 6, 7]
        throughput_values_3replica = [626.75, 667.83, 584.44, 515.81,
                                      471.94, 548.26, 475.42, 385.54,
                                      250, 400, 500, 450,
                                      111, 111, 111, 111]

        pos = 0

        for distro in k8s_distributions:
            for request in requests:
                # Create a dictionary for each combination of values
                data_dict_latency_1replica = {
                    'Distribution': distro,
                    'Request': request,
                    'Metric': metrics[0],
                    'Value': latency_values_1replica[pos]
                }

                data_dict_throughput_1replica = {
                    'Distribution': distro,
                    'Request': request,
                    'Metric': metrics[1],
                    'Value': throughput_values_1replica[pos]
                }

                data_dict_latency_3replica = {
                    'Distribution': distro,
                    'Request': request,
                    'Metric': metrics[0],
                    'Value': latency_values_3replica[pos]
                }

                data_dict_throughput_3replica = {
                    'Distribution': distro,
                    'Request': request,
                    'Metric': metrics[1],
                    'Value': throughput_values_3replica[pos]
                }

                # Append the dictionary to the list
                latency_data_1replica.append(data_dict_latency_1replica)
                throughput_data_1replica.append(data_dict_throughput_1replica)
                latency_data_3replica.append(data_dict_latency_3replica)
                throughput_data_3replica.append(data_dict_throughput_3replica)
                pos += 1

    if deployment == 'cp-latency':
        k8s_distributions = ['Microk8s', 'K0s']#, 'K3s', 'Openshift']
        pods = ['1', '2', '4', '8', '16', '32', '64']
        metrics = ['Latency', 'Throughput']

        # format: microk8s-1, microk8s-2, microk8s-4, ..., k0s-1, ...
        latency_values_3replica = [3.55, 3.84, 3.71, 4.06, 5.73, 7.32, 12.34,
                                   4.70, 4.96, 4.44, 4.77, 4.98, 5.70, 7.14]
        throughput_values_3replica = [41.60, 57.66, 101.49, 177.34, 242.16, 385.94, 343.12,
                                      22.41, 29.05, 74.28, 139.07, 280.68, 437.39, 764.35]

        pos = 0

        for distro in k8s_distributions:
            for pod in pods:
                print(pos)
                print(latency_values_3replica[pos])
                # Create a dictionary for each combination of values
                data_dict_latency_3replica = {
                    'Distribution': distro,
                    'Pods': pod,
                    'Metric': metrics[0],
                    'Value': latency_values_3replica[pos]
                }

                data_dict_throughput_3replica = {
                    'Distribution': distro,
                    'Pods': pod,
                    'Metric': metrics[1],
                    'Value': throughput_values_3replica[pos]
                }

                # Append the dictionary to the list
                latency_data_3replica.append(data_dict_latency_3replica)
                throughput_data_3replica.append(data_dict_throughput_3replica)
                pos += 1

    if deployment == 'deployment':
        my_plot_object.seaborn_bar_plot(data=data_deployment, x='Operation', y='Value', hue='Distribution',
                                        x_label='Operation', y_label='API Latency (ms)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=2100,
                                        error=True, legend=True, format_axis_label='none')
    elif deployment == 'other':
        my_plot_object.seaborn_bar_plot(data=data_rest, x='Operation', y='Value', hue='Distribution',
                                        x_label='Type of Object', y_label='API Latency (sec)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=20,
                                        error=True, legend=True, format_axis_label='none')
    elif deployment == 'baseline':
        my_plot_object.seaborn_bar_plot(data=cpu_data, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average CPU Usage (%)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=20,
                                        error=False, legend=False, format_axis_label='none')
        my_plot_object.seaborn_bar_plot(data=memory_data, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Memory Usage (%)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=40,
                                        error=False, legend=True, format_axis_label='none')
        my_plot_object.seaborn_bar_plot(data=disk_data, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Disk Usage (%)',
                                        row_index=1, col_index=0, ylim_start=0, ylim_end=15,
                                        error=False, legend=False, format_axis_label='none')
        my_plot_object.seaborn_bar_plot(data=network_data, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Network Usage (txkB/s)',
                                        row_index=1, col_index=1, ylim_start=0, ylim_end=5,
                                        error=False, legend=False, format_axis_label='none')
    elif deployment == 'dp-latency':
        my_plot_object.seaborn_bar_plot(data=latency_data_1replica, x='Request', y='Value', hue='Distribution',
                                        x_label='No. of requests', y_label='NodePort Service Latency (sec)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=40,
                                        error=False, legend=False, format_axis_label='x')
        my_plot_object.seaborn_bar_plot(data=throughput_data_1replica, x='Request', y='Value', hue='Distribution',
                                        x_label='No. of requests', y_label='NodePort Service Throughput (req/sec)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=800,
                                        error=False, legend=True, format_axis_label='x')
        my_plot_object.seaborn_bar_plot(data=latency_data_3replica, x='Request', y='Value', hue='Distribution',
                                        x_label='No. of requests', y_label='ClusterIP Service Latency (sec)',
                                        row_index=1, col_index=0, ylim_start=0, ylim_end=40,
                                        error=False, legend=False, format_axis_label='x')
        my_plot_object.seaborn_bar_plot(data=throughput_data_3replica, x='Request', y='Value', hue='Distribution',
                                        x_label='No. of requests', y_label='ClusterIP Service Throughput (req/sec)',
                                        row_index=1, col_index=1, ylim_start=0, ylim_end=800,
                                        error=False, legend=False, format_axis_label='x')
    elif deployment == 'cp-latency':
        my_plot_object.seaborn_bar_plot(data=latency_data_3replica, x='Pods', y='Value', hue='Distribution',
                                        x_label='No. of Deployments', y_label='Average Latency (sec)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=15,
                                        error=False, legend=False, format_axis_label='none')
        my_plot_object.seaborn_bar_plot(data=throughput_data_3replica, x='Pods', y='Value', hue='Distribution',
                                        x_label='No. of Deployments', y_label='Average Throughput (req/sec)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=1000,
                                        error=False, legend=True, format_axis_label='none')
    else:
        print('Invalid deployment type.')
        sys.exit(1)


def calculate_metric_mean(file_path, metric):
    """Calculate the mean of a metric"""
    if metric == 'CPU':
        df = pd.read_csv(f'{file_path}_2.csv')
        df['value'] = (100 - df['idle'])
        metric_avg = df['value'].mean()

    elif metric == 'Memory':
        df = pd.read_csv(f'{file_path}_4.csv')
        # df['value'] = (df['kbmemused'] / 1000)
        df['value'] = (df['p_memused'])
        metric_avg = df['value'].mean()

    elif metric == 'Disk':
        df = pd.read_csv(f'{file_path}_6.csv')
        df['value'] = (df['p_util'])
        metric_avg = df['value'].mean()

    else:
        df = pd.read_csv(f'{file_path}_0.csv')
        df['value'] = (df['rxkB/s'])
        metric_avg = df['value'].mean()

    return metric_avg


def bar_plot_processor():
    # fig, axs = plt.subplots(2, 2, sharex='none', sharey='none')
    nodes = ['master', 'worker1', 'worker2', 'worker3']
    metrics = ['CPU', 'Memory', 'Disk', 'Network']

    # Load data from CSV files and calculate min, max, avg
    cpu_usage = []
    mem_usage = []
    disk_usage = []
    net_usage = []

    for metric in metrics:
        for node in nodes:
            if metric == 'CPU':
                df = pd.read_csv(f'{files_path}/output_su_{node}_2.csv')
                df['value'] = (100 - df['idle'])
                cpu_avg = df['value'].mean()
                cpu_usage.append(cpu_avg)
            elif metric == 'Memory':
                df = pd.read_csv(f'{files_path}/output_su_{node}_4.csv')
                df['value'] = (df['kbmemused'] / 1000)
                mem_avg = df['value'].mean()
                mem_usage.append(mem_avg)
            elif metric == 'Disk':
                df = pd.read_csv(f'{files_path}/output_su_{node}_6.csv')
                df['value'] = (df['p_util'])
                disk_avg = df['value'].mean()
                disk_usage.append(disk_avg)
            else:
                df = pd.read_csv(f'{files_path}/output_su_{node}_0.csv')
                df['value'] = (df['rxkB/s'])
                net_avg = df['value'].mean()
                net_usage.append(net_avg)

    my_plot_object.bar_plot(x_data=nodes, y_data=cpu_usage, axs_row=0, axs_col=0, title="CPU Usage",
                            y_label="Percentage", y_lim_start=0, y_lim_end=20)
    my_plot_object.bar_plot(x_data=nodes, y_data=mem_usage, axs_row=0, axs_col=1, title="Memory Usage", y_label="MiB",
                            y_lim_start=0, y_lim_end=1024)
    my_plot_object.bar_plot(x_data=nodes, y_data=disk_usage, axs_row=1, axs_col=0, title="Disk Usage",
                            y_label="Percentage", y_lim_start=0, y_lim_end=20)
    my_plot_object.bar_plot(x_data=nodes, y_data=net_usage, axs_row=1, axs_col=1, title="Network Usage",
                            y_label="Rx KBytes/sec", y_lim_start=0, y_lim_end=5)


def pod_latency_throughput_processor(num_pods):
    """Pod creation latency and throughput"""
    avg_latencies_owp = [2.90, 2.835, 2.919, 3.986, 6.12, 11.866, 47.21]
    throughput_owp = [20.688, 19.895, 39.860, 59.145, 73.05, 81.35, 40.498]

    avg_latencies_mwp = [7.69, 3.68, 3.82, 4.10, 4.43, 5.709, 10.64]
    throughput_mwp = [7.798, 13.06, 27.785, 50.50, 113.21, 166.07, 183.67]

    # files_path = f'microk8s/pod_3worker_1run'
    my_plot_object.dual_bar_plot(x_data=num_pods,
                                 y1_data=avg_latencies_owp, y2_data=avg_latencies_mwp, y3_data=throughput_owp,
                                 y4_data=throughput_mwp,
                                 label1="One Worker Node", label2="Three Worker Nodes",
                                 x_label="Pods created concurrently", y_label_1="Latency (sec)",
                                 y_label_2="Throughput (min)")
    plt.savefig(f'figures/{distribution}_pod_latency_throughput.png', dpi=800)


workers = 3  # 1, 2, 3, 4, 5
deployment = 'other'  # 'pod' or 'deployment' or 'other' or 'baseline' or 'dp-latency' or 'cp-latency'
files_path =f'microk8s/{deployment}_{workers}worker_1run'
#files_path = f'.'
#files_path = f'system_usage_baseline'
distribution = 'microk8s'  # 'baseline' or 'microk8s' or 'k0s' or 'k3s' or 'openshift'

# Pod creation latency and throughput
# num_pods = [1, 2, 4, 8, 16, 32, 64, 110]
#num_pods = [1, 2, 4, 8, 16, 32, 64]
#pod_latency_throughput_processor(num_pods=num_pods)

# [Start] Create Seaborn bar plots
seaborn_bar_plot_process()
#plt.savefig(f'figures/{deployment}_api_latency_{workers}worker.png', dpi=800)
plt.savefig(f'figures/{deployment}_apis_latency.png', dpi=800)
#plt.savefig(f'figures/su_baseline.png', dpi=800)
#plt.savefig(f'figures/cp_latency_throughput.png', dpi=800)
#plt.savefig(f'figures/dp_latency_throughput.png', dpi=800)
# [End] Create Seaborn bar plots

# [Start] Create other plots
# bar_plot_processor(x_data=num_pods, y_data=avg_latencies, title="", x_label="Pods created concurrently", y_label="Pods starting latency (sec)", y_lim_start=0, y_lim_end=70, label="Avg. Latency", color='blue')
# bar_plot_processor(x_data=num_pods, y_data=max_latencies, title="", x_label="Pods created concurrently", y_label="Pods starting latency (sec)", y_lim_start=0, y_lim_end=70, label="Max. Latency", color='red')

# my_plot_object.dual_axis_plot(x_data=num_pods, y1_data=avg_latencies_owp, y2_data=throughput_owp, x_label="Pods created concurrently", y_lim_start=0, y_lim_end=70)
# plt.savefig(f'figures/dp_latency_throughput.png', dpi=800)
# [End] Create other plots