#!/bin/sh
# Рендерит alertmanager.yml: подставляет __BOT_TOKEN__ и __CHAT_ID__
# значениями из переменных окружения (которые приходят из .env через env_file).

set -e

TPL=/etc/alertmanager/alertmanager.yml
OUT=/etc/alertmanager/rendered.yml

sed -e "s|__BOT_TOKEN__|${BOT_TOKEN}|g" \
    -e "s|__CHAT_ID__|${CHAT_ID}|g" \
    "$TPL" > "$OUT"

exec /bin/alertmanager --config.file="$OUT"