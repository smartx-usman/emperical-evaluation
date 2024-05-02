import sys

import pandas as pd
from matplotlib import pyplot as plt

from plots import Plots

import warnings

# Filter out the specific warning message
warnings.filterwarnings("ignore", message="FixedFormatter should only be used together with FixedLocator")


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Subplots layout
no_of_rows = 2
no_of_cols = 2
sharex = 'none'
sharey = 'none'
legend_columns = 1
figure_width = 8.0  # inches
#figure_width = 6.0  # inches
#figure_height = 3.5  # inches for single row charts
figure_height = 6.0  # inches for two row charts
# figure_height = 7.0  # inches for four row charts

# Create the plot object
my_plot_object = Plots(no_of_rows, no_of_cols, sharex, sharey, legend_columns, figure_width, figure_height)


def seaborn_bar_plot_process():
    data_deployment = []
    data_rest = []
    k8s_distributions = ['K0s', 'K3s', 'Microk8s', 'Microshift']
    max_values = {"create": 1126.35,
                  "list": 184.50,
                  "update": 1154.4,
                  "scale": 1743.8,
                  "delete": 2056.97}

    if deployment == 'deployment':
        metrics = ['Median', 'Min', 'Max']
        actions_dep = ['create', 'list', 'update', 'scale', 'delete']

        # 40 deployments
        data_deployment_values = [
            # k0s deployment API latency results (median, min, max)
            74.524, 39.63, 351.01, 27.04, 2.49, 100.2, 55.98, 8.73, 114.37, 513.29, 9.30, 927.79, 12.25, 4.95, 993.11,
            # k3s deployment API latency results (median, min, max)
            93.23, 45.67, 234.44, 97.29, 10.21, 184.50, 107.37, 6.59, 210.71, 434.96, 6.45, 941.46, 11.61, 6.01, 490.56,
            # Microk8s deployment API latency results (median, min, max)
            324.59, 66.11, 674.39, 4.79, 2.74, 55.7, 126.54, 16.25, 1154.4, 977.6, 77.2, 1743.8, 725.6, 403.1, 1980.99,
            # Microshift deployment API latency results (median, min, max)
            115.4, 30.43, 1126.35, 21.78, 3.07, 55.39, 79.02, 8.16, 141.42, 449.55, 9.47, 1392.6, 220.16, 13.2, 2056.97
        ]

        # 20 deployments
        # data_deployment_values = [
        #     # k0s deployment API latency results (median, min, max)
        #     89.04, 17.78, 124.3, 10.3, 2.67, 26.9, 42.9, 12.3, 78.8, 630.9, 11.4,  938, 52.5, 5.38, 813.1,
        #     # k3s deployment API latency results (median, min, max)
        #     53.4, 23.0, 66.0, 37.5, 17.2, 48.3, 35.9, 11.2, 57.8, 614.4, 4.79, 915.0, 50.9, 4.43, 668.3,
        #     # Microk8s deployment API latency results (median, min, max)
        #     127.17, 28.02, 1320.8, 4.86, 2.56, 41.7, 76.4, 14.4, 337.48, 527.19, 12.27, 969.0, 577.6, 286.9, 1024.9,
        #     # Microshift deployment API latency results (median, min, max)
        #     1066.36, 1040.90, 1067.15, 11.50, 7.38, 31.58, 57.05, 28.71, 70.25, 480.53, 217.56, 996.5, 232.58, 40.50, 517.41
        # ]

        pos = 0

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            cpd_result = 0
            for action in actions_dep:
                for metric in metrics:
                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Action': action,
                        'Metric': metric,
                        'Value': data_deployment_values[pos]  # You can set the initial value as needed
                    }

                    # Append the dictionary to the list
                    data_deployment.append(data_dict)
                    pos += 1

                    # For equation result calculation
                    if metric == 'Median':
                        median_value = data_deployment_values[pos-1]
                    #if metric == 'Max':
                    #    max_value = data_deployment_values[pos-1]
                result = round(0.2 * (median_value / max_values[action]), 3)
                cpd_result = round(cpd_result + result, 3)
                print(f'Distribution: {distro}, Operation: {action}, Median: {median_value}, Max: {max_values[action]}, '
                      f'Result: {result}\n')
            print(f'Distribution: {distro}, CPD Result: {cpd_result}\n')

        my_plot_object.seaborn_bar_plot(data=data_deployment, x='Action', y='Value', hue='Distribution',
                                        x_label='Action', y_label='API Latency (ms)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=1000,
                                        legend=True, legend_outside=True, format_axis_label='none', error=None)

        plt.savefig(f'figures/{deployment}_api_latency_{workers}worker.png', dpi=800)
    elif deployment == 'other':
        max_values = {"Namespace": 6.68,
                      "Service": 17.58,
                      "PV": 6.70,
                      "PVC": 5.83}

        metrics = ['Median', 'Min', 'Max']
        operations_rest = ['Namespace', 'Service', 'PV', 'PVC']
        data_rest_values = [
            # k0s deployment API latency results (median, min, max)
            2.13, 1.58, 2.55, 6.89, 0.39, 13.24, 0.73, 0.14, 0.77, 0.62, 0.19, 1.12,
            # k3s deployment API latency results (median, min, max)
            1.28, 0.36, 1.96, 3.07, 0.52, 5.41, 0.47, 0.39, 0.86, 0.67, 0.23, 1.12,
            # Microk8s deployment API latency results (median, min, max)
            4.59, 1.61, 6.68, 10.84, 1.41, 17.58, 4.33, 0.81, 6.70, 2.75, 0.48, 5.83,
            # Microshift deployment API latency results (median, min, max)
            2.21, 1.61, 2.94, 5.05, 0.39, 5.27, 0.94, 0.30, 1.14, 0.85, 0.29, 1.67
        ]
        pos = 0

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            ood_result = 0
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

                    # For equation result calculation
                    if metric == 'Median':
                        median_value = data_rest_values[pos - 1]
                    #if metric == 'Max':
                    #    max_value = data_rest_values[pos - 1]

                    if operation == 'Namespace':
                        weight = 0.20
                    elif operation == 'Service':
                        weight = 0.50
                    elif operation == 'PV':
                        weight = 0.15
                    else:
                        weight = 0.15

                result = round(weight * (median_value / max_values[operation]), 3)
                ood_result = round(ood_result + result, 3)
                print(f'Distribution: {distro}, Operation: {operation}, Median: {median_value}, Max: {max_values[operation]}, '
                      f'Result: {result}\n')
            print(f'Distribution: {distro}, CPO Result: {ood_result}\n')

        my_plot_object.seaborn_bar_plot(data=data_rest, x='Operation', y='Value', hue='Distribution',
                                        x_label='Type of Object', y_label='Create API Latency (sec)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=20,
                                        error=True, legend=True, format_axis_label='none')
        plt.savefig(f'figures/{deployment}_apis_latency.png', dpi=800)
    elif deployment == 'baseline-master':
        cluster_nodes = ['master']
        metrics = ['CPU', 'Memory', 'Disk', 'Network']

        cpu_data_master, memory_data_master, disk_data_master, network_data_master = [[] for _ in range(4)]
        baseline_ubuntu_master = {}
        baseline_rhel_master = {}

        for distro in ('Ubuntu', 'RHEL'):
            for metric in metrics:
                if distro == 'Ubuntu':
                    baseline_ubuntu_master[metric] = calculate_metric_mean(
                        file_path=f'system_usage_baseline_ubuntu/output_su_master', metric=metric)
                else:
                    baseline_rhel_master[metric] = calculate_metric_mean(
                        file_path=f'system_usage_baseline_rhel/output_su_master', metric=metric)

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            print(f'Distribution: {distro}')
            for node in cluster_nodes:
                final_sum = 0.0  # Calculate for final equation
                for metric in metrics:
                    # Calculate the mean of the metric
                    if distro == 'Microk8s':
                        avg = calculate_metric_mean(file_path=f'microk8s/system_usage_idle/output_su_{node}',
                                                    metric=metric)
                    elif distro == 'K0s':
                        avg = calculate_metric_mean(file_path=f'k0s/system_usage_idle/output_su_{node}', metric=metric)
                    elif distro == 'K3s':
                        avg = calculate_metric_mean(file_path=f'k3s/system_usage_idle/output_su_{node}', metric=metric)
                    else:
                        avg = calculate_metric_mean(file_path=f'microshift/system_usage_idle/output_su_{node}',
                                                    metric=metric)

                    # print(f'Metric: {metric}, value: {round(avg/100, 3)}')

                    if metric == 'CPU':
                        weight = 0.4
                    elif metric == 'Memory':
                        weight = 0.25
                    elif metric == 'Disk':
                        weight = 0.20
                    elif metric == 'Network':
                        weight = 0.15

                    print(f'Weighted {metric} Value: {round((avg / 100) * weight, 3)}')
                    final_sum = final_sum + round((avg / 100) * weight, 3)

                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Node': node,
                        'Metric': metric,
                        'Value': avg  # You can set the initial value as needed
                    }

                    # Append the dictionary to the list
                    if metric == 'CPU':
                        cpu_data_master.append(data_dict)
                    elif metric == 'Memory':
                        memory_data_master.append(data_dict)
                    elif metric == 'Disk':
                        disk_data_master.append(data_dict)
                    else:
                        network_data_master.append(data_dict)
                print(f'Final Result: {round(final_sum, 3)}\n')

        my_plot_object.seaborn_bar_plot(data=cpu_data_master, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average CPU Usage (%)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=20,
                                        error=False, legend=False, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_master['CPU'],
                                        hl_value2=baseline_rhel_master['CPU'])
        my_plot_object.seaborn_bar_plot(data=memory_data_master, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Memory Usage (%)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=40,
                                        error=False, legend=False, legend_outside=True, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_master['Memory'],
                                        hl_value2=baseline_rhel_master['Memory'])
        my_plot_object.seaborn_bar_plot(data=disk_data_master, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Disk Usage (%)',
                                        row_index=0, col_index=2, ylim_start=0, ylim_end=10,
                                        error=False, legend=False, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_master['Disk'],
                                        hl_value2=baseline_rhel_master['Disk'])
        my_plot_object.seaborn_bar_plot(data=network_data_master, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Network Usage (txkB/s)',
                                        row_index=0, col_index=3, ylim_start=0, ylim_end=4,
                                        error=False, legend=True, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_master['Network'],
                                        hl_value2=baseline_rhel_master['Network'])
        plt.savefig(f'figures/su_baseline_master.png', dpi=800)
    elif deployment == 'baseline-worker':
        k8s_distributions = ['K0s', 'K3s', 'Microk8s']
        cluster_nodes = ['worker1', 'worker2', 'worker3']
        cluster_nodes = ['worker1']
        metrics = ['CPU', 'Memory', 'Disk', 'Network']

        cpu_data_workers, memory_data_workers, disk_data_workers, network_data_workers = [[] for _ in range(4)]

        baseline_ubuntu_worker = {}
        baseline_rhel_master = {}

        for distro in ('Ubuntu', 'RHEL'):
            for metric in metrics:
                if distro == 'Ubuntu':
                    baseline_ubuntu_worker[metric] = calculate_metric_mean(
                        file_path=f'system_usage_baseline_ubuntu/output_su_worker1', metric=metric)
                else:
                    baseline_rhel_master[metric] = calculate_metric_mean(
                        file_path=f'system_usage_baseline_rhel/output_su_master', metric=metric)

        # Nested loops to iterate over distributions, operations, and metrics
        for distro in k8s_distributions:
            for node in cluster_nodes:
                for metric in metrics:
                    # Calculate the mean of the metric
                    if distro == 'Microk8s':
                        avg = calculate_metric_mean(file_path=f'microk8s/system_usage_idle/output_su_{node}',
                                                    metric=metric)
                    elif distro == 'K0s':
                        avg = calculate_metric_mean(file_path=f'k0s/system_usage_idle/output_su_{node}', metric=metric)
                    elif distro == 'K3s':
                        avg = calculate_metric_mean(file_path=f'k3s/system_usage_idle/output_su_{node}', metric=metric)
                    else:
                        if node == 'master':
                            avg = calculate_metric_mean(file_path=f'microshift/system_usage_idle/output_su_{node}',
                                                        metric=metric)
                        else:
                            avg = 0

                    # Create a dictionary for each combination of values
                    data_dict = {
                        'Distribution': distro,
                        'Node': node,
                        'Metric': metric,
                        'Value': avg  # You can set the initial value as needed
                    }

                    # Append the dictionary to the list
                    if metric == 'CPU':
                        cpu_data_workers.append(data_dict)
                    elif metric == 'Memory':
                        memory_data_workers.append(data_dict)
                    elif metric == 'Disk':
                        disk_data_workers.append(data_dict)
                    else:
                        network_data_workers.append(data_dict)

        my_plot_object.seaborn_bar_plot(data=cpu_data_workers, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average CPU Usage (%)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=20,
                                        error=False, legend=False, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_worker['CPU'])
        my_plot_object.seaborn_bar_plot(data=memory_data_workers, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Memory Usage (%)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=40,
                                        error=False, legend=False, legend_outside=True, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_worker['Memory'])
        my_plot_object.seaborn_bar_plot(data=disk_data_workers, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Disk Usage (%)',
                                        row_index=0, col_index=2, ylim_start=0, ylim_end=10,
                                        error=False, legend=False, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_worker['Disk'])
        my_plot_object.seaborn_bar_plot(data=network_data_workers, x='Node', y='Value', hue='Distribution',
                                        x_label='Cluster Node', y_label='Average Network Usage (txkB/s)',
                                        row_index=0, col_index=3, ylim_start=0, ylim_end=4,
                                        error=False, legend=True, format_axis_label='none',
                                        horizontal_line=True, hl_value1=baseline_ubuntu_worker['Network'])

        plt.savefig(f'figures/su_baseline_worker.png', dpi=800)
    elif deployment == 'dp-latency':
        k8s_distributions = ['K0s-MN', 'K0s-WN', 'K3s-MN', 'K3s-WN', 'Microk8s-MN', 'Microk8s-WN', 'Microshift-MN']
        requests = ['50000', '100000', '150000']
        metrics = ['Latency', 'Throughput']

        display = 'both'  # clusterIP, nodePort, both

        np_latency_data_1replica, np_throughput_data_1replica = [], []
        ci_latency_data_1replica, ci_throughput_data_1replica = [], []
        ci_latency_data_3replica, ci_throughput_data_3replica = [], []

        # format: microk8s-1000, microk8s-50,000, microk8s-100,000, microk8s-150,000, k0s-1000, ...
        # np_latency_1replica = [258.6, 290.6, 274.6, 274.8,
        #                        157.14, 236.52, 230.00, 227.88,
        #                        165.5, 211.5, 216.0, 214.7,
        #                        99.92, 136.14, 137.84, 138.70]
        #
        # np_throughput_1replica = [335.27, 343.93, 354.96, 352.75,
        #                           474.15, 421.26, 433.88, 436.89,
        #                           484.69, 470.79, 431.94, 464.71,
        #                           640.75, 692.99, 721.42, 718.03]

        np_latency_1replica = [145.00, 142.88, 144.44,  # k0s MN
                               150.10, 138.82, 134.30,  # k0s WN
                               140.96, 139.26, 137.96,
                               172.10, 166.22, 153.04,
                               139.60, 140.00, 139.92,
                               196.50, 187.70, 166.84,
                               136.14, 137.84, 138.70]

        np_throughput_1replica = [685.57, 695.78, 689.02,
                                  662.65, 717.67, 740.26,
                                  705.18, 715.25, 722.60,
                                  572.73, 600.80, 651.89,
                                  686.80, 711.49, 712.47,
                                  506.36, 532.19, 598.49,
                                  692.99, 721.42, 718.03]

        # np_latency_1replica = [93.50, 150.10, 138.82, 134.30,
        #                        106.68, 172.10, 166.22, 153.04,
        #                        132.54, 196.50, 187.70, 166.84,
        #                        99.92, 136.14, 137.84, 138.70]
        #
        # np_throughput_1replica = [627.07, 662.65, 717.67, 740.26,
        #                           634.55, 572.73, 600.80, 651.89,
        #                           515.84, 506.36, 532.19, 598.49,
        #                           640.75, 692.99, 721.42, 718.03]

        ci_latency_1replica = [118.10, 117.76, 118.80,  # k0s MN
                               183.70, 172.18, 157.68,  # k0s WN
                               125.60, 125.14, 124.46,
                               242.58, 240.96, 237.78,
                               119.76, 120.82, 125.72,
                               211.62, 198.58, 186.44,
                               127.42, 127.90, 131.80]

        ci_throughput_1replica = [786.40, 844.54, 835.42,
                                  541.51, 577.91, 631.22,
                                  789.98, 816.17, 811.62,
                                  410.39, 414.07, 419.76,
                                  828.14, 824.19, 791.88,
                                  470.17, 501.47, 532.59,
                                  778.30, 777.26, 755.45]

        k0s_ci_latency_1replica_mn        = [118.10, 117.76, 118.80]
        k3s_ci_latency_1replica_mn        = [125.60, 125.14, 124.46]
        microk8s_ci_latency_1replica_mn   = [119.76, 120.82, 125.72]
        microshift_ci_latency_1replica_mn = [127.42, 127.90, 131.80]
        k0s_np_latency_1replica_mn        = [145.00, 142.88, 144.44]
        k3s_np_latency_1replica_mn        = [140.96, 139.26, 137.96]
        microk8s_np_latency_1replica_mn   = [139.60, 140.00, 139.92]
        microshift_np_latency_1replica_mn = [136.14, 137.84, 138.70]

        k0s_ci_throughput_1replica_mn        = [786.40, 844.54, 835.42]
        k3s_ci_throughput_1replica_mn        = [789.98, 816.17, 811.62]
        microk8s_ci_throughput_1replica_mn   = [828.14, 824.19, 791.88]
        microshift_ci_throughput_1replica_mn = [778.30, 777.26, 755.45]
        k0s_np_throughput_1replica_mn        = [685.57, 695.78, 689.02]
        k3s_np_throughput_1replica_mn        = [705.18, 715.25, 722.60]
        microk8s_np_throughput_1replica_mn   = [686.80, 711.49, 712.47]
        microshift_np_throughput_1replica_mn = [692.99, 721.42, 718.03]

        k0s_ci_latency_1replica_wn = [183.70, 172.18, 157.68]
        k0s_ci_throughput_1replica_wn = [541.51, 577.91, 631.22]

        k3s_ci_latency_1replica_wn = [242.58, 240.96, 237.78]
        k3s_ci_throughput_1replica_wn = [410.39, 414.07, 419.76]

        microk8s_ci_latency_1replica_wn = [211.62, 198.58, 186.44]
        microk8s_ci_throughput_1replica_wn = [470.17, 501.47, 532.59]

        k0s_np_latency_1replica_wn = [150.10, 138.82, 134.30]
        k0s_np_throughput_1replica_wn = [662.65, 717.67, 740.26]

        k3s_np_latency_1replica_wn = [172.10, 166.22, 153.04]
        k3s_np_throughput_1replica_wn = [572.73, 600.80, 651.89]

        microk8s_np_latency_1replica_wn = [196.50, 187.70, 166.84]
        microk8s_np_throughput_1replica_wn = [506.36, 532.19, 598.49]

        # ci_latency_1replica = [66.90, 118.10, 117.76, 118.80,
        #                        72.60, 125.60, 125.14, 124.46,
        #                        100.02, 119.76, 120.82, 125.72,
        #                        64.50, 127.42, 127.90, 131.80]
        #
        # ci_throughput_1replica = [896.93, 786.40, 844.54, 835.42,
        #                           849.25, 789.98, 816.17, 811.62,
        #                           643.92, 828.14, 824.19, 791.88,
        #                           770.21, 778.30, 777.26, 755.45]

        # ci_latency_3replica = [70.4, 177.4, 207.5, 242.9,
        #                        33.94, 69.68, 72.94, 74.78,
        #                        55.3, 142.1, 162.1, 187.1,
        #                        4, 5, 6, 7]
        # ci_throughput_3replica = [471.94, 548.26, 475.42, 385.54,
        #                           971.10, 995.19, 1137.67, 1151.72,
        #                           626.75, 667.83, 584.44, 515.81,
        #                           111, 111, 111, 111]

        pos = 0

        # for distro in k8s_distributions:
        #     # np_latency_data_1replica, np_throughput_data_1replica = [], []
        #     # ci_latency_data_1replica, ci_throughput_data_1replica = [], []
        #     for request in requests:
        #         # Create a dictionary for each combination of values
        #         ci_dict_latency_1replica = {
        #             'Distribution': distro, 'Request': request, 'Metric': metrics[0], 'Value': ci_latency_1replica[pos]
        #         }
        #
        #         ci_dict_throughput_1replica = {
        #             'Distribution': distro, 'Request': request, 'Metric': metrics[1],
        #             'Value': ci_throughput_1replica[pos]
        #         }
        #
        #         # ci_dict_latency_3replica = {
        #         #     'Distribution': distro, 'Request': request, 'Metric': metrics[0], 'Value': ci_latency_3replica[pos]
        #         # }
        #         #
        #         # ci_dict_throughput_3replica = {
        #         #     'Distribution': distro, 'Request': request, 'Metric': metrics[1],
        #         #     'Value': ci_throughput_3replica[pos]
        #         # }
        #
        #         np_dict_latency_1replica = {
        #             'Distribution': distro, 'Request': request, 'Metric': metrics[0], 'Value': np_latency_1replica[pos]
        #         }
        #
        #         np_dict_throughput_1replica = {
        #             'Distribution': distro, 'Request': request, 'Metric': metrics[1],
        #             'Value': np_throughput_1replica[pos]
        #         }
        #
        #         # Append the dictionary to the list
        #         ci_latency_data_1replica.append(ci_dict_latency_1replica)
        #         ci_throughput_data_1replica.append(ci_dict_throughput_1replica)
        #         # ci_latency_data_3replica.append(ci_dict_latency_3replica)
        #         # ci_throughput_data_3replica.append(ci_dict_throughput_3replica)
        #         np_latency_data_1replica.append(np_dict_latency_1replica)
        #         np_throughput_data_1replica.append(np_dict_throughput_1replica)
        #
        #         pos += 1

        if display == 'clusterIP':
            my_plot_object.seaborn_bar_plot(data=ci_latency_data_1replica, x='Request', y='Value', hue='Distribution',
                                            x_label='No. of requests', y_label='Latency (ms)',
                                            title='ClusterIP Service (1 Replica)',
                                            row_index=0, col_index=0, ylim_start=0, ylim_end=350, format_axis_label='x')
            my_plot_object.seaborn_bar_plot(data=ci_throughput_data_1replica, x='Request', y='Value',
                                            hue='Distribution',
                                            x_label='No. of requests', y_label='Throughput (req/sec)',
                                            title='ClusterIP Service (1 Replica)',
                                            row_index=1, col_index=0, ylim_start=0, ylim_end=1250,
                                            format_axis_label='x')
            my_plot_object.seaborn_bar_plot(data=ci_latency_data_3replica, x='Request', y='Value', hue='Distribution',
                                            x_label='No. of requests', y_label='Latency (ms)',
                                            title='ClusterIP Service (3 Replicas)',
                                            row_index=0, col_index=1, ylim_start=0, ylim_end=350, legend=True,
                                            format_axis_label='x')
            my_plot_object.seaborn_bar_plot(data=ci_throughput_data_3replica, x='Request', y='Value',
                                            hue='Distribution',
                                            x_label='No. of requests', y_label='Throughput (req/sec)',
                                            title='ClusterIP Service (3 Replicas)',
                                            row_index=1, col_index=1, ylim_start=0, ylim_end=1400,
                                            format_axis_label='x')
        elif display == 'nodePort':
            my_plot_object.seaborn_bar_plot(data=np_latency_data_1replica, x='Request', y='Value', hue='Distribution',
                                            x_label='No. of requests', y_label='Latency (ms)',
                                            title='ClusterIP Service (1 Replica)',
                                            row_index=0, col_index=0, ylim_start=0, ylim_end=350, format_axis_label='x')
            my_plot_object.seaborn_bar_plot(data=np_throughput_data_1replica, x='Request', y='Value',
                                            hue='Distribution',
                                            x_label='No. of requests', y_label='Throughput (req/sec)',
                                            title='ClusterIP Service (1 Replica)',
                                            row_index=1, col_index=0, ylim_start=0, ylim_end=1250,
                                            format_axis_label='x')
            # my_plot_object.seaborn_bar_plot(data=np_latency_data_3replica, x='Request', y='Value', hue='Distribution',
            #                                 x_label='No. of requests', y_label='Latency (ms)',
            #                                 title='ClusterIP Service (3 Replicas)',
            #                                 row_index=0, col_index=1, ylim_start=0, ylim_end=350, legend=True,
            #                                 format_axis_label='x')
            # my_plot_object.seaborn_bar_plot(data=np_throughput_data_3replica, x='Request', y='Value', hue='Distribution',
            #                                 x_label='No. of requests', y_label='Throughput (req/sec)',
            #                                 title='ClusterIP Service (3 Replicas)',
            #                                 row_index=1, col_index=1, ylim_start=0, ylim_end=1400,
            #                                 format_axis_label='x')
        else:
            for row_index in (0, 1):
                for col_index in (0, 1):
                    legend = False

                    if row_index == 0 and col_index == 0:
                        title = 'ClusterIP Service (MN)'
                        y1_lim_start = 100
                        y1_lim_end = 250
                        y2_lim_start = 500
                        y2_lim_end = 900
                    elif row_index == 0 and col_index == 1:
                        title = 'NodePort Service (MN)'
                        y1_lim_start = 100
                        y1_lim_end = 250
                        y2_lim_start = 500
                        y2_lim_end = 900
                    elif row_index == 1 and col_index == 0:
                        title = 'ClusterIP Service (WN)'
                        y1_lim_start = 120
                        y1_lim_end = 250
                        y2_lim_start = 400
                        y2_lim_end = 700
                    else:
                        title = 'NodePort Service (WN)'
                        y1_lim_start = 120
                        y1_lim_end = 240
                        y2_lim_start = 400
                        y2_lim_end = 800

                    k8s_distributions = ['K0s', 'K3s', 'Microk8s', 'Microshift']
                    for distro in k8s_distributions:
                        if row_index == 0 and col_index == 0:
                            if distro == 'K0s':
                                latency_data = k0s_ci_latency_1replica_mn
                                throughput_data = k0s_ci_throughput_1replica_mn
                                color = 'blue'
                            elif distro == 'K3s':
                                color = 'orange'
                                latency_data = k3s_ci_latency_1replica_mn
                                throughput_data = k3s_ci_throughput_1replica_mn
                            elif distro == 'Microk8s':
                                color = 'green'
                                latency_data = microk8s_ci_latency_1replica_mn
                                throughput_data = microk8s_ci_throughput_1replica_mn
                            else:
                                color = 'red'
                                latency_data = microshift_ci_latency_1replica_mn
                                throughput_data = microshift_ci_throughput_1replica_mn

                            print(f'Latency: {latency_data[1]}  Throughput: {throughput_data[1]}')
                            print(f'Service: ClusterIP Distribution: {distro} Latency: {round(0.6 * latency_data[1]/142.88 , 3)} Throughput: {round(0.6 * (1 - (throughput_data[1]/844.54)), 3)}')

                        elif row_index == 0 and col_index == 1:
                            if distro == 'K0s':
                                latency_data = k0s_np_latency_1replica_mn
                                throughput_data = k0s_np_throughput_1replica_mn
                                color = 'blue'
                                legend = True
                            elif distro == 'K3s':
                                color = 'orange'
                                latency_data = k3s_np_latency_1replica_mn
                                throughput_data = k3s_np_throughput_1replica_mn
                            elif distro == 'Microk8s':
                                color = 'green'
                                latency_data = microk8s_np_latency_1replica_mn
                                throughput_data = microk8s_np_throughput_1replica_mn
                            else:
                                color = 'red'
                                latency_data = microshift_np_latency_1replica_mn
                                throughput_data = microshift_np_throughput_1replica_mn

                            print(f'Latency: {latency_data[1]}  Throughput: {throughput_data[1]}')
                            print(
                                f'Service: ClusterIP Distribution: {distro} Latency: {round(0.4 * latency_data[1] / 142.88, 3)} Throughput: {round(0.4 * (1 - (throughput_data[1] / 844.54)), 3)}')

                        elif row_index == 1 and col_index == 0:
                            if distro == 'K0s':
                                latency_data = k0s_ci_latency_1replica_wn
                                throughput_data = k0s_ci_throughput_1replica_wn
                                color = 'blue'
                            elif distro == 'K3s':
                                color = 'orange'
                                latency_data = k3s_ci_latency_1replica_wn
                                throughput_data = k3s_ci_throughput_1replica_wn
                            elif distro == 'Microk8s':
                                color = 'green'
                                latency_data = microk8s_ci_latency_1replica_wn
                                throughput_data = microk8s_ci_throughput_1replica_wn
                            else:
                                latency_data = ''
                                throughput_data = ''
                        else:
                            if distro == 'K0s':
                                latency_data = k0s_np_latency_1replica_wn
                                throughput_data = k0s_np_throughput_1replica_wn
                                color = 'blue'
                            elif distro == 'K3s':
                                color = 'orange'
                                latency_data = k3s_np_latency_1replica_wn
                                throughput_data = k3s_np_throughput_1replica_wn
                            elif distro == 'Microk8s':
                                color = 'green'
                                latency_data = microk8s_np_latency_1replica_wn
                                throughput_data = microk8s_np_throughput_1replica_wn
                            else:
                                latency_data = ''
                                throughput_data = ''

                        if latency_data and throughput_data:
                            my_plot_object.dual_axis_plot(x_data=requests,
                                                      y1_data=latency_data, y2_data=throughput_data,
                                                      title=title,
                                                      legend=legend,
                                                      color=color,
                                                      x_label="No. of requests",
                                                      y1_label="Latency (ms)",
                                                      y2_label="Throughput (req/sec)",
                                                      distributions=k8s_distributions,
                                                      row_index=row_index, col_index=col_index,
                                                      format_x_axis=True,
                                                      y1_lim_start=y1_lim_start, y1_lim_end=y1_lim_end,
                                                      y2_lim_start=y2_lim_start, y2_lim_end=y2_lim_end)

            # my_plot_object.seaborn_bar_plot(data=ci_latency_data_1replica, x='Request', y='Value', hue='Distribution',
            #                                 x_label='No. of requests', y_label='Latency (ms)',
            #                                 title='ClusterIP Service', color=True,
            #                                 row_index=0, col_index=0, ylim_start=0, ylim_end=250, format_axis_label='x')
            # my_plot_object.seaborn_bar_plot(data=ci_throughput_data_1replica, x='Request', y='Value',
            #                                 hue='Distribution',
            #                                 x_label='No. of requests', y_label='Throughput (req/sec)',
            #                                 title='ClusterIP Service', color=True,
            #                                 row_index=1, col_index=0, ylim_start=0, ylim_end=1000,
            #                                 format_axis_label='x')
            # my_plot_object.seaborn_bar_plot(data=np_latency_data_1replica, x='Request', y='Value', hue='Distribution',
            #                                 x_label='No. of requests', y_label='Latency (ms)',
            #                                 title='NodePort Service', color=True,
            #                                 row_index=0, col_index=1, ylim_start=0, ylim_end=250,
            #                                 format_axis_label='x', legend_outside=True, legend=True)
            # my_plot_object.seaborn_bar_plot(data=np_throughput_data_1replica, x='Request', y='Value',
            #                                 hue='Distribution',
            #                                 x_label='No. of requests', y_label='Throughput (req/sec)',
            #                                 title='NodePort Service', color=True,  # legend=True,
            #                                 row_index=1, col_index=1, ylim_start=0, ylim_end=1000,
            #                                 format_axis_label='x')

        plt.savefig(f'figures/dp_{display}_latency_throughput.png', dpi=800)
    elif deployment == 'cp-latency':
        pods = ['1', '2', '4', '8', '16', '32', '64']
        metrics = ['Latency', 'Throughput']
        latency_data_3replica = []
        throughput_data_3replica = []

        # format: microk8s-1, microk8s-2, microk8s-4, ..., k0s-1, ...
        latency_values_3replica = [4.70, 4.96, 4.44, 4.77, 4.98, 5.70, 7.14,
                                   4.82, 4.69, 4.60, 4.54, 3.56, 4.01, 6.61,
                                   3.55, 3.84, 3.71, 4.06, 5.73, 7.32, 12.34,
                                   3.09, 3.08, 2.68, 3.45, 6.16, 11.60, 0]
        throughput_values_3replica = [22.41, 29.05, 74.28, 139.07, 280.68, 437.39, 764.35,
                                      21.00, 33.08, 71.31, 142.39, 401.45, 698.84, 974.27,
                                      41.60, 57.66, 101.49, 177.34, 242.16, 385.94, 343.12,
                                      36.34, 56.47, 135.29, 203.16, 221.52, 207.92, 0
                                      ]

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

        my_plot_object.seaborn_bar_plot(data=latency_data_3replica, x='Pods', y='Value', hue='Distribution',
                                        x_label='No. of Deployments', y_label='Average Latency (sec)',
                                        row_index=0, col_index=0, ylim_start=0, ylim_end=15)
        my_plot_object.seaborn_bar_plot(data=throughput_data_3replica, x='Pods', y='Value', hue='Distribution',
                                        x_label='No. of Deployments', y_label='Average Throughput (pods/min)',
                                        row_index=0, col_index=1, ylim_start=0, ylim_end=1100, legend=True)

        plt.savefig(f'figures/cp_latency_throughput.png', dpi=800)
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

    avg_latencies_mwp = [3.68, 3.68, 3.82, 4.10, 4.43, 5.709, 10.64]
    throughput_mwp = [13.06, 13.06, 27.785, 50.50, 113.21, 166.07, 183.67]

    # files_path = f'microk8s/pod_3worker_1run'
    my_plot_object.dual_bar_plot(x_data=num_pods,
                                 y1_data=avg_latencies_owp, y2_data=avg_latencies_mwp, y3_data=throughput_owp,
                                 y4_data=throughput_mwp,
                                 label1="One Worker", label2="Three Workers",
                                 x_label="Pods created concurrently", y_label_1="Latency (sec)",
                                 y_label_2="Throughput (min)")
    plt.savefig(f'figures/{distribution}_pod_latency_throughput.png', dpi=800)


