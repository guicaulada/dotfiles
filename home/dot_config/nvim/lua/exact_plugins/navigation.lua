return {
  {
    'mrjones2014/smart-splits.nvim',
    lazy = false,
    config = function()
      local ss = require('smart-splits')
      ss.setup({ at_edge = 'wrap' })
      vim.keymap.set('n', '<C-h>', ss.move_cursor_left, { desc = 'Focus left split/pane' })
      vim.keymap.set('n', '<C-j>', ss.move_cursor_down, { desc = 'Focus lower split/pane' })
      vim.keymap.set('n', '<C-k>', ss.move_cursor_up, { desc = 'Focus upper split/pane' })
      vim.keymap.set('n', '<C-l>', ss.move_cursor_right, { desc = 'Focus right split/pane' })
      vim.keymap.set('n', '<A-h>', ss.resize_left, { desc = 'Resize left' })
      vim.keymap.set('n', '<A-j>', ss.resize_down, { desc = 'Resize down' })
      vim.keymap.set('n', '<A-k>', ss.resize_up, { desc = 'Resize up' })
      vim.keymap.set('n', '<A-l>', ss.resize_right, { desc = 'Resize right' })
    end,
  },
  {
    'folke/flash.nvim',
    event = 'VeryLazy',
    opts = {
      modes = {
        search = { enabled = false },
        char = { enabled = true },
      },
      label = {
        uppercase = false,
        rainbow = { enabled = true },
      },
    },
    keys = {
      {
        'gs',
        function()
          require('flash').jump()
        end,
        mode = { 'n', 'x', 'o' },
        desc = 'Flash jump',
      },
      {
        'gS',
        function()
          require('flash').treesitter()
        end,
        mode = { 'n', 'x', 'o' },
        desc = 'Flash treesitter',
      },
      {
        'r',
        function()
          require('flash').remote()
        end,
        mode = 'o',
        desc = 'Remote flash',
      },
      {
        'R',
        function()
          require('flash').treesitter_search()
        end,
        mode = { 'o', 'x' },
        desc = 'Treesitter search',
      },
    },
  },
}
