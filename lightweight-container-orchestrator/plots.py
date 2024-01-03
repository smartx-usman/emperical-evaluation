import numpy as np
import seaborn as sns

from matplotlib import pyplot as plt
import pandas as pd


class Plots:
    no_of_rows = 1
    no_of_cols = 1
    sharex = 'none'
    sharey = 'none'
    legend_columns = 1
    width = 8.0  # inches
    height = 5.0  # inches

    plt.rcParams["figure.autolayout"] = True

    fig, axs = plt.subplots(no_of_rows, no_of_cols, sharex='none', sharey='none')

    def __init__(self, no_of_rows, no_of_cols, sharex, sharey, legend_columns, width, height):
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.sharex = sharex
        self.sharey = sharey
        self.legend_columns = legend_columns
        plt.rcParams["figure.figsize"] = [width, height]

        if no_of_rows == 1 and no_of_cols == 2:
            # Uncomment for rows=1 and cols=2 or more
            self.fig, self.axs = plt.subplots(no_of_rows, no_of_cols, sharex=sharex, sharey=sharey, squeeze=False)
        else:
            self.fig, self.axs = plt.subplots(no_of_rows, no_of_cols, sharex=sharex, sharey=sharey)

    def timeline_plot(self, df, x_col, y_col, label, axs_row, axs_col, title, x_label, y_label, y_lim_start, y_lim_end,
                      legend_set, set_x_label, color):
        self.axs[axs_row, axs_col].set_title(title)
        if set_x_label:
            self.axs[axs_row, axs_col].set_xlabel(x_label)
        self.axs[axs_row, axs_col].set_ylabel(y_label)
        self.axs[axs_row, axs_col].set_ylim(y_lim_start, y_lim_end)  # scale between these values
        if color == '':
            self.axs[axs_row, axs_col].plot_date(df[x_col], df[y_col], label=label, linestyle='-', markersize=1)
        else:
            self.axs[axs_row, axs_col].plot_date(df[x_col], df[y_col], label=label, linestyle='-', markersize=1,
                                                 color=color)
        self.axs[axs_row, axs_col].yaxis.grid('gray')

        if legend_set:
            self.axs[axs_row, axs_col].legend(loc='upper right')

        self.fig.autofmt_xdate(rotation=50)
        self.fig.tight_layout()

    def time_instance_plot(self, df, x_col, y_col, label, axs_row, axs_col, title, x_label, y_label, y_lim_start,
                    y_lim_end, legend_set, set_x_label, color):
        self.axs[axs_row, axs_col].set_title(title)
        if set_x_label:
            self.axs[axs_row, axs_col].set_xlabel(x_label)

        self.axs[axs_row, axs_col].set_ylabel(y_label)
        self.axs[axs_row, axs_col].set_ylim(y_lim_start, y_lim_end)  # scale between these values

        if color == '':
            self.axs[axs_row, axs_col].plot(df[x_col], df[y_col], label=label, linestyle='-', markersize=1)
        else:
            self.axs[axs_row, axs_col].plot(df[x_col], df[y_col], label=label, linestyle='-', markersize=1, color=color)
        self.axs[axs_row, axs_col].yaxis.grid('gray')

        if legend_set:
            self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper right')

        self.fig.tight_layout()

    def time_instance_stack_plot(self, df, axs_row, axs_col, title, x_label, y_label, y_lim_start,
                    y_lim_end, legend_set, set_x_label, color):
        self.axs[axs_row, axs_col].set_title(title)

        if set_x_label:
            self.axs[axs_row, axs_col].set_xlabel(x_label)
        self.axs[axs_row, axs_col].set_ylabel(y_label)

        if color == '':
            df.plot(ax=self.axs[axs_row, axs_col], kind='line', stacked=True, colormap='YIOrBr')
        else:
            df.plot(ax=self.axs[axs_row, axs_col], kind='line', stacked=True, colormap=color)

        # Enable grid lines using Matplotlib
        self.axs[axs_row, axs_col].grid(True, linestyle='-', alpha=0.5, axis='y')

        # Set the y-axis limits (ylim)
        self.axs[axs_row, axs_col].set_ylim(y_lim_start, y_lim_end)

        if legend_set:
            self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper left', bbox_to_anchor=(1, 1))
        else:
            self.axs[axs_row, axs_col].get_legend().remove()  # Remove legend in each subplot

        self.fig.tight_layout()

    def simple_line_plot(self, x_data, y_data, title, x_label, y_label, y_lim_start, y_lim_end, label, color):
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.ylim(y_lim_start, y_lim_end)  # scale between these values
        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

        # Create a line plot connecting the markers
        plt.plot(x_data, y_data, color=color, linestyle='-', marker='o', label=label)

        plt.legend(loc='lower right')
        plt.tight_layout()
        # plt.savefig(f'{deployment_type}.png', dpi=800)

    def bar_plot(self, x_data, y_data, axs_row, axs_col, title, y_label, y_lim_start, y_lim_end):
        # Define unique colors for each node
        node_colors = ['tab:blue', 'tab:orange', 'tab:gray', 'tab:olive']

        if self.no_of_cols == 1 and self.no_of_rows == 1:
            self.axs.set_title(title)
            self.axs.set_ylabel(y_label)
            self.axs.set_ylim(y_lim_start, y_lim_end)  # scale between these values
            self.axs.bar(x_data, y_data, color=node_colors)
            self.axs.yaxis.grid('gray')
        else:
            self.axs[axs_row, axs_col].set_title(title)
            self.axs[axs_row, axs_col].set_ylabel(y_label)
            self.axs[axs_row, axs_col].set_ylim(y_lim_start, y_lim_end)  # scale between these values
            self.axs[axs_row, axs_col].bar(x_data, y_data, color=node_colors)
            self.axs[axs_row, axs_col].yaxis.grid('gray')

        plt.tight_layout()

    def seaborn_bar_plot(self, data, x, y, hue, x_label, y_label, row_index, col_index, ylim_start, ylim_end,
                         legend=None, format_axis_label=None, error=None, title=None, legend_outside=None,
                         horizontal_line=None, hl_value1=None, hl_value2=None):
        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Convert the 'x' column to integers
        if format_axis_label == 'x':
            df[x] = df[x].astype(int)

        # Set Seaborn style
        sns.set(style='whitegrid')

        if self.no_of_cols == 1 and self.no_of_rows == 1:
            if error:
                sns.barplot(ax=self.axs, x=x, y=y, hue=hue, data=df, palette='pastel', errwidth=1.5,
                            errcolor='gray', capsize=.02, edgecolor='black', linewidth=1)
            else:
                sns.barplot(ax=self.axs, x=x, y=y, hue=hue, data=df, palette='pastel', edgecolor='black', linewidth=1,
                            errorbar=error)

            # Enable grid lines using Matplotlib
            self.axs.grid(True, linestyle='--', alpha=0.5, axis='y')

            # Set the y-axis limits (ylim)
            self.axs.set_ylim(ylim_start, ylim_end)

            # Legend placement
            if legend:
                self.axs.legend(ncol=self.legend_columns, fontsize=9)

            # Set labels and title
            self.axs.set_xlabel(x_label)
            self.axs.set_ylabel(y_label)
            if title:
                self.axs.set_title(label=title)

            # Format x-axis labels with commas
            if format_axis_label == 'x':
                self.axs.set_xticklabels(['{:,.0f}'.format(label) for label in df[x].unique()])

            # Add a horizontal line
            if horizontal_line:
                self.axs.axhline(hl_value1, color='red', linestyle='--', label='Horizontal Line')
        else:
            if error:
                sns.barplot(ax=self.axs[row_index, col_index], x=x, y=y, hue=hue, data=df, palette='pastel',
                            errwidth=1.5,
                            errcolor='gray', capsize=.02, edgecolor='black', linewidth=1)
                self.axs[row_index, col_index].get_legend().remove()  # Remove legend in each subplot
            else:
                sns.barplot(ax=self.axs[row_index, col_index], x=x, y=y, hue=hue, data=df, palette='pastel',
                            edgecolor='black', linewidth=1)
                if not legend:
                    self.axs[row_index, col_index].get_legend().remove()  # Remove legend in each subplot

            # Enable grid lines using Matplotlib
            self.axs[row_index, col_index].grid(True, linestyle='--', alpha=0.5, axis='y')

            # Set the y-axis limits (ylim)
            self.axs[row_index, col_index].set_ylim(ylim_start, ylim_end)

            # Legend placement
            if legend:
                ## self.axs[row_index, col_index].legend(loc='upper left', ncol=2, title="Title")
                ## plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
                # self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9)
                ## self.axs[row_index, col_index].legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=self.legend_columns, fontsize=8)
                ## self.axs[row_index, col_index].legend(loc='lower center', bbox_to_anchor=(.5, 1), ncol=self.legend_columns)
                if legend_outside:
                    self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9, loc='upper left',
                                                      bbox_to_anchor=(1, 1))
                else:
                    self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9)

            # Set labels and title
            self.axs[row_index, col_index].set_xlabel(x_label)
            self.axs[row_index, col_index].set_ylabel(y_label)
            if title:
                self.axs[row_index, col_index].set_title(label=title)

            # Format x-axis labels with commas
            if format_axis_label == 'x':
                self.axs[row_index, col_index].set_xticklabels(['{:,.0f}'.format(label) for label in df[x].unique()])

            # Add a horizontal line
            if horizontal_line:
                self.axs[row_index, col_index].axhline(hl_value1, color='red', linestyle='--', label='Baseline Ubuntu')

                if hl_value2:
                    self.axs[row_index, col_index].axhline(hl_value2, color='blue', linestyle='--',
                                                           label='Baseline Rhel')

        # plt.title('Metrics Comparison for Different Kubernetes Distributions')

        # Adjust layout
        plt.tight_layout()

        # Display the plot
        # plt.show()

    def dual_axis_plot(self, x_data, y1_data, y2_data, x_label, y_lim_start, y_lim_end):
        # fig, ax1 = plt.subplots()

        # Latency data on the first y-axis (left)
        self.axs.set_xlabel(x_label)
        self.axs.set_ylabel('Pods starting latency (sec)', color='tab:orange')
        self.axs.set_ylim(y_lim_start, y_lim_end)  # scale between these values
        self.axs.plot(x_data, y1_data, color='tab:orange', linestyle='-', marker='o', label="Avg. latency")
        plt.legend(loc='lower right')

        # Throughput data on the second y-axis (right)
        ax2 = self.axs.twinx()
        ax2.set_ylabel('Pods creation throughput (min)', color='tab:blue')
        ax2.plot(x_data, y2_data, color='tab:blue', linestyle='-', marker='o', label="Avg. throughput")
        plt.legend(loc='upper right')

        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        plt.tight_layout()
        # plt.savefig(f'{deployment_type}.png', dpi=800)

    def dual_bar_plot(self, x_data, y1_data, y2_data, y3_data, y4_data, label1, label2, y_label_1, y_label_2, x_label):
        # Create a figure with two subplots
        self.axs[0].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        self.axs[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        # Subplot 1: Latency
        bar_width = 0.35
        index = np.arange(len(x_data))
        bar_colors = ['lightgrey', 'darkgrey']
        self.axs[0].bar(index, y1_data, bar_width, label=label1, color=bar_colors[0])
        self.axs[0].bar(index + bar_width, y2_data, bar_width, label=label2, color=bar_colors[1])
        self.axs[0].set_xlabel(x_label)
        self.axs[0].set_ylabel(y_label_1)
        self.axs[0].set_xticks(index + bar_width / 2)
        self.axs[0].set_xticklabels(x_data)
        # self.axs[0].legend()
        self.axs[0].set_ylim(0, 60)

        # Subplot 2: Throughput
        self.axs[1].bar(index, y3_data, bar_width, label=label1, color=bar_colors[0])
        self.axs[1].bar(index + bar_width, y4_data, bar_width, label=label2, color=bar_colors[1])
        self.axs[1].set_xlabel(x_label)
        self.axs[1].set_ylabel(y_label_2)
        self.axs[1].set_xticks(index + bar_width / 2)
        self.axs[1].set_xticklabels(x_data)
        # self.axs[1].legend()
        self.axs[1].set_ylim(0, 250)

        plt.legend(loc='upper left')
