#Before installing Microshift add additional disk and create vgs with name rhel.

# Set MTU for the ovn-master. Uncomment below lines and add in the file.
vi /etc/microshift/ovn.cfg
# MTU value to be used for the Pods, must be less than or equal to the MTU of
# default route interface.
#ovsInit:
#  disableOVSInit: true
#  gatewayInterface: eth0
#mtu: 1330

# Assign IP to br-ex and set MTU
sudo ip address add 10.42.0.1/24 dev br-ex
sudo ip link set dev br-ex mtu 1330

# Create security settings to allow pods creation
kubectl create ns coap-server
oc label namespace coap-server pod-security.kubernetes.io/warn=privileged --overwrite
oc label namespace coap-server pod-security.kubernetes.io/enforce=privileged --overwrite
oc label namespace coap-server pod-security.kubernetes.io/audit=privileged --overwrite