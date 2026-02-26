local map = vim.keymap.set

map('n', '<Esc>', '<cmd>nohlsearch<CR>')
map('t', '<Esc><Esc>', '<C-\\><C-n>', { desc = 'Exit terminal mode' })

-- Window navigation: C-h/j/k/l handled by smart-splits.nvim (navigation.lua)

-- Window management
map('n', '<leader>wv', '<C-w>v', { desc = 'Split vertical' })
map('n', '<leader>ws', '<C-w>s', { desc = 'Split horizontal' })
map('n', '<leader>wc', '<C-w>c', { desc = 'Close window' })
map('n', '<leader>wo', '<C-w>o', { desc = 'Close other windows' })
map('n', '<leader>wr', '<C-w>r', { desc = 'Rotate windows' })
map('n', '<leader>wx', '<C-w>x', { desc = 'Swap windows' })
-- <leader>w= handled by windows.nvim (WindowsEqualize)

-- UI/Toggle options
map('n', '<leader>uw', '<cmd>set wrap!<CR>', { desc = 'Toggle word wrap' })
-- <leader>un handled by snacks.nvim (dismiss notifications)
map('n', '<leader>ur', '<cmd>set relativenumber!<CR>', { desc = 'Toggle relative numbers' })
map('n', '<leader>us', '<cmd>set spell!<CR>', { desc = 'Toggle spell check' })

-- Line movement (Alt+Arrow)
map('n', '<A-Down>', '<cmd>m .+1<CR>==', { desc = 'Move line down' })
map('n', '<A-Up>', '<cmd>m .-2<CR>==', { desc = 'Move line up' })
map('i', '<A-Down>', '<Esc><cmd>m .+1<CR>==gi', { desc = 'Move line down' })
map('i', '<A-Up>', '<Esc><cmd>m .-2<CR>==gi', { desc = 'Move line up' })
map('v', '<A-Down>', ":m '>+1<CR>gv=gv", { desc = 'Move selection down' })
map('v', '<A-Up>', ":m '<-2<CR>gv=gv", { desc = 'Move selection up' })

-- Blank line insertion
map('n', ']<Space>', 'o<Esc>k', { desc = 'Add blank line below' })
map('n', '[<Space>', 'O<Esc>j', { desc = 'Add blank line above' })

-- Quickfix/location navigation
map('n', ']q', '<cmd>cnext<CR>zz', { desc = 'Next quickfix' })
map('n', '[q', '<cmd>cprev<CR>zz', { desc = 'Previous quickfix' })

-- Horizontal scroll (trackpad gestures)
map({ 'n', 'v' }, '<ScrollWheelLeft>', '3zh')
map({ 'n', 'v' }, '<ScrollWheelRight>', '3zl')
map('i', '<ScrollWheelLeft>', '<C-o>3zh')
map('i', '<ScrollWheelRight>', '<C-o>3zl')

-- Better visual mode indenting (keep selection)
map('v', '<', '<gv', { desc = 'Indent left' })
map('v', '>', '>gv', { desc = 'Indent right' })

-- Fold operations
map('n', '<leader>za', 'za', { desc = 'Toggle fold' })
map('n', '<leader>zc', 'zc', { desc = 'Close fold' })
map('n', '<leader>zo', 'zo', { desc = 'Open fold' })
map('n', '<leader>zM', 'zM', { desc = 'Close all folds' })
map('n', '<leader>zR', 'zR', { desc = 'Open all folds' })
map('n', '<leader>z<Down>', 'zj', { desc = 'Next fold' })
map('n', '<leader>z<Up>', 'zk', { desc = 'Previous fold' })
map('n', '<leader>zd', 'zd', { desc = 'Delete fold under cursor' })
map('n', '<leader>zi', 'zi', { desc = 'Toggle foldenable' })
