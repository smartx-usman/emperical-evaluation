#On all the nodes in the cluster, run the following commands and modify /etc/sysctl.conf and add the following line net.ipv4.ip_forward=1:
sudo sysctl net.ipv4.ip_forward=1
sudo sysctl -p

# Create VM instances from image
microstack.openstack server create --image  ubuntu22.04 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:master --flavor m1.medium --network 1c18ccdb-e038-442c-bb77-68383fd3a359 master1
microstack.openstack server create --image  ubuntu22.04 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker1 --flavor m1.medium --network 1c18ccdb-e038-442c-bb77-68383fd3a359 simulator
microstack.openstack server create --image  ubuntu22.04 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker1 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker1
microstack.openstack server create --image  ubuntu22.04 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker2 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker2
microstack.openstack server create --image  ubuntu22.04 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker3 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker3

# Create VM instances from snapshots
microstack.openstack server create --image  1ea7ab0a-a335-4d88-8a79-95dd9fffc5c2 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:master --flavor m1.medium --network 1c18ccdb-e038-442c-bb77-68383fd3a359 master1
microstack.openstack server create --image  554ed5ef-4753-455f-b300-8041f984eae4 --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker1 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker1
microstack.openstack server create --image  b7a6ef6b-5387-4b1c-a80e-a2c92e4629cd --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker2 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker2
microstack.openstack server create --image  1c36d2fc-b99a-4c80-a81b-ab36b667b3ff --security-group de309f13-7c25-4b6b-86a1-95c5f9e3c02c --availability-zone nova:worker3 --flavor m1.small --network 1c18ccdb-e038-442c-bb77-68383fd3a359 worker3

#microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m1.small --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker8
#microstack.openstack server create --image  ubuntu22.04 --security-group default --availability-zone nova:worker3 --flavor m2.tiny --network c62d9fb5-ebeb-4c19-837c-0882129f5918 worker9

# Create floating ip
microstack.openstack floating ip create external --floating-ip-address 10.20.20.10
microstack.openstack floating ip create external --floating-ip-address 10.20.20.11
microstack.openstack floating ip create external --floating-ip-address 10.20.20.12
microstack.openstack floating ip create external --floating-ip-address 10.20.20.13
microstack.openstack floating ip create external --floating-ip-address 10.20.20.14

# Assign floating ip
microstack.openstack server add floating ip master1 10.20.20.10
microstack.openstack server add floating ip worker1 10.20.20.11
microstack.openstack server add floating ip worker2 10.20.20.12
microstack.openstack server add floating ip worker3 10.20.20.13
microstack.openstack server add floating ip simulator 10.20.20.14
