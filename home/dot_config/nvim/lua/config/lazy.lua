local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = 'https://github.com/folke/lazy.nvim.git'
  -- Pin the bootstrap to a release commit: the stable branch is a mutable ref,
  -- and lazy-lock.json cannot protect the plugin manager that reads it.
  -- Renovate (.github/renovate.json) bumps the SHA when a new release ships.
  local lazycommit = '85c7ff3711b730b4030d03144f6db6375044ae82' -- release:v11.17.5
  local out = vim.fn.system({ 'git', 'clone', '--filter=blob:none', lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    error('Error cloning lazy.nvim:\n' .. out)
  end
  out = vim.fn.system({ 'git', '-C', lazypath, 'checkout', '--quiet', lazycommit })
  if vim.v.shell_error ~= 0 then
    error('Error checking out lazy.nvim ' .. lazycommit .. ':\n' .. out)
  end
end
vim.opt.rtp:prepend(lazypath)

require('lazy').setup({
  { import = 'plugins' },
}, {
  ui = {
    icons = vim.g.have_nerd_font and {} or {
      cmd = '⌘',
      config = '🛠',
      event = '📅',
      ft = '📂',
      init = '⚙',
      keys = '🗝',
      plugin = '🔌',
      runtime = '💻',
      require = '🌙',
      source = '📄',
      start = '🚀',
      task = '📌',
      lazy = '💤 ',
    },
  },
})
