#!/usr/bin/env bash

# Read JSON input from stdin
input=$(cat)

# Extract all data from JSON in a single jq call
eval "$(echo "$input" | jq -r '
  @sh "model=\(.model.display_name // "Unknown")",
  @sh "context_total=\(.context_window.context_window_size // 0)",
  @sh "context_percentage=\(.context_window.used_percentage // 0)",
  @sh "input_tokens=\(.context_window.total_input_tokens // 0)",
  @sh "output_tokens=\(.context_window.total_output_tokens // 0)",
  @sh "cache_write=\(.context_window.current_usage.cache_creation_input_tokens // 0)",
  @sh "cache_read=\(.context_window.current_usage.cache_read_input_tokens // 0)",
  @sh "cost=\(.cost.total_cost_usd // 0)",
  @sh "duration_ms=\(.cost.total_duration_ms // 0)",
  @sh "api_duration_ms=\(.cost.total_api_duration_ms // 0)",
  @sh "lines_added=\(.cost.total_lines_added // 0)",
  @sh "lines_removed=\(.cost.total_lines_removed // 0)",
  @sh "vim_mode=\(.vim.mode // "")",
  @sh "agent_name=\(.agent.name // "")",
  @sh "cwd=\(.workspace.current_dir // "")"
' 2>/dev/null)" || {
  model="Unknown"; context_total=0; context_percentage=0
  input_tokens=0; output_tokens=0; cache_write=0; cache_read=0
  cost=0; duration_ms=0; api_duration_ms=0
  lines_added=0; lines_removed=0; vim_mode=""; agent_name=""; cwd=""
}
total_tokens=$((input_tokens + output_tokens))

# Format cost display
if [ "$(echo "$cost >= 1" | bc)" -eq 1 ]; then
    cost_formatted=$(printf "\$%.2f" "$cost")
else
    cost_formatted=$(printf "\$%.4f" "$cost")
fi

# Format duration (ms to Xh Xm Xs)
format_duration() {
    local ms=$1
    local total_s=$((ms / 1000))
    local h=$((total_s / 3600))
    local m=$(((total_s % 3600) / 60))
    local s=$((total_s % 60))
    if [ "$h" -gt 0 ]; then
        printf "%dh %dm" "$h" "$m"
    elif [ "$m" -gt 0 ]; then
        printf "%dm %ds" "$m" "$s"
    else
        printf "%ds" "$s"
    fi
}

# Format token counts with K/M suffixes
format_tokens() {
    local tokens=$1
    if [ "$tokens" -ge 1000000 ]; then
        printf "%.1fM" "$(echo "scale=1; $tokens / 1000000" | bc)"
    elif [ "$tokens" -ge 1000 ]; then
        printf "%.1fK" "$(echo "scale=1; $tokens / 1000" | bc)"
    else
        echo "$tokens"
    fi
}

# Git information (with caching for performance)
cache_file="/tmp/claude_statusline_git_$(echo "$cwd" | md5 2>/dev/null || echo "default")"
cache_ttl=5

