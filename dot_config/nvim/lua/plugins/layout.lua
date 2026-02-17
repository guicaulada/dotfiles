return {
  {
    'folke/edgy.nvim',
    enabled = false,
    event = 'VeryLazy',
    opts = {
      left = {
        { title = 'Files', ft = 'snacks_explorer', size = { width = 30 } },
        { title = 'Test Summary', ft = 'neotest-summary', size = { width = 0.2 } },
      },
      bottom = {
        { ft = 'qf', title = 'QuickFix', size = { height = 0.3 } },
        { ft = 'help', title = 'Help', size = { height = 0.4 } },
        { title = 'Test Output', ft = 'neotest-output-panel', size = { height = 0.3 } },
      },
      animate = { enabled = false },
    },
    keys = {
      { '<leader>we', function() require('edgy').toggle() end, desc = 'Toggle edgy' },
      { '<leader>wE', function() require('edgy').select() end, desc = 'Select edgy window' },
    },
  },
}
