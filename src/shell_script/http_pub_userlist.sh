#!/bin/bash
#set -x  # 启用调试模式

# HTTP 发布脚本 - 上报ndsctl用户列表

# 默认配置
URL="http://192.168.50.242:8000/device/data/upload"
GATE_NAME="23456789"
TYPE="user_list"

# 获取ndsctl的JSON输出
get_ndsctl_json() {
    #/usr/bin/ndsctl json 2>/dev/null
    echo '{
"client_list_length": "1",
"clients":{
"b6:c8:ae:85:82:6f":{
"id":"7",
"ip":"192.168.9.114",
"mac":"b6:c8:ae:85:82:6f",
"added":"1762328300",
"active":"1762328305",
"duration":"5",
"token":"be566da7",
"state":"Authenticated",
"downloaded":"33",
"avg_down_speed":"53.80",
"uploaded":"14",
"avg_up_speed":"22.64"
}
}
}
' 2>/dev/null
}

# 构建消息体
build_message() {
    local ndsctl_json="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat <<EOF
{

    "type": "$TYPE",
    "gate_name": "$GATE_NAME",
    "timestamp": "$timestamp",
    "data": $ndsctl_json
}
EOF
}

# 发布数据到HTTP
publish_to_http() {
    local message="$1"
    echo "[DEBUG] 消息内容：$message"
    curl -X 'POST' "$URL" -H 'Content-Type: application/json' -d "$message"
}

# 主函数
main() {
    echo "[DEBUG] 脚本启动..."
    
    # 获取ndsctl JSON数据
    local ndsctl_json=$(get_ndsctl_json)
    
    if [ -z "$ndsctl_json" ]; then
        echo "[ERROR] 无法获取ndsctl数据"
        exit 1
    fi
    
    echo "[DEBUG] 获取到的ndsctl数据："
    echo "$ndsctl_json"
    
    # 构建消息
    local message=$(build_message "$ndsctl_json")
    
    # 发布到HTTP
    publish_to_http "$message"
    
    echo "[DEBUG] 脚本执行完成。"
}

# 执行主函数
main