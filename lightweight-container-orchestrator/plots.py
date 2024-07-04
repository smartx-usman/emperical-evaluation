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
            #self.fig, self.axs = plt.subplots(no_of_rows, no_of_cols, sharex=sharex, sharey=sharey)
            self.fig, self.axs = plt.subplots(no_of_rows, no_of_cols, sharex=sharex, sharey=sharey, squeeze=False)

        elif no_of_rows == 1 and no_of_cols == 4:
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
                           y_lim_end, legend_set, set_x_label, color, legend_outside=None):
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

        if title:
            self.axs[axs_row, axs_col].set_title(label=title)

        if legend_set:
            if legend_outside:
                self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper left',
                                                  bbox_to_anchor=(1, 1))
            else:
                self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper right')

        self.fig.tight_layout()

    def time_instance_stack_plot(self, df, axs_row, axs_col, title, x_label, y_label, y_lim_start,
                                 y_lim_end, legend_set, legend_outside, set_x_label, color, services, set_y_label=True):
        self.axs[axs_row, axs_col].set_title(title)

        if set_x_label:
            self.axs[axs_row, axs_col].set_xlabel(x_label)

        if set_y_label:
            self.axs[axs_row, axs_col].set_ylabel(y_label)

        if color == '':
            # Define colormap
            cmap = plt.get_cmap('YIOrBr')
            colors = cmap(np.linspace(0, 1, len(services)))
            df.plot(ax=self.axs[axs_row, axs_col], kind='line', stacked=True, colors=colors)
        else:
            cmap = plt.get_cmap(color)
            colors = cmap(np.linspace(0, 1, len(services)))
            self.axs[axs_row, axs_col].stackplot(df.index, df[services].T, labels=services, colors=colors)

        # Enable grid lines using Matplotlib
        self.axs[axs_row, axs_col].grid(True, linestyle='-', alpha=0.5, axis='y')

        # Set the y-axis limits (ylim)
        self.axs[axs_row, axs_col].set_ylim(y_lim_start, y_lim_end)

        if legend_set:
            if legend_outside:
                self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper right',
                                                  bbox_to_anchor=(1, 1))
            else:
                self.axs[axs_row, axs_col].legend(ncol=self.legend_columns, fontsize=9, loc='upper right')
        #else:
        #    self.axs[axs_row, axs_col].get_legend().remove()  # Remove legend in each subplot

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
                         horizontal_line=None, hl_value1=None, hl_value2=None,
                         hatch=None, color=None, y_no_decimal=None):
        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Convert the 'x' column to integers
        if format_axis_label == 'x':
            df[x] = df[x].astype(int)

        # Set Seaborn style
        sns.set(style='whitegrid')

        # Set the hatch pattern
        if hatch:
            hatches = ['', '+']
        else:
            hatches = ['']

        # Set color
        if color:
            pastel_palette = sns.color_palette("Paired")
            color_palette = [pastel_palette[0], pastel_palette[1], pastel_palette[6], pastel_palette[7],
                             pastel_palette[2], pastel_palette[3], pastel_palette[4], pastel_palette[5]]
        else:
            color_palette = sns.color_palette("pastel")

        if self.no_of_cols == 1 and self.no_of_rows == 1:
            if error:
                sns.barplot(ax=self.axs, x=x, y=y, hue=hue, data=df, palette='pastel', errwidth=1.5,
                            errcolor='gray', capsize=.02, edgecolor='black', linewidth=1)
            else:
                #df_median = df[df['Metric'] == 'Median']
                #sns.barplot(ax=self.axs, x=x, y=y, hue=hue, data=df_median, palette='pastel', edgecolor='black', linewidth=1,
                #            errorbar=error)
                sns.barplot(ax=self.axs, x=x, y=y, hue=hue, data=df, palette=color_palette,
                            edgecolor='black', linewidth=1, hatch=hatches, errorbar=error)

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

            # Y-Axis format without decimal places
            #self.axs.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.1f}".format(int(x))))
            self.axs.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        else:
            if error:
                sns.barplot(ax=self.axs[row_index, col_index], x=x, y=y, hue=hue, data=df, palette=color_palette,
                            errwidth=1.5,
                            errcolor='gray', capsize=.02, edgecolor='black', linewidth=1, hatch=hatches)
                self.axs[row_index, col_index].get_legend().remove()  # Remove legend in each subplot
            else:
                sns.barplot(ax=self.axs[row_index, col_index], x=x, y=y, hue=hue, data=df, palette=color_palette,
                            edgecolor='black', linewidth=1, hatch=hatches, errorbar=error)
                #df_median = df[df['Metric'] == 'Median']
                #sns.barplot(ax=self.axs[row_index, col_index], x=x, y=y, hue=hue, data=df_median, palette='pastel', edgecolor='black',
                #            linewidth=1, errorbar=error)
                if not legend:
                    self.axs[row_index, col_index].get_legend().remove()  # Remove legend in each subplot

            # Enable grid lines using Matplotlib
            self.axs[row_index, col_index].grid(True, linestyle='--', alpha=0.5, axis='y')

            # Set the y-axis limits (ylim)
            self.axs[row_index, col_index].set_ylim(ylim_start, ylim_end)

            # Set labels and title
            self.axs[row_index, col_index].set_xlabel(x_label)
            self.axs[row_index, col_index].set_ylabel(y_label)
            if title:
                self.axs[row_index, col_index].set_title(label=title)
                # self.axs[row_index, col_index].set_title(label=title, y=-0.3) # Adjust title position at bottom

            # Format x-axis labels with commas
            if format_axis_label == 'x':
                self.axs[row_index, col_index].set_xticklabels(['{:,.0f}'.format(label) for label in df[x].unique()])

            # Add a horizontal line
            if horizontal_line:
                self.axs[row_index, col_index].axhline(hl_value1, color='red', linestyle='--', label='Ubuntu')

                if hl_value2:
                    self.axs[row_index, col_index].axhline(hl_value2, color='blue', linestyle='--',
                                                           label='RHEL')

            # Legend placement
            if legend:
                ## self.axs[row_index, col_index].legend(loc='upper left', ncol=2, title="Title")
                ## plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
                # self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9)
                ## self.axs[row_index, col_index].legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=self.legend_columns, fontsize=8)
                ## self.axs[row_index, col_index].legend(loc='lower center', bbox_to_anchor=(.5, 1), ncol=self.legend_columns)
                if legend_outside:
                    self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9,
                                                          loc='upper left', bbox_to_anchor=(1, 1))
                else:
                    self.axs[row_index, col_index].legend(ncol=self.legend_columns, fontsize=9)

            # Y-Axis format without decimal places
            if y_no_decimal:
                #self.axs[row_index, col_index].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(int(x))))
                #else:
                self.axs[row_index, col_index].get_yaxis().set_major_formatter(
                    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        # plt.title('Metrics Comparison for Different Kubernetes Distributions')

        # Adjust layout
        plt.tight_layout()

    def dual_axis_plot(self, x_data, y1_data, y2_data, x_label, y1_lim_start, y1_lim_end, y2_lim_start, y2_lim_end,
                       row_index, col_index, y1_label, y2_label,
                       color, color1='tab:orange', color2='tab:blue', legend=False, title=None, distributions=None,
                       format_x_axis=None):
        self.axs[row_index, col_index].set_title(label=title)

        # Latency data on the first y-axis (left)
        self.axs[row_index, col_index].set_xlabel(x_label)
        self.axs[row_index, col_index].set_ylabel(y1_label)
        self.axs[row_index, col_index].set_ylim(y1_lim_start, y1_lim_end)  # scale between these values
        self.axs[row_index, col_index].plot(x_data, y1_data, color=color, linestyle='-', marker='o')
        #if legend:
        #    plt.legend(loc='lower right', ncol=self.legend_columns, bbox_to_anchor=(1, 1), fontsize=9)

        # Throughput data on the second y-axis (right)
        ax2 = self.axs[row_index, col_index].twinx()
        ax2.set_ylabel(y2_label)
        ax2.set_ylim(y2_lim_start, y2_lim_end)  # scale between these values
        #ax2.set_ylim(400, 900)  # scale between these values

        ax2.plot(x_data, y2_data, color=color, linestyle='--', marker='x')

        # Format x-axis labels with commas
        if format_x_axis:
            x_data_float = [float(label) for label in x_data]
            self.axs[row_index, col_index].set_xticklabels(['{:,.0f}'.format(label) for label in x_data_float])

        # Add custom legends
        if legend:
            # Define custom labels and colors for the legend
            distributions = ['K0s-latency', 'K0s-throughput', 'K3s-latency', 'K3s-throughput',
                             'Microk8s-latency', 'Microk8s-throughput', 'Microshift-latency', 'Microshift-throughput']
            #distributions = ['K0s-latency', 'K0s-throughput', 'K3s-latency', 'K3s-throughput',
            #                 'Microk8s-latency', 'Microk8s-throughput']
            custom_labels = distributions
            #custom_colors = ['blue', 'orange', 'green', 'red']
            custom_colors = ['blue', 'blue', 'orange', 'orange', 'green', 'green', 'red', 'red']

            #Define line styles
            line_styles = ['-', '--', '-', '--', '-', '--', '-', '--']  # Solid and dotted lines

            # Create custom legend
            for label, color, style in zip(custom_labels, custom_colors, line_styles):
                plt.plot([], label=label, color=color, linestyle=style)

            # Remove existing legends (if any)
            plt.legend().remove()
            #plt.legend(loc='upper left', ncol=self.legend_columns, bbox_to_anchor=(1.30, 1), fontsize=9)
            plt.legend(loc='upper left', ncol=self.legend_columns, fontsize=9, bbox_to_anchor=(1.33, 1))

        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        plt.tight_layout()

    def dual_bar_plot(self, x_data, y1_data, y2_data, y3_data, y4_data, label1, label2, y_label_1, y_label_2, x_label):
        # Create a figure with two subplots
        self.axs[0].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        self.axs[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        # Subplot 1: Latency
        bar_width = 0.35
        index = np.arange(len(x_data))
        bar_colors = ['crimson', 'slategrey']
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

        #plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.legend(loc='upper left')
