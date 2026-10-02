#!/usr/bin/env bash

### BEGIN INIT INFO
# Provides:          maiawall
# Required-Start:    $network $local_fs
# Required-Stop:     $network $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Maia Firewall Service
### END INIT INFO

op=$1

function Firewall() {
cat > /etc/init.d/maiawall << "EOF"
#!/usr/bin/env bash
### BEGIN INIT INFO
# Provides:          maiawall
# Required-Start:    $network $local_fs
# Required-Stop:     $network $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Maia Firewall Service
### END INIT INFO

# Tenta carregar os modulos, ignora se já forem built-in
modprobe nf_conntrack 2>/dev/null || true
modprobe xt_LOG 2>/dev/null || true

# Enable broadcast echo Protection
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts

# Disable Source Routed Packets
echo 0 > /proc/sys/net/ipv4/conf/all/accept_source_route
echo 0 > /proc/sys/net/ipv4/conf/default/accept_source_route

# Enable TCP SYN Cookie Protection
echo 1 > /proc/sys/net/ipv4/tcp_syncookies

# Disable ICMP Redirect Acceptance
echo 0 > /proc/sys/net/ipv4/conf/default/accept_redirects

# Do not send Redirect Messages
echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/default/send_redirects

# Drop Spoofed Packets
echo 1 > /proc/sys/net/ipv4/conf/all/rp_filter
echo 1 > /proc/sys/net/ipv4/conf/default/rp_filter

# Log packets with impossible addresses
echo 1 > /proc/sys/net/ipv4/conf/all/log_martians
echo 1 > /proc/sys/net/ipv4/conf/default/log_martians

# Dynamic IP
echo 2 > /proc/sys/net/ipv4/ip_dynaddr

# Disable ECN
echo 0 > /proc/sys/net/ipv4/tcp_ecn

# Set a known state
iptables -P INPUT   DROP
iptables -P FORWARD DROP
iptables -P OUTPUT  DROP

# Flush rules
iptables -F
iptables -X
iptables -Z
iptables -t nat -F

# Allow loopback
iptables -A INPUT  -i lo -j ACCEPT

# Allow HTTP and HTTPS
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT

# Allow output
iptables -A OUTPUT -j ACCEPT

# Permit established/related
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Log remaining
iptables -A INPUT -j LOG --log-prefix "FIREWALL:INPUT "

# Restaura regras personalizadas salvas pela interface (se o arquivo existir)
if [ -s /etc/init.d/maiafirewall ]; then
    iptables-restore < /etc/init.d/maiafirewall
fi

EOF

}

function StartFirewall() {
    Firewall
    chmod +x /etc/init.d/maiawall
    bash /etc/init.d/maiawall
}

function StopFirewall() {
    echo "Parando firewall e resetando regras..."
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -F
    iptables -X
    iptables -t nat -F
}

function Outros() {
    echo "Comandos aceitos: ( start | stop | restart )"
}

case $op in
    start)
        StartFirewall
    ;;
    stop)
        StopFirewall
    ;;
    restart)
        StopFirewall
        StartFirewall
    ;;
    *)
        Outros
    ;;
esac
