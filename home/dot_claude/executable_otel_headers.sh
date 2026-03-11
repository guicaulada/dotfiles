#!/usr/bin/env bash
set -euo pipefail

cache_dir="${TMPDIR:-/tmp}/otel-headers-cache"
cache_file="$cache_dir/headers"
lock_dir="$cache_dir/lock"
cache_ttl=300 # seconds
lock_stale=30 # seconds — assume lock is stale after this

mkdir -p "$cache_dir"

now=$(date +%s)

# Check if cached result is fresh enough
if [[ -f "$cache_file" ]]; then
  mod_time=$(stat -f %m "$cache_file" 2>/dev/null || stat -c %Y "$cache_file" 2>/dev/null)
  if ((now - mod_time < cache_ttl)); then
    cat "$cache_file"
    exit 0
  fi
fi

# Break stale locks (e.g. from a previous crash)
if [[ -d "$lock_dir" ]]; then
  lock_age=$((now - $(stat -f %m "$lock_dir" 2>/dev/null || stat -c %Y "$lock_dir" 2>/dev/null)))
  if ((lock_age > lock_stale)); then
    rmdir "$lock_dir" 2>/dev/null || true
  fi
fi

# Use mkdir as an atomic lock (portable across macOS and Linux)
if mkdir "$lock_dir" 2>/dev/null; then
  trap 'rmdir "$lock_dir" 2>/dev/null' EXIT

  instance_id="$(op read "op://Private/grafana-cloud-otlp/instance-id")"
  api_token="$(op read "op://Private/grafana-cloud-otlp/api-token")"
  encoded="$(printf '%s:%s' "$instance_id" "$api_token" | base64)"

  printf '{"Authorization":"Basic %s"}' "$encoded" >"$cache_file"
  cat "$cache_file"
else
  # Another process holds the lock — wait for it to finish
  for ((i = 0; i < 100; i++)); do
    [[ -d "$lock_dir" ]] || break
    sleep 0.1
  done

  if [[ -f "$cache_file" ]]; then
    cat "$cache_file"
  fi
fi
