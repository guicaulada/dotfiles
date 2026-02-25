return {
  {
    'folke/sidekick.nvim',
    opts = {
      cli = {
        mux = {
          enabled = true,
          backend = 'tmux',
        },
      },
    },
    keys = {
      {
        '<c-.>',
        function()
          require('sidekick.cli').toggle()
        end,
        mode = { 'n', 't', 'i', 'x' },
        desc = 'Sidekick Toggle',
      },
      { '<leader>a', '', desc = '+AI', mode = { 'n', 'v' } },
      {
        '<leader>aa',
        function()
          require('sidekick.cli').toggle()
        end,
        desc = 'Toggle CLI',
      },
      {
        '<leader>as',
        function()
          require('sidekick.cli').select()
        end,
        desc = 'Select CLI',
      },
      {
        '<leader>ad',
        function()
          require('sidekick.cli').close()
        end,
        desc = 'Detach CLI session',
      },
      {
        '<leader>at',
        function()
          require('sidekick.cli').send({ msg = '{this}' })
        end,
        mode = { 'x', 'n' },
        desc = 'Send this',
      },
      {
        '<leader>af',
        function()
          require('sidekick.cli').send({ msg = '{file}' })
        end,
        desc = 'Send file',
      },
      {
        '<leader>av',
        function()
          require('sidekick.cli').send({ msg = '{selection}' })
        end,
        mode = { 'x' },
        desc = 'Send selection',
      },
      {
        '<leader>ap',
        function()
          require('sidekick.cli').prompt()
        end,
        mode = { 'n', 'x' },
        desc = 'Select prompt',
      },
    },
  },
}
