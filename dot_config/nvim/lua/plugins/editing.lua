return {
  -- Substitute and exchange text
  {
    'gbprod/substitute.nvim',
    event = { 'BufReadPre', 'BufNewFile' },
    opts = {
      highlight_substituted_text = { enabled = true, timer = 500 },
      exchange = { motion = false, use_esc_to_cancel = true },
    },
    keys = {
      { '<leader>r', function() require('substitute').operator() end, desc = 'Substitute with motion' },
      { '<leader>rr', function() require('substitute').line() end, desc = 'Substitute line' },
      { '<leader>R', function() require('substitute').eol() end, desc = 'Substitute to EOL' },
      { '<leader>r', function() require('substitute').visual() end, mode = 'x', desc = 'Substitute selection' },
      -- Exchange
      { 'sx', function() require('substitute.exchange').operator() end, desc = 'Exchange with motion' },
      { 'sxx', function() require('substitute.exchange').line() end, desc = 'Exchange line' },
      { 'sxc', function() require('substitute.exchange').cancel() end, desc = 'Cancel exchange' },
      { 'X', function() require('substitute.exchange').visual() end, mode = 'x', desc = 'Exchange selection' },
    },
  },

  -- Easy alignment
  {
    'junegunn/vim-easy-align',
    event = 'VeryLazy',
    keys = {
      { 'ga', '<Plug>(EasyAlign)', mode = { 'n', 'x' }, desc = 'Easy align' },
    },
  },
}
