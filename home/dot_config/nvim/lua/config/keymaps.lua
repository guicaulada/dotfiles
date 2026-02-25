local map = vim.keymap.set

map('n', '<Esc>', '<cmd>nohlsearch<CR>')
map('t', '<Esc><Esc>', '<C-\\><C-n>', { desc = 'Exit terminal mode' })

-- Window navigation: C-h/j/k/l handled by smart-splits.nvim (navigation.lua)

-- Window management
map('n', '<leader>wv', '<C-w>v', { desc = 'Split vertical' })
map('n', '<leader>ws', '<C-w>s', { desc = 'Split horizontal' })
map('n', '<leader>wc', '<C-w>c', { desc = 'Close window' })
map('n', '<leader>wo', '<C-w>o', { desc = 'Close other windows' })
-- <leader>w= handled by windows.nvim (WindowsEqualize)

-- Delete operations
map('n', '<leader>dw', '<C-w>c', { desc = 'Delete window' })
map('n', '<leader>dW', '<C-w>o', { desc = 'Delete other windows' })

-- Diagnostics (panel mappings in trouble.nvim, ]d/[d built-in in 0.11+)
map('n', '<leader>xn', function()
  vim.diagnostic.jump({ count = 1 })
end, { desc = 'Next diagnostic' })
map('n', '<leader>xp', function()
  vim.diagnostic.jump({ count = -1 })
end, { desc = 'Previous diagnostic' })

-- UI/Toggle options
map('n', '<leader>uw', '<cmd>set wrap!<CR>', { desc = 'Toggle word wrap' })
-- <leader>un handled by snacks.nvim (dismiss notifications)
map('n', '<leader>ur', '<cmd>set relativenumber!<CR>', { desc = 'Toggle relative numbers' })
map('n', '<leader>us', '<cmd>set spell!<CR>', { desc = 'Toggle spell check' })

-- Line movement (Alt+j/k)
map('n', '<A-j>', '<cmd>m .+1<CR>==', { desc = 'Move line down' })
map('n', '<A-k>', '<cmd>m .-2<CR>==', { desc = 'Move line up' })
map('i', '<A-j>', '<Esc><cmd>m .+1<CR>==gi', { desc = 'Move line down' })
map('i', '<A-k>', '<Esc><cmd>m .-2<CR>==gi', { desc = 'Move line up' })
map('v', '<A-j>', ":m '>+1<CR>gv=gv", { desc = 'Move selection down' })
map('v', '<A-k>', ":m '<-2<CR>gv=gv", { desc = 'Move selection up' })

-- Blank line insertion
map('n', ']<Space>', 'o<Esc>k', { desc = 'Add blank line below' })
map('n', '[<Space>', 'O<Esc>j', { desc = 'Add blank line above' })

-- Smart join
map('n', '<leader>j', 'J', { desc = 'Join lines' })

-- Quickfix/location navigation
map('n', ']q', '<cmd>cnext<CR>zz', { desc = 'Next quickfix' })
map('n', '[q', '<cmd>cprev<CR>zz', { desc = 'Previous quickfix' })

-- Horizontal scroll (trackpad gestures)
map({ 'n', 'i', 'v' }, '<ScrollWheelLeft>', '3zh')
map({ 'n', 'i', 'v' }, '<ScrollWheelRight>', '3zl')

-- Better visual mode indenting (keep selection)
map('v', '<', '<gv', { desc = 'Indent left' })
map('v', '>', '>gv', { desc = 'Indent right' })

-- Fold operations
map('n', '<leader>za', 'za', { desc = 'Toggle fold' })
map('n', '<leader>zc', 'zc', { desc = 'Close fold' })
map('n', '<leader>zo', 'zo', { desc = 'Open fold' })
map('n', '<leader>zM', 'zM', { desc = 'Close all folds' })
map('n', '<leader>zR', 'zR', { desc = 'Open all folds' })
map('n', '<leader>zj', 'zj', { desc = 'Next fold' })
map('n', '<leader>zk', 'zk', { desc = 'Previous fold' })
