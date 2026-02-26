return {
  { 'NMAC427/guess-indent.nvim', opts = {} },

  {
    'folke/which-key.nvim',
    event = 'VimEnter',
    opts = {
      delay = 0,
      icons = {
        mappings = vim.g.have_nerd_font,
        keys = vim.g.have_nerd_font and {} or {
          Up = '<Up> ',
          Down = '<Down> ',
          Left = '<Left> ',
          Right = '<Right> ',
          C = '<C-…> ',
          M = '<M-…> ',
          D = '<D-…> ',
          S = '<S-…> ',
          CR = '<CR> ',
          Esc = '<Esc> ',
          ScrollWheelDown = '<ScrollWheelDown> ',
          ScrollWheelUp = '<ScrollWheelUp> ',
          NL = '<NL> ',
          BS = '<BS> ',
          Space = '<Space> ',
          Tab = '<Tab> ',
          F1 = '<F1>',
          F2 = '<F2>',
          F3 = '<F3>',
          F4 = '<F4>',
          F5 = '<F5>',
          F6 = '<F6>',
          F7 = '<F7>',
          F8 = '<F8>',
          F9 = '<F9>',
          F10 = '<F10>',
          F11 = '<F11>',
          F12 = '<F12>',
        },
      },
      spec = {
        -- Leader groups
        { '<leader>f', group = 'Find', icon = ' ', mode = { 'n', 'v' } },
        { '<leader>h', group = 'Hunk', icon = ' ', mode = { 'n', 'v' } },
        { '<leader>g', group = 'Git', icon = '' },
        { '<leader>t', group = 'Test', icon = ' ' },
        { '<leader>u', group = 'UI', icon = ' ' },
        { '<leader>c', group = 'Code', icon = ' ' },

        { '<leader>o', group = 'Open', icon = ' ' },
        { '<leader>w', group = 'Window', icon = ' ' },
        { '<leader>b', group = 'Buffer', icon = ' ' },
        { '<leader>x', group = 'Diagnostics', icon = ' ' },
        { '<leader>m', group = 'Move', icon = '󰆾 ' },
        { '<leader>r', group = 'Replace', icon = '' },
        { '<leader>a', group = 'AI', icon = '' },
        { '<leader>q', group = 'Session', icon = ' ' },
        { '<leader>z', group = 'Fold', icon = ' ' },
        { '<leader>p', group = 'Profile', icon = ' ' },

        -- File explorer
        { '<leader>e', desc = 'File explorer', icon = ' ' },
        { '<leader>E', desc = 'File explorer (float)', icon = ' ' },

        -- Quick access
        { '<leader>-', desc = 'Delete current buffer', icon = '󰅖 ' },
        { '<leader>/', desc = 'Fuzzy search buffer', icon = ' ' },
        { '<leader><leader>', desc = 'Find buffers', icon = ' ' },

        -- LSP gr* mappings
        { 'gr', group = 'LSP', icon = ' ' },
        { 'grn', desc = 'Rename' },
        { 'gra', desc = 'Code action' },
        { 'grr', desc = 'References' },
        { 'gri', desc = 'Implementation' },
        { 'grd', desc = 'Definition' },
        { 'grt', desc = 'Type definition' },
        { 'grD', desc = 'Declaration' },

        -- Go to
        { 'g', group = 'Go to', icon = '󰞘 ' },
        { 'gO', desc = 'Document symbols' },
        { 'gW', desc = 'Workspace symbols' },

        -- Navigation brackets
        { ']', group = 'Next', icon = ' ' },
        { '[', group = 'Previous', icon = ' ' },
        { ']h', desc = 'Next hunk' },
        { '[h', desc = 'Previous hunk' },
        { ']q', desc = 'Next quickfix' },
        { '[q', desc = 'Previous quickfix' },
        { ']<Space>', desc = 'Add blank line below' },
        { '[<Space>', desc = 'Add blank line above' },
        { ']d', desc = 'Next diagnostic' },
        { '[d', desc = 'Previous diagnostic' },
        { ']m', desc = 'Next method start' },
        { '[m', desc = 'Prev method start' },
        { ']]', desc = 'Next class start' },
        { '[[', desc = 'Prev class start' },
        { ']i', desc = 'Next conditional' },
        { '[i', desc = 'Prev conditional' },
        { ']l', desc = 'Next loop/loclist' },
        { '[l', desc = 'Prev loop/loclist' },
        { ']r', desc = 'Next reference' },
        { '[r', desc = 'Prev reference' },

        -- Window navigation
        { '<C-h>', desc = 'Focus left window', icon = ' ' },
        { '<C-j>', desc = 'Focus lower window', icon = ' ' },
        { '<C-k>', desc = 'Focus upper window', icon = ' ' },
        { '<C-l>', desc = 'Focus right window', icon = ' ' },

        -- Text objects
        { 'i', group = 'Inside', mode = { 'o', 'x' } },
        { 'a', group = 'Around', mode = { 'o', 'x' } },
      },
    },
    keys = {
      {
        '<leader>?',
        function()
          require('which-key').show({ global = false })
        end,
        desc = 'Buffer keymaps',
      },
    },
  },

  {
    'folke/todo-comments.nvim',
    event = 'VimEnter',
    dependencies = { 'nvim-lua/plenary.nvim' },
    opts = { signs = false },
  },

  {
    'nvim-mini/mini.nvim',
    config = function()
      require('mini.ai').setup({ n_lines = 500 })
      require('mini.surround').setup()
    end,
  },

  -- Maximize/restore splits (native implementation)
  {
    'anuvyklack/windows.nvim',
    dependencies = { 'anuvyklack/middleclass' },
    event = 'WinNew',
    keys = {
      { '<leader>wm', '<cmd>WindowsMaximize<CR>', desc = 'Toggle maximize' },
      { '<leader>w=', '<cmd>WindowsEqualize<CR>', desc = 'Equalize windows' },
    },
    config = function()
      vim.o.winwidth = 10
      vim.o.winminwidth = 10
      vim.o.equalalways = false
      require('windows').setup({
        autowidth = { enable = false },
        animation = { enable = false },
      })
    end,
  },

  -- Undo tree visualization
  {
    'jiaoshijie/undotree',
    dependencies = { 'nvim-lua/plenary.nvim' },
    keys = {
      {
        '<leader>ou',
        function()
          require('undotree').toggle()
        end,
        desc = 'Open undo tree',
      },
    },
    opts = {
      position = 'right',
      window = { winblend = 0 },
    },
  },

  -- Edit files as sudo
  {
    'lambdalisue/vim-suda',
    event = { 'BufRead', 'BufNewFile' },
    cmd = { 'SudaRead', 'SudaWrite' },
    config = function()
      vim.g.suda_smart_edit = 1
    end,
  },
}
