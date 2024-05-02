import os
import subprocess
import sys

data = 'all'  # 'all' or 'services'
deployment = 'deployment'  # 'pod' or 'deployment'
distribution = 'k0s'
workers = 1  # 1, 2, 3, 4, 5
run = 1  # 1, 3

#files_path = f'system_usage_baseline_rhel'
#files_path = f'{distribution}/system_usage_idle'
files_path = f'{distribution}/{deployment}_{workers}worker_{run}run'
files_path = f'{distribution}/pu_{workers}worker_{run}run'
files_path = f'{distribution}/dp_clusterip_1replica_{workers}worker'

#input_file_list = ['pu_cpu_master1', 'pu_cpu_worker1', 'pu_memory_master1', 'pu_memory_worker1']
input_file_list = ['pu_cpu_master1', 'pu_memory_master1']
#input_file_list = ['su_master', 'su_worker1', 'su_worker2', 'su_worker3']
#input_file_list = ['su_master', 'su_worker1']
#input_file_list = ['su_worker1', 'su_simulator']
input_file_list = ['su_master']


def process_file_all(input_file_path, output_file_path):
    # Open the input file for reading
    with open(input_file_path, 'r') as input_file:
        for line_number, line in enumerate(input_file, start=1):
            # Perform modulo operation on line number
            modulo_value = line_number % 8

            # Add column header to the first line of the output file
            if line_number == 1:
                with open(f'{output_file_path}_0.csv', 'w') as output_file:
                    output_file.write(
                        'timestamp,iface,rxpck/s,txpck/s,rxkB/s,txkB/s,rxcmp/s,txcmp/s,rxmcst/s,p_ifutil\n')

                with open(f'{output_file_path}_2.csv', 'w') as output_file:
                    output_file.write('timestamp,cpu,user,nice,system,iowait,steal,idle\n')

                with open(f'{output_file_path}_4.csv', 'w') as output_file:
                    output_file.write(
                        'timestamp,kbmemfree,kbavail,kbmemused,p_memused,kbbuffers,kbcached,kbcommit,p_commit,kbactive,kbinact,kbdirty\n')

                with open(f'{output_file_path}_6.csv', 'w') as output_file:
                    output_file.write('timestamp,dev,tps,rkB/s,wkB/s,dkB/s,areq-sz,aqu-sz,await,p_util\n')

            # Generate output file name based on modulo result
            if modulo_value in [0, 2, 4, 6]:
                output_file_path_updated = f'{output_file_path}_{modulo_value}.csv'

                # Split the input line by spaces
                values = line.split()

                # Convert the values into a CSV-formatted line
                csv_line = ','.join(values)

                # Open the output file in append mode and write the line
                with open(output_file_path_updated, 'a') as output_file:
                    output_file.write(csv_line + '\n')


def process_file_services(input_file_path, output_file_path):
    # Open the input file for reading
    with open(input_file_path, 'r') as input_file:
        for line_number, line in enumerate(input_file, start=1):
            # Perform modulo operation on line number
            modulo_value = line_number % 8

            # Add column header to the first line of the output file
            if line_number == 1:
                print(line_number)
                with open(f'{output_file_path}_0.csv', 'w') as output_file:
                    output_file.write(
                        'timestamp,uid,pid,user,system,guest,wait,cpu,cpu_no,command\n')

                with open(f'{output_file_path}_2.csv', 'w') as output_file:
                    output_file.write('timestamp,cpu,user,nice,system,iowait,steal,idle\n')

                with open(f'{output_file_path}_4.csv', 'w') as output_file:
                    output_file.write(
                        'timestamp,kbmemfree,kbavail,kbmemused,p_memused,kbbuffers,kbcached,kbcommit,p_commit,kbactive,kbinact,kbdirty\n')

                with open(f'{output_file_path}_6.csv', 'w') as output_file:
                    output_file.write('timestamp,dev,tps,rkB/s,wkB/s,dkB/s,areq-sz,aqu-sz,await,p_util\n')

            # Generate output file name based on modulo result
            if modulo_value in [0, 2, 4, 6]:
                output_file_path_updated = f'{output_file_path}_{modulo_value}.csv'

                # Split the input line by spaces
                values = line.split()

                # Convert the values into a CSV-formatted line
                csv_line = ','.join(values)

                # Open the output file in append mode and write the line
                with open(output_file_path_updated, 'a') as output_file:
                    output_file.write(csv_line + '\n')


def process_file_microshift_net(input_file_path, output_file_path):
    # Open the input file for reading
    with open(input_file_path, 'r') as input_file:
        for line_number, line in enumerate(input_file, start=1):
            # Add column header to the first line of the output file
            if line_number == 1:
                with open(f'{output_file_path}_0.csv', 'w') as output_file:
                    output_file.write(
                        'timestamp,iface,rxpck/s,txpck/s,rxkB/s,txkB/s,rxcmp/s,txcmp/s,rxmcst/s,p_ifutil\n')


            output_file_path_updated = f'{output_file_path}_0.csv'

            # Split the input line by spaces
            values = line.split()

            # Convert the values into a CSV-formatted line
            csv_line = ','.join(values)

            # Open the output file in append mode and write the line
            with open(output_file_path_updated, 'a') as output_file:
                output_file.write(csv_line + '\n')


