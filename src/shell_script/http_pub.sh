#!/bin/bash
#set -x  # 启用调试模式

# MQTT 发布脚本 - 上报机器特征（IP、时间、MAC、主机名、DHCP、主板、硬盘等）

# 默认配置
URL="http://192.168.50.242:8000/device/data/upload"
GATE_NAME="23456789"
TYPE="machine_info"

# 发布机器特征到 MQTT
publish_to_mqtt() {
    # 获取本机 IP 地址
    IP_ADDRESS=$(hostname -I | awk '{print $1}')
    if [ -z "$IP_ADDRESS" ]; then
        IP_ADDRESS=$(ip addr | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d'/' -f1 | head -n 1)
    fi

    # 获取当前时间
    CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

    # 获取 MAC 地址
    MAC_ADDRESS=$(ip link | grep -A 1 "$(ip route | grep default | awk '{print $5}')" | grep ether | awk '{print $2}')
    if [ -z "$MAC_ADDRESS" ]; then
        MAC_ADDRESS=$(ifconfig | grep ether | awk '{print $2}' | head -n 1)
    fi

    # 获取主机名
    HOSTNAME=$(hostname)

    # 获取操作系统信息
    OS_INFO=$(uname -a)

    # 获取 DHCP 信息
    DHCP_SERVER=""
    DHCP_LEASE_TIME=""
    # if command -v dhcpcd &> /dev/null; then
    #     DHCP_SERVER=$(dhcpcd -U eth0 | grep "dhcp_server_identifier" | awk -F"'" '{print $2}')
    #     DHCP_LEASE_TIME=$(dhcpcd -U eth0 | grep "dhcp_lease_time" | awk -F"'" '{print $2}')
    # elif command -v dhclient &> /dev/null; then
    #     DHCP_SERVER=$(dhclient -v eth0 2>&1 | grep "DHCPOFFER" | awk '{print $3}')
    #     DHCP_LEASE_TIME=$(dhclient -v eth0 2>&1 | grep "lease-time" | awk '{print $3}')
    # fi

    # 获取主板序列号（需要 sudo 权限）
    BOARD_SERIAL=""
    if command -v dmidecode &> /dev/null; then
        BOARD_SERIAL=$(sudo dmidecode -s baseboard-serial-number 2>/dev/null || echo "N/A")
    else
        BOARD_SERIAL="N/A"
    fi

    # 获取硬盘序列号（需要 sudo 权限）
    DISK_SERIAL=""
    if command -v hdparm &> /dev/null; then
        DISK_SERIAL=$(sudo hdparm -I /dev/sda | grep "Serial Number" | awk -F":" '{print $2}' | tr -d "[:space:]" 2>/dev/null || echo "N/A")
    elif command -v smartctl &> /dev/null; then
        DISK_SERIAL=$(sudo smartctl -i /dev/sda | grep "Serial Number" | awk -F":" '{print $2}' | tr -d "[:space:]" 2>/dev/null || echo "N/A")
    else
        DISK_SERIAL="N/A"
    fi

    # 获取CPU信息
    CPU_CORES=$(nproc 2>/dev/null || echo "N/A")
    CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | sed 's/^[ \t]*//' 2>/dev/null || echo "N/A")
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}' 2>/dev/null || echo "N/A")

    # 获取内存信息
    MEM_TOTAL=$(free -h | grep Mem | awk '{print $2}' 2>/dev/null || echo "N/A")
    MEM_USED=$(free -h | grep Mem | awk '{print $3}' 2>/dev/null || echo "N/A")
    MEM_FREE=$(free -h | grep Mem | awk '{print $4}' 2>/dev/null || echo "N/A")
    MEM_USAGE_PERCENT=$(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100}' 2>/dev/null || echo "N/A")

    # 获取硬盘大小和使用情况
    DISK_TOTAL=$(df -h / | awk 'NR==2 {print $2}' 2>/dev/null || echo "N/A")
    DISK_USED=$(df -h / | awk 'NR==2 {print $3}' 2>/dev/null || echo "N/A")
    DISK_AVAIL=$(df -h / | awk 'NR==2 {print $4}' 2>/dev/null || echo "N/A")
    DISK_USAGE_PERCENT=$(df -h / | awk 'NR==2 {print $5}' 2>/dev/null || echo "N/A")

    # 构造 JSON 消息
    local data='{ "ip":"'$IP_ADDRESS'", "time":"'$CURRENT_TIME'", "mac":"'$MAC_ADDRESS'", "hostname":"'$HOSTNAME'", "os":"'$OS_INFO'", "dhcp_server":"'$DHCP_SERVER'", "dhcp_lease_time":"'$DHCP_LEASE_TIME'", "board_serial":"'$BOARD_SERIAL'", "disk_serial":"'$DISK_SERIAL'", "cpu_cores":"'$CPU_CORES'", "cpu_model":"'$CPU_MODEL'", "cpu_usage":"'$CPU_USAGE'", "mem_total":"'$MEM_TOTAL'", "mem_used":"'$MEM_USED'", "mem_free":"'$MEM_FREE'", "mem_usage_percent":"'$MEM_USAGE_PERCENT'", "disk_total":"'$DISK_TOTAL'", "disk_used":"'$DISK_USED'", "disk_avail":"'$DISK_AVAIL'", "disk_usage_percent":"'$DISK_USAGE_PERCENT'"}'
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message='{"type":"'$TYPE'", "gate_name":"'$GATE_NAME'", "timestamp": "'$timestamp'", "data":'$data'}'

    echo "[DEBUG] 消息内容：$message"
    #mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" -t "$MQTT_TOPIC" -m "$message" $auth
    curl -X 'POST' "$URL" -H 'Content-Type: application/json' -d "$message"
}

# 主函数
main() {
    echo "[DEBUG] 脚本启动..."
    publish_to_mqtt
    echo "[DEBUG] 脚本执行完成。"
}

# 执行主函数
main