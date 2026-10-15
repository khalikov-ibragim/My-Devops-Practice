# Monitoring — инфраструктура

Папка мониторинга. Собирает метрики с трёх машин, хранит их и показывает в Grafana,
присылает уведомления в Telegram.

## Схема

```
VM1 (10.81.6.252) ──┐
VM2 (10.81.6.179) ──┼──▶ Prometheus ──▶ Grafana
   NOTBOOK (главная) ┘      │
   node-exporter             ▼
                            Alertmanager ──▶ Telegram
```

Роли инструментов:

| Инструмент | Роль | Порт |
| --- | --- | --- |
| node-exporter | агент: собирает метрики хоста (CPU, RAM, диск) | 9100 |
| Prometheus | хранилище: опрашивает агентов, хранит историю, считает правила | 9090 |
| Grafana | витрина: рисует графики из Prometheus | 3000 |
| Alertmanager | доставщик: отправляет алерты в Telegram | 9093 |

**Кто кому инициирует:** Prometheus сам ходит к node-exporter'ам по HTTP и забирает
метрики (pull-модель). Никто ничего никуда не «отправляет» — все ждут, пока спросят.

## Файлы

| Файл | Кто читает | Зачем |
| --- | --- | --- |
| `docker-compose.yml` | podman-compose | сервисы главной машины: node-exporter, Prometheus, Grafana, Alertmanager |
| `docker-monitoring.yml` | podman-compose на VM | только node-exporter для удалённых машин (передаётся через Ansible) |
| `prometheus.yml` | Prometheus | как часто опрашивать, какие targets, куда слать алерты |
| `alertmanager.yml` | Alertmanager | **куда** слать уведомления (Telegram: токен + chat_id) |
| `alert.rules.yml` | Prometheus | **что** считать проблемой (условия срабатывания алертов) |
| `.env.example` | человек | образец переменных, **без реальных секретов** |

## Разделение ответственности (главное, что путают)

```
prometheus.yml      — ГДЕ искать (targets) и КОГДА (scrape_interval)
alert.rules.yml     — ЧТО считать проблемой (expr, for)
alertmanager.yml    — КУДА слать (telegram_configs)
```

Правило живёт в Prometheus (он его вычисляет), канал доставки — в Alertmanager
(он его отправляет). Разные файлы, разные ответственности.

## Поток данных по шагам

```
1. Prometheus каждые scrape_interval (15s) делает GET http://<target>:9100/metrics
2. node-exporter отдаёт текст с метриками
3. Prometheus складывает значения в свою базу (TSDB) — появляется история
4. Prometheus вычисляет правила из alert.rules.yml:
      up == 0 дольше 1 минуты  →  алерт InstanceDown (severity: critical)
5. Алерт уходит в Alertmanager (адрес указан в prometheus.yml → alerting)
6. Alertmanager группирует и шлёт в Telegram (адрес/токен — в alertmanager.yml)
7. Grafana рисует историю из Prometheus
```

## Как это связано с Ansible

```
infra/ansible/monitoring.yml              ← playbook
infra/ansible/roles/node-exporter/        ← роль
infra/ansible/roles/node-exporter/files/docker-compose.yml
```

Роль копирует `docker-monitoring.yml` на VM как `/opt/node-exporter/docker-compose.yml`
и запускает. Группа `[monitoring]` в inventory = vm1 + vm2.

## Проверка

```bash
# кто жив
curl -sG 'http://localhost:9090/api/v1/query' --data-urlencode 'query=up'

# загрузка CPU, %
curl -sG 'http://localhost:9090/api/v1/query' \
  --data-urlencode 'query=100 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100'

# UI
http://localhost:9090          # Targets, Config, Alerts
http://localhost:3000          # Grafana
http://localhost:9093          # Alertmanager
```

## Известные грабли (личный опыт)

1. **`.env` не читается в смонтированных конфигах.** `${{ VAR }}` работает только
   в самом docker-compose.yml. Внутри `alertmanager.yml` подстановки нет — токен
   пишется строкой. В проде это решают рендерингом через `envsubst` или секрет-хранилищем.
2. **Путь монтирования = путь по умолчанию в образе.** Alertmanager читает
   `/etc/alertmanager/alertmanager.yml`. Если смонтировать в `/etc/alertmanager.yml` —
   конфиг просто не прочитается.
3. **Файл правил монтируется в сервис `prometheus`, а не `node-exporter`.**
4. **`alerting:` — верхний ключ в prometheus.yml, не внутри `global:`.**
5. **`targets` — список, не строка.** И локальные цели пишутся именем сервиса
   (`node-exporter:9100`), а удалённые — IP (`10.81.6.252:9100`).
6. **SELinux на РЕД ОС** — конфиги монтируются с `:ro,z`. Без `z` → `permission denied`
   (файл помечен `user_home_t`).
7. **Prometheus читает конфиг только при старте** — после правки `prometheus.yml`
   нужен `podman restart monitoring_prometheus_1`.
8. **`.env.example` без секретов**, `.env` — в `.gitignore`.
