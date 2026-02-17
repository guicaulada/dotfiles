vim.g.mapleader = ' '
vim.g.maplocalleader = ' '
vim.g.have_nerd_font = true

local opt = vim.opt

opt.number = true
opt.relativenumber = false
opt.mouse = 'a'
opt.showmode = false
opt.breakindent = true
opt.undofile = true
opt.ignorecase = true
opt.smartcase = true
opt.signcolumn = 'yes'
opt.updatetime = 250
opt.timeoutlen = 300
opt.splitright = true
opt.splitbelow = true
opt.list = true
opt.listchars = { tab = '» ', trail = '·', nbsp = '␣' }
opt.inccommand = 'split'
opt.cursorline = true
opt.scrolloff = 10
opt.smoothscroll = true
opt.sidescroll = 1
opt.sidescrolloff = 10
opt.confirm = true
opt.termguicolors = true
opt.wrap = false

vim.schedule(function()
  opt.clipboard = 'unnamedplus'
end)

vim.diagnostic.config({
  severity_sort = true,
  float = { border = 'rounded', source = 'if_many' },
  underline = { severity = vim.diagnostic.severity.ERROR },
  virtual_text = {
    prefix = '●',
    spacing = 4,
  },
  virtual_lines = false,
  jump = { float = true },
  signs = {
    text = {
      [vim.diagnostic.severity.ERROR] = '\u{ea87}',
      [vim.diagnostic.severity.WARN] = '\u{ea6c}',
      [vim.diagnostic.severity.HINT] = '\u{f400}',
      [vim.diagnostic.severity.INFO] = '\u{ea74}',
    },
  },
})