workers = 3  # 1, 2, 3, 4, 5
deployment = 'dp-latency'  # 'pod' or 'deployment' or 'other' or 'baseline-master' or 'baseline-worker' or 'dp-latency' or 'cp-latency'
files_path = f'microk8s/{deployment}_{workers}worker_1run'
# files_path = f'system_usage_baseline'
distribution = 'microk8s'  # 'baseline' or 'microk8s' or 'k0s' or 'k3s' or 'microshift'

# Pod creation latency and throughput
# num_pods = [1, 2, 4, 8, 16, 32, 64, 110]
#num_pods = [1, 2, 4, 8, 16, 32, 64]
#pod_latency_throughput_processor(num_pods=num_pods)

# [Start] Create Seaborn bar plots
seaborn_bar_plot_process()
# [End] Create Seaborn bar plots

# [Start] Create other plots
# bar_plot_processor(x_data=num_pods, y_data=avg_latencies, title="", x_label="Pods created concurrently", y_label="Pods starting latency (sec)", y_lim_start=0, y_lim_end=70, label="Avg. Latency", color='blue')
# bar_plot_processor(x_data=num_pods, y_data=max_latencies, title="", x_label="Pods created concurrently", y_label="Pods starting latency (sec)", y_lim_start=0, y_lim_end=70, label="Max. Latency", color='red')

# my_plot_object.dual_axis_plot(x_data=num_pods, y1_data=avg_latencies_owp, y2_data=throughput_owp, x_label="Pods created concurrently", y_lim_start=0, y_lim_end=70)
# plt.savefig(f'figures/dp_latency_throughput.png', dpi=800)
# [End] Create other plots
