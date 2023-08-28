apt update
apt install -y less vim iproute2 
apt install -y dnsutils iputils-ping

echo "export LC_ALL=C.utf8" >> ~/.bashrc
source ~/.bashrc