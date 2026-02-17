return {
  {
    'mrjones2014/smart-splits.nvim',
    lazy = false,
    opts = {},
    keys = {
      { '<C-h>', function() require('smart-splits').move_cursor_left() end, desc = 'Focus left window/pane' },
      { '<C-j>', function() require('smart-splits').move_cursor_down() end, desc = 'Focus lower window/pane' },
      { '<C-k>', function() require('smart-splits').move_cursor_up() end, desc = 'Focus upper window/pane' },
      { '<C-l>', function() require('smart-splits').move_cursor_right() end, desc = 'Focus right window/pane' },
    },
  },
  {
    'folke/flash.nvim',
    event = 'VeryLazy',
    opts = {
      modes = {
        search = { enabled = true },
        char = { enabled = true },
      },
      label = {
        uppercase = false,
        rainbow = { enabled = true },
      },
    },
    keys = {
      { 'gs', function() require('flash').jump() end, mode = { 'n', 'x', 'o' }, desc = 'Flash jump' },
      { 'gS', function() require('flash').treesitter() end, mode = { 'n', 'x', 'o' }, desc = 'Flash treesitter' },
      { 'r', function() require('flash').remote() end, mode = 'o', desc = 'Remote flash' },
      { 'R', function() require('flash').treesitter_search() end, mode = { 'o', 'x' }, desc = 'Treesitter search' },
    },
  },
}
