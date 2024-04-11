#!/bin/bash

# Function to add iptables rules
add_rules() {
    iptables -A FORWARD -i eth0 -o wg0 -p tcp --syn --dport 9735 -m conntrack --ctstate NEW -j ACCEPT
    iptables -A FORWARD -i eth0 -o wg0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -A FORWARD -i wg0 -o eth0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 9735 -j DNAT --to-destination 10.8.0.2
    iptables -t nat -A POSTROUTING -o wg0 -p tcp --dport 9735 -d 10.8.0.2 -j SNAT --to-source 10.8.0.1
    echo "iptables rules added successfully."
}

# Function to remove iptables rules
remove_rules() {
    iptables -D FORWARD -i eth0 -o wg0 -p tcp --syn --dport 9735 -m conntrack --ctstate NEW -j ACCEPT
    iptables -D FORWARD -i eth0 -o wg0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -D FORWARD -i wg0 -o eth0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -t nat -D PREROUTING -i eth0 -p tcp --dport 9735 -j DNAT --to-destination 10.8.0.2
    iptables -t nat -D POSTROUTING -o wg0 -p tcp --dport 9735 -d 10.8.0.2 -j SNAT --to-source 10.8.0.1
    echo "iptables rules removed successfully."
}

# Check command line argument
case "$1" in
    start)
        add_rules
        ;;
    stop)
        remove_rules
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac