return {
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
