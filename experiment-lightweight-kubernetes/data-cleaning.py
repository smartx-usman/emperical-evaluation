import os
import subprocess
import sys

deployment = 'deployment'  # 'pod' or 'deployment'
#measure = 'latency'  # 'latency' or 'throughput'
workers = 3  # 1, 2, 3, 4, 5

#files_path = f'microk8s/{deployment}_{workers}worker_1run'
#files_path = f'system_usage_baseline'
files_path = f'k0s/system_usage_idle'
#files_path = f'microk8s/dp_1replica_1worker'

#input_file_list = ['su_master', 'su_worker1', 'su_worker2', 'su_worker3']
input_file_list = ['su_master', 'su_worker1', 'su_worker2', 'su_worker3', 'su_simulator']
#input_file_list = ['su_master', 'su_worker1', 'su_simulation1']


def process_file(input_file_path, output_file_path):
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


for input_file in input_file_list:
    # Remove lines that contain 'cali' or 'vxlan' or 'loop' etc.
    command = (
        f"grep -vE 'cali.*|vxlan.*|loop*' '{files_path}/{input_file}.txt' > temp1 && "
        "grep -v 'Average' temp1 > temp2 && "
        "grep -Ev '(lo|kube-bridge|veth.*)' temp2 > temp3 && "
        "awk 'NR>1' temp3 > temp4 && "
        f"awk 'NF > 0' temp4 > '{files_path}/{input_file}_formatted.txt' && "
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
    process_file(f'{files_path}/{input_file}_formatted.txt', f'{files_path}/output_{input_file}')

    # Remove the intermediate formatted file
    if os.path.exists(f'{files_path}/{input_file}_formatted.txt'):
        os.remove(f'{files_path}/{input_file}_formatted.txt')
        print(f"File '{files_path}/{input_file}_formatted.txt' removed.")

# Monitoring Commands
# sar -u -r -d -n DEV 1 720 > su_worker3.txt