for input_file in input_file_list:
    # Remove lines that contain 'cali' or 'vxlan' or 'loop' etc.
    if data == 'all':
        if distribution == 'microshift':
            if files_path == f'system_usage_baseline_rhel':
                command = (
                    f"grep -vE 'cali.*|vxlan.*|loop*|zram0*|vdb' '{files_path}/{input_file}.txt' > temp1 && "
                    "grep -v 'Average' temp1 > temp2 && "
                    "grep -Ev '(lo|kube-bridge|flannel.1|cni0|veth.*|ovs-system|br-ex|br-int)' temp2 > temp3 && "
                    "awk 'NR>1' temp3 > temp4 && "
                    f"awk 'NF > 0' temp4 > temp5 && "
                    f"cp temp5 '{files_path}/{input_file}_formatted.txt' &&"
                    "rm temp* &&"
                    f"cat {files_path}/{input_file}.txt | grep ovn-k8s-mp0 > net_temp"
                )
            else:
                command = (
                    f"grep -vE 'cali.*|vxlan.*|loop*|zram0*|vdb' '{files_path}/{input_file}.txt' > temp1 && "
                    "grep -v 'Average' temp1 > temp2 && "
                    "grep -Ev '(lo|veth.*|ovs-system|br-ex|br-int|ovn-k8s-mp0)' temp2 > temp3 && "
                    "awk 'NR>1' temp3 > temp4 && "
                    f"awk 'NF > 0' temp4 > temp5 && "
                    "awk '/IFACE/ {flag=1} /%user/ && !/%user$/ {flag=0; print} flag==0 || /IFACE/ || /%user/' temp5 > temp6 && "
                    "awk 'NR>1' temp6 > temp7 && "
                    f"cp temp7 '{files_path}/{input_file}_formatted.txt' &&"
                    "rm temp* &&"
                    f"cat {files_path}/{input_file}.txt | grep eth0 | grep -vE 'Average:'> net_temp"
                )
        else:
            command = (
                f"grep -vE 'cali.*|vxlan.*|loop*|zram0*' '{files_path}/{input_file}.txt' > temp1 && "
                "grep -v 'Average' temp1 > temp2 && "
                "grep -Ev '(lo|kube-bridge|flannel.1|cni0|veth.*)' temp2 > temp3 && "
                "awk 'NR>1' temp3 > temp4 && "
                f"awk 'NF > 0' temp4 > '{files_path}/{input_file}_formatted.txt' && "
                "rm temp*"
            )
    else:
        search_pattern = 'pu_cpu'
        if search_pattern in input_file:
            command = (
                f"grep -vE 'Linux.*|Time*|^$' '{files_path}/{input_file}.txt' > temp1 && "
                f"cat temp1 | awk '{{print $1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6\",\"$7\",\"$8\",\"$9\",\"$10}}' > temp2.txt && "
                f"echo 'timestamp,uid,pid,user,system,guest,wait,cpu,cpu_no,command\n' > '{files_path}/{input_file}.csv' && "
                f"cat temp2.txt >> '{files_path}/{input_file}.csv' && "
                "rm temp*"
            )
        else:
            command = (
                f"grep -vE 'Linux.*|Time*|^$' '{files_path}/{input_file}.txt' > temp1 && "
                f"cat temp1 | awk '{{print $1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6\",\"$7\",\"$8\",\"$9}}' > temp2.txt && "
                f"echo 'timestamp,uid,pid,minflt,majflt,vsz,rss,mem_per,command\n' > '{files_path}/{input_file}.csv' && "
                f"cat temp2.txt >> '{files_path}/{input_file}.csv' && "
                "rm temp*"
            )

    # Run the command
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if the command failed
    if result.returncode != 0:
        print("Command failed.")
        print("Error Output:")
        print(result.stderr)
        sys.exit(1)

    # Process the file
    if data == 'all':
        process_file_all(f'{files_path}/{input_file}_formatted.txt', f'{files_path}/output_{input_file}')

        if distribution == 'microshift':
            process_file_microshift_net(f'net_temp', f'{files_path}/output_{input_file}')

    # Remove the intermediate formatted file
    if os.path.exists(f'{files_path}/{input_file}_formatted.txt'):
        os.remove(f'{files_path}/{input_file}_formatted.txt')
        print(f"File '{files_path}/{input_file}_formatted.txt' removed.")

    # Remove the intermediate formatted file
    if os.path.exists(f'net_temp'):
        os.remove(f'net_temp')
        print(f"File net_temp removed.")

# Monitoring Commands
# sar -u -r -d -n DEV 1 720 > su_worker3.txt
