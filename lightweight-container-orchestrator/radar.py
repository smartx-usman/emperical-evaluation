import sys

import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    node = sys.argv[1]
else:
    node = 'os_master'

categories = ['CPU Usage (%)', 'Memory Usage (%)', 'Disk Usage (%)', 'Net. Usage (txkB/s)']
N = len(categories)

if node == 'os_master':
    ubuntu_master = [0.28, 3.72, 0.36, 5]
    redhat = [0.20, 3.53, 0.05, 5.8]
    ubuntu_worker = [0.34, 5.86, 0.31, 5]
elif node == 'master':
    k0s = [10.6, 18, 4.9, 10]
    k3s = [6.4, 17.3, 0.42, 9.4]
    microk8s = [16.5, 19.8, 9.8, 8.8]
    microshift = [11.61, 33.6, 1.77, 5]
else:
    k0s = [2.32, 12.36, 0.31, 9.8]
    k3s = [1.71, 10.58, 0.31, 7]
    microk8s = [4.71, 13.32, 0.51, 9.4]

# Normalize original network data
data = np.array([0.01, 0.13, 0.005, 0.78, 0.69, 0.6, 0.012, 0.75, 0.31, 0.69])

# Step 1: Find the minimum and maximum values of the data
data_min = np.min(data)
data_max = np.max(data)

# Step 2: Scale the data to the range 0 to 1. We use a simple linear transformation.
scaled_data = (data - data_min) / (data_max - data_min)
print(scaled_data)

# Step 3: Transform the scaled data to the range 5 to 10
normalized_data = scaled_data * (10 - 5) + 5

# Step 4: Round the normalized data to a single decimal place
normalized_data = np.round(normalized_data, 1)

print(normalized_data)


# Function to create a radar chart
def plot_radar_chart(data_dict, title, y_range):
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for label, data in data_dict.items():
        values = data + data[:1]
        ax.fill(angles, values, alpha=0.1)
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=label)

    #ax.set_yticks(np.linspace(y_range[0], y_range[1], 5))
    y_step = 5
    ax.set_yticks(np.arange(y_range[0], y_range[1] + y_step, y_step))
    ax.set_ylim(*y_range)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, va='center', verticalalignment='center')
    #ax.set_xticklabels(categories, fontsize=10, ha='right')

    # Ensure labels are outside the plot area
    for label, angle in zip(ax.get_xticklabels(), angles):
        x = np.cos(angle)
        y = np.sin(angle)
        label.set_rotation_mode('anchor')
        if x < 0:  # Left side of the plot
            label.set_horizontalalignment('right')
        else:  # Right side of the plot
            label.set_horizontalalignment('left')
        #if y < 0:  # Bottom side of the plot
        #   label.set_verticalalignment('top')
        #else:  # Top side of the plot
        #   label.set_verticalalignment('bottom')

    #plt.setp(ax.get_xticklabels(), rotation=90, ha="center", rotation_mode="anchor")
    #plt.title(title, size=20, color='black', y=1.1)
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1)
    plt.tight_layout()
    #plt.show()
    fig.savefig(f"su_baseline_{node}.png", format='png', dpi=600, bbox_inches='tight')


def plot_chart_distro():
    if node == 'master':
        data_dict = {
            'K0s': k0s,
            'K3s': k3s,
            'Microk8s': microk8s,
            'Microshift': microshift if node == 'master' else []
        }
        start_range = 0
        end_range = 35
    else:
        data_dict = {
            'K0s': k0s,
            'K3s': k3s,
            'Microk8s': microk8s
        }

        start_range = 0
        end_range = 15

    plot_radar_chart(data_dict, 'Distro Radar Chart', [start_range, end_range])


def plot_chart_os():
    data_dict = {
        'Ubuntu-Master': ubuntu_master,
        'Ubuntu-Worker': ubuntu_worker
    }
    if node == 'os_master':
        data_dict['RHEL'] = redhat
    plot_radar_chart(data_dict, 'OS Radar Chart', [-1, 15])


if node == 'os_master' or node == 'os_worker':
    plot_chart_os()
else:
    plot_chart_distro()