get_git_info() {
    if [ -f "$cache_file" ]; then
        cache_age=$(($(date +%s) - $(stat -f %m "$cache_file" 2>/dev/null || echo 0)))
        if [ "$cache_age" -lt "$cache_ttl" ]; then
            cat "$cache_file"
            return
        fi
    fi

    if [ -n "$cwd" ] && [ -d "$cwd/.git" ]; then
        cd "$cwd" 2>/dev/null || return

        git_branch=$(git --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
        git_remote=$(git --no-optional-locks config --get remote.origin.url 2>/dev/null || echo "")

        if [[ "$git_remote" =~ github.com[:/]([^/]+)/(.+)(\.git)?$ ]]; then
            repo_name="${BASH_REMATCH[2]}"
            repo_name="${repo_name%.git}"
            repo_info="${BASH_REMATCH[1]}/${repo_name}"
        else
            repo_info="local"
        fi

        status_output=$(git --no-optional-locks status --porcelain 2>/dev/null || echo "")
        added=$(echo "$status_output" | grep -cE "^A" || true)
        modified=$(echo "$status_output" | grep -cE "^.M|^M." || true)
        deleted=$(echo "$status_output" | grep -cE "^.D|^D." || true)
        untracked=$(echo "$status_output" | grep -c "^??" || true)

        echo "${git_branch}|${repo_info}|${added}|${modified}|${deleted}|${untracked}" > "$cache_file"
        echo "${git_branch}|${repo_info}|${added}|${modified}|${deleted}|${untracked}"
    else
        echo "|||||" > "$cache_file"
        echo "|||||"
    fi
}

git_info=$(get_git_info)
IFS='|' read -r git_branch repo_info g_added g_modified g_deleted g_untracked <<< "$git_info"

# Format tokens
input_fmt=$(format_tokens "$input_tokens")
output_fmt=$(format_tokens "$output_tokens")
total_fmt=$(format_tokens "$total_tokens")
cache_write_fmt=$(format_tokens "$cache_write")
cache_read_fmt=$(format_tokens "$cache_read")
context_used=$(echo "scale=0; $context_total * $context_percentage / 100" | bc)
ctx_used_fmt=$(format_tokens "$context_used")
ctx_total_fmt=$(format_tokens "$context_total")
duration_fmt=$(format_duration "$duration_ms")
api_duration_fmt=$(format_duration "$api_duration_ms")

# Colors
bold="\033[1m"
dim="\033[2m"
reset="\033[0m"
white="\033[97m"
cyan="\033[36m"
green="\033[32m"
yellow="\033[33m"
red="\033[31m"
magenta="\033[35m"
blue="\033[34m"

# Context color
if [ "$(echo "$context_percentage < 50" | bc)" -eq 1 ]; then
    ctx_color="$green"
elif [ "$(echo "$context_percentage < 80" | bc)" -eq 1 ]; then
    ctx_color="$yellow"
else
    ctx_color="$red"
fi

# Cost color
if [ "$(echo "$cost < 0.5" | bc)" -eq 1 ]; then
    cost_color="$green"
elif [ "$(echo "$cost < 2" | bc)" -eq 1 ]; then
    cost_color="$yellow"
else
    cost_color="$red"
fi

# Build progress bar (20 chars)
bar_width=20
filled=$(echo "scale=0; $context_percentage * $bar_width / 100" | bc)
empty=$((bar_width - filled))
bar=""
for ((i = 0; i < filled; i++)); do bar+="▮"; done
for ((i = 0; i < empty; i++)); do bar+="▯"; done

# Build git changes string (only show non-zero)
changes=""
total_changes=$((g_added + g_modified + g_deleted + g_untracked))
if [ "$total_changes" -eq 0 ]; then
    changes="${green}✓${reset}"
else
    [ "$g_added" -gt 0 ] && changes+="${green}+${g_added}${reset} "
    [ "$g_modified" -gt 0 ] && changes+="${yellow}~${g_modified}${reset} "
    [ "$g_deleted" -gt 0 ] && changes+="${red}-${g_deleted}${reset} "
    [ "$g_untracked" -gt 0 ] && changes+="${dim}?${g_untracked}${reset} "
    changes="${changes% }"
fi

# Line 1 (Session): Model · Cost · Duration (api) · Lines [│ VIM] [│ Agent]
line1="${bold}${white}${model}${reset}"
line1+=" ${dim}·${reset} ${cost_color}${cost_formatted}${reset}"
line1+=" ${dim}·${reset} ${dim}${duration_fmt}${reset} ${dim}(api ${api_duration_fmt})${reset}"
total_lines=$((lines_added + lines_removed))
if [ "$total_lines" -gt 0 ]; then
    line1+=" ${dim}·${reset}"
    line1+=" ${green}+${lines_added}${reset}"
    line1+=" ${red}-${lines_removed}${reset}"
    line1+=" ${dim}lines${reset}"
fi
[ -n "$vim_mode" ] && line1+=" ${dim}│${reset} ${bold}${blue}${vim_mode}${reset}"
[ -n "$agent_name" ] && line1+=" ${dim}│${reset} ${bold}${cyan}${agent_name}${reset}"

# Line 2 (Workspace): Progress bar % (used/total) │ Repo  Branch │ Changes
ctx_pct=$(printf "%.1f%%" "$context_percentage")
line2="${ctx_color}${bar}${reset}"
line2+=" ${bold}${ctx_color}${ctx_pct}${reset}"
line2+=" ${dim}(${ctx_used_fmt} / ${ctx_total_fmt})${reset}"
if [ -n "$repo_info" ]; then
    line2+=" ${dim}│${reset} ${cyan}${repo_info}${reset}"
    line2+="  ${magenta}${git_branch}${reset}"
    line2+=" ${dim}│${reset} ${changes}"
fi

# Line 3 (Tokens): in · out · total │ cached w · r (turn)
line3="${dim}in${reset} ${white}${input_fmt}${reset}"
line3+="  ${dim}out${reset} ${white}${output_fmt}${reset}"
line3+="  ${dim}total${reset} ${white}${total_fmt}${reset}"
cache_total=$((cache_write + cache_read))
if [ "$cache_total" -gt 0 ]; then
    line3+=" ${dim}│ cached${reset}"
    line3+=" ${dim}↑${reset}${white}${cache_write_fmt}${reset}"
    line3+=" ${dim}↓${reset}${white}${cache_read_fmt}${reset}"
fi

# Output
printf "%b\n%b\n%b\n" "$line1" "$line2" "$line3"
