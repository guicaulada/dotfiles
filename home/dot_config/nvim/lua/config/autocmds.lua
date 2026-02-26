local augroup = vim.api.nvim_create_augroup
local autocmd = vim.api.nvim_create_autocmd

--- Detect filetype for template files (e.g. .sh.tmpl, .toml.tpl).
--- Checks the inner extension first, then falls back to content inspection.
local function detect_template(path, bufnr)
  -- Check for compound extension: file.sh.tmpl -> "sh"
  local inner_ext = path:match('%.(%w+)%.[^.]+$')
  if inner_ext then
    local ft = vim.filetype.match({ filename = 'file.' .. inner_ext, buf = bufnr })
    if ft then
      return ft
    end
  end

  local first_line = vim.api.nvim_buf_get_lines(bufnr, 0, 1, false)[1] or ''

  -- Parse shebang: #!/bin/bash, #!/usr/bin/env python3, etc.
  if first_line:match('^#!') then
    local interpreter = first_line:match('^#!.*/env%s+(%S+)') or first_line:match('^#!/.*/([^/%s]+)')
    if interpreter then
      local shebang_map = {
        bash = 'bash',
        sh = 'sh',
        zsh = 'zsh',
        fish = 'fish',
        python = 'python',
        python3 = 'python',
        ruby = 'ruby',
        perl = 'perl',
        node = 'javascript',
        nodejs = 'javascript',
        lua = 'lua',
        php = 'php',
      }
      return shebang_map[interpreter] or 'sh'
    end
    return 'sh'
  elseif first_line:match('^#') then
    return 'sh'
  elseif first_line:match('^{') or first_line:match('^%[') then
    return 'json'
  elseif first_line:match('^%-%-%-') or first_line:match('^%w+:') then
    return 'yaml'
  elseif first_line:match('^<%?xml') or first_line:match('^<') then
    return 'xml'
  end
  return 'gotmpl'
end

vim.filetype.add({
  extension = {
    tmpl = detect_template,
    tpl = detect_template,
  },
})

-- Filter out diagnostics on lines containing Go template syntax ({{ }})
autocmd('DiagnosticChanged', {
  desc = 'Hide diagnostics on Go template lines',
  group = augroup('template-diagnostics', { clear = true }),
  pattern = { '*.tmpl', '*.tpl' },
  callback = function(event)
    local bufnr = event.buf
    if vim.b[bufnr]._filtering_tmpl then
      return
    end
    vim.b[bufnr]._filtering_tmpl = true
    for ns_id, _ in pairs(vim.diagnostic.get_namespaces()) do
      local diagnostics = vim.diagnostic.get(bufnr, { namespace = ns_id })
      local line_count = vim.api.nvim_buf_line_count(bufnr)
      local lines = vim.api.nvim_buf_get_lines(bufnr, 0, line_count, false)
      -- Cache which lines have template syntax
      local tmpl_lines = {}
      for i, line in ipairs(lines) do
        if line:match('{{') or line:match('}}') then
          tmpl_lines[i] = true
        end
      end
      local filtered = vim.tbl_filter(function(d)
        -- Check the diagnostic line and its neighbors (diagnostics can bleed)
        local lnum = d.lnum + 1 -- convert 0-indexed to 1-indexed
        return not tmpl_lines[lnum] and not tmpl_lines[lnum - 1] and not tmpl_lines[lnum + 1]
      end, diagnostics)
      if #filtered < #diagnostics then
        vim.diagnostic.set(ns_id, bufnr, filtered)
      end
    end
    vim.b[bufnr]._filtering_tmpl = false
  end,
})

autocmd('TextYankPost', {
  desc = 'Highlight on yank',
  group = augroup('highlight-yank', { clear = true }),
  callback = function()
    vim.hl.on_yank()
  end,
})
