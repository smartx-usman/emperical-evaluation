# Install microstack on all servers
sudo snap install microstack --devmode --beta

# Initialize microstack on controller node
sudo microstack init --auto --control --setup-loop-based-cinder-lvm-backend --loop-device-file-size 120

# Generate connection string
sudo microstack add-compute

# Initialize microstack on compute nodes
sudo microstack init --auto --compute --join hKhob3N0bmFtZa0xMzAuMjQzLjI2LjI4q2ZpbmdlcnByaW50xCDLHVV7ehaRynVHuPIyA8EkDJ8+Xc5hkBym/Iwf1yzvDKJpZNkgYjc5Yjk4MTI3MGI3NGE3YWJhMWQ2YjQzMzg1YjIwYWWmc2VjcmV02SBvQVgzN21DMlRoNGxBQXBiV0YzaWJUYU12T0RQaGh6cQ==

# Get key
sudo snap get microstack config.credentials.keystone-password
