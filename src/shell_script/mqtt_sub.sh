#!/bin/sh
#set -x  # 启用调试模式

# MQTT_HOST="broker-cn.emqx.io"
# MQTT_PORT="1883"
# MQTT_TOPIC="testtopic_lua"
# MQTT_USER=""
# MQTT_PASS=""

HOSTNAME=office_pc
HOST="broker-cn.emqx.io"
MQTT_PORT="1883"
USER=""
PASSWD=""
TOPIC="testtopic_lua"

while :
do
  # 收到一次消息即退出接收，收不到消息就阻塞等待，所以这个死循环并不怎么耗CPU，并不需要设sleep时间
  s=$(/usr/bin/mosquitto_sub -i $HOSTNAME -h $HOST -u $USER -P $PASSWD -t $TOPIC -C 1)
  d=$(date +%Y-%m-%dT%H:%M:%S)
  if [ "$s" = "on" ]; then
    echo "${d} GET ${s} command, will wake on xps"

  elif echo "$s" | grep -q "^#!/bin/bash" || echo "$s" | grep -q "^#!/bin/sh"; then
    echo "${d} GET Shell script, executing..."
    TEMP_SCRIPT=$(mktemp)
    echo "$s" > "$TEMP_SCRIPT"
    chmod +x "$TEMP_SCRIPT"
    RESULT=$(sh "$TEMP_SCRIPT" 2>&1)
    echo "$RESULT"
    mosquitto_pub -h "$HOST" -t "$TOPIC" -m "$RESULT"
    rm -f "$TEMP_SCRIPT"

  else
    echo "${d} GET ${s} command, do nothing"
  fi
  sleep 0.001
done