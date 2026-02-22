return {
  {
    'nvim-neotest/neotest',
    dependencies = {
      'nvim-neotest/nvim-nio',
      'nvim-lua/plenary.nvim',
      'nvim-treesitter/nvim-treesitter',
      'nvim-neotest/neotest-jest',
      'marilari88/neotest-vitest',
      'nvim-neotest/neotest-go',
      'rouge8/neotest-rust',
      'nvim-neotest/neotest-python',
    },
    keys = {
      {
        '<leader>tt',
        function()
          require('neotest').run.run()
        end,
        desc = 'Run nearest test',
      },
      {
        '<leader>tf',
        function()
          require('neotest').run.run(vim.fn.expand('%'))
        end,
        desc = 'Run file tests',
      },
      {
        '<leader>tl',
        function()
          require('neotest').run.run_last()
        end,
        desc = 'Run last test',
      },
      {
        '<leader>td',
        function()
          require('neotest').run.run({ strategy = 'dap' })
        end,
        desc = 'Debug test',
      },
      {
        '<leader>ts',
        function()
          require('neotest').summary.toggle()
        end,
        desc = 'Toggle test summary',
      },
      {
        '<leader>to',
        function()
          require('neotest').output.open({ enter = true })
        end,
        desc = 'Show test output',
      },
      {
        '<leader>tO',
        function()
          require('neotest').output_panel.toggle()
        end,
        desc = 'Toggle output panel',
      },
      {
        '<leader>ta',
        function()
          require('neotest').run.attach()
        end,
        desc = 'Attach to test output',
      },
      {
        '<leader>tS',
        function()
          require('neotest').run.stop()
        end,
        desc = 'Stop tests',
      },
      {
        '[t',
        function()
          require('neotest').jump.prev({ status = 'failed' })
        end,
        desc = 'Prev failed test',
      },
      {
        ']t',
        function()
          require('neotest').jump.next({ status = 'failed' })
        end,
        desc = 'Next failed test',
      },
    },
    config = function()
      require('neotest').setup({
        adapters = {
          require('neotest-jest')({ jestConfigFile = 'jest.config.js' }),
          require('neotest-vitest'),
          require('neotest-go'),
          require('neotest-rust'),
          require('neotest-python'),
        },
      })
    end,
  },
}
