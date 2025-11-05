#!/bin/bash
#set -x  # 启用调试模式

# MQTT 发布脚本 - 上报机器特征（IP、时间、MAC、主机名、DHCP、主板、硬盘等）

# 默认配置
MQTT_HOST="broker-cn.emqx.io"
MQTT_PORT="1883"
MQTT_TOPIC="testtopic_lua"
MQTT_USER=""
MQTT_PASS=""

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
    if command -v dhcpcd &> /dev/null; then
        DHCP_SERVER=$(dhcpcd -U eth0 | grep "dhcp_server_identifier" | awk -F"'" '{print $2}')
        DHCP_LEASE_TIME=$(dhcpcd -U eth0 | grep "dhcp_lease_time" | awk -F"'" '{print $2}')
    elif command -v dhclient &> /dev/null; then
        DHCP_SERVER=$(dhclient -v eth0 2>&1 | grep "DHCPOFFER" | awk '{print $3}')
        DHCP_LEASE_TIME=$(dhclient -v eth0 2>&1 | grep "lease-time" | awk '{print $3}')
    fi

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

    # 构造 JSON 消息
    local message="{\"ip\":\"$IP_ADDRESS\", \"time\":\"$CURRENT_TIME\", \"mac\":\"$MAC_ADDRESS\", \"hostname\":\"$HOSTNAME\", \"os\":\"$OS_INFO\", \"dhcp_server\":\"$DHCP_SERVER\", \"dhcp_lease_time\":\"$DHCP_LEASE_TIME\", \"board_serial\":\"$BOARD_SERIAL\", \"disk_serial\":\"$DISK_SERIAL\"}"
    local auth=""
    
    if [ -n "$MQTT_USER" ] && [ -n "$MQTT_PASS" ]; then
        auth="-u $MQTT_USER -P $MQTT_PASS"
    fi
    
    echo "[DEBUG] 发布到 MQTT 服务器：$MQTT_HOST:$MQTT_PORT, 主题: $MQTT_TOPIC"
    echo "[DEBUG] 消息内容：$message"
    mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" -t "$MQTT_TOPIC" -m "$message" $auth
}

# 主函数
main() {
    echo "[DEBUG] 脚本启动..."
    publish_to_mqtt
    echo "[DEBUG] 脚本执行完成。"
}

# 执行主函数
main