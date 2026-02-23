local augroup = vim.api.nvim_create_augroup
local autocmd = vim.api.nvim_create_autocmd

vim.filetype.add({
  extension = {
    tmpl = 'gotmpl',
    tpl = function(_path, bufnr)
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
    end,
  },
})

autocmd('TextYankPost', {
  desc = 'Highlight on yank',
  group = augroup('highlight-yank', { clear = true }),
  callback = function()
    vim.hl.on_yank()
  end,
})
