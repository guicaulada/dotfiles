#!/usr/bin/env bash
set -euo pipefail

instance_id="$(op read "op://Private/grafana-cloud-otlp/instance-id")"
api_token="$(op read "op://Private/grafana-cloud-otlp/api-token")"
encoded="$(printf '%s:%s' "$instance_id" "$api_token" | base64)"

printf '{"Authorization":"Basic %s"}' "$encoded"
