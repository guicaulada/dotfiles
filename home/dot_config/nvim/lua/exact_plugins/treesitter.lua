return {
  {
    'nvim-treesitter/nvim-treesitter',
    build = ':TSUpdate',
    dependencies = {
      'nvim-treesitter/nvim-treesitter-textobjects',
    },
    config = function()
      local filetypes = {
        'bash',
        'c',
        'diff',
        'html',
        'lua',
        'luadoc',
        'markdown',
        'markdown_inline',
        'query',
        'vim',
        'vimdoc',
        -- TypeScript/JavaScript
        'typescript',
        'tsx',
        'javascript',
        'jsdoc',
        -- Rust
        'rust',
        -- Python
        'python',
        -- Go
        'go',
        'gomod',
        'gosum',
        'gowork',
        -- Jsonnet
        'jsonnet',
        -- Terraform/HCL
        'terraform',
        'hcl',
        -- Docker
        'dockerfile',
        -- Common formats
        'json',
        'yaml',
        'toml',
        -- Just (justfile)
        'just',
        -- Nix
        'nix',
        -- Go templates
        'gotmpl',
      }
      require('nvim-treesitter').install(filetypes)
      vim.api.nvim_create_autocmd('FileType', {
        pattern = filetypes,
        callback = function()
          vim.treesitter.start()
        end,
      })

      -- Configure treesitter-textobjects
      require('nvim-treesitter-textobjects').setup({
        select = {
          lookahead = true,
          selection_modes = {
            ['@parameter.outer'] = 'v',
            ['@function.outer'] = 'V',
            ['@class.outer'] = 'V',
          },
        },
        move = {
          set_jumps = true,
        },
        swap = {
          enable = true,
        },
      })

      -- Text object keymaps
      local ts_select = require('nvim-treesitter-textobjects.select')
      vim.keymap.set({ 'x', 'o' }, 'af', function()
        ts_select.select_textobject('@function.outer', 'textobjects')
      end, { desc = 'Around function' })
      vim.keymap.set({ 'x', 'o' }, 'if', function()
        ts_select.select_textobject('@function.inner', 'textobjects')
      end, { desc = 'Inside function' })
      vim.keymap.set({ 'x', 'o' }, 'ac', function()
        ts_select.select_textobject('@class.outer', 'textobjects')
      end, { desc = 'Around class' })
      vim.keymap.set({ 'x', 'o' }, 'ic', function()
        ts_select.select_textobject('@class.inner', 'textobjects')
      end, { desc = 'Inside class' })
      vim.keymap.set({ 'x', 'o' }, 'aa', function()
        ts_select.select_textobject('@parameter.outer', 'textobjects')
      end, { desc = 'Around argument' })
      vim.keymap.set({ 'x', 'o' }, 'ia', function()
        ts_select.select_textobject('@parameter.inner', 'textobjects')
      end, { desc = 'Inside argument' })

      -- Movement keymaps
      local ts_move = require('nvim-treesitter-textobjects.move')
      vim.keymap.set({ 'n', 'x', 'o' }, ']m', function()
        ts_move.goto_next_start('@function.outer', 'textobjects')
      end, { desc = 'Next method start' })
      vim.keymap.set({ 'n', 'x', 'o' }, '[m', function()
        ts_move.goto_previous_start('@function.outer', 'textobjects')
      end, { desc = 'Prev method start' })
      vim.keymap.set({ 'n', 'x', 'o' }, ']M', function()
        ts_move.goto_next_end('@function.outer', 'textobjects')
      end, { desc = 'Next method end' })
      vim.keymap.set({ 'n', 'x', 'o' }, '[M', function()
        ts_move.goto_previous_end('@function.outer', 'textobjects')
      end, { desc = 'Prev method end' })
      vim.keymap.set({ 'n', 'x', 'o' }, ']]', function()
        ts_move.goto_next_start('@class.outer', 'textobjects')
      end, { desc = 'Next class start' })
      vim.keymap.set({ 'n', 'x', 'o' }, '[[', function()
        ts_move.goto_previous_start('@class.outer', 'textobjects')
      end, { desc = 'Prev class start' })
      vim.keymap.set({ 'n', 'x', 'o' }, ']i', function()
        ts_move.goto_next_start('@conditional.outer', 'textobjects')
      end, { desc = 'Next conditional' })
      vim.keymap.set({ 'n', 'x', 'o' }, '[i', function()
        ts_move.goto_previous_start('@conditional.outer', 'textobjects')
      end, { desc = 'Prev conditional' })
      vim.keymap.set({ 'n', 'x', 'o' }, ']l', function()
        ts_move.goto_next_start('@loop.outer', 'textobjects')
      end, { desc = 'Next loop' })
      vim.keymap.set({ 'n', 'x', 'o' }, '[l', function()
        ts_move.goto_previous_start('@loop.outer', 'textobjects')
      end, { desc = 'Prev loop' })

      -- Move (swap) keymaps
      local ts_swap = require('nvim-treesitter-textobjects.swap')
      vim.keymap.set('n', '<leader>ma', function()
        ts_swap.swap_next('@parameter.inner')
      end, { desc = 'Move next argument' })
      vim.keymap.set('n', '<leader>mA', function()
        ts_swap.swap_previous('@parameter.inner')
      end, { desc = 'Move prev argument' })
      vim.keymap.set('n', '<leader>mp', function()
        ts_swap.swap_next('@property.outer')
      end, { desc = 'Move next property' })
      vim.keymap.set('n', '<leader>mP', function()
        ts_swap.swap_previous('@property.outer')
      end, { desc = 'Move prev property' })
      vim.keymap.set('n', '<leader>mf', function()
        ts_swap.swap_next('@function.outer')
      end, { desc = 'Move next function' })
      vim.keymap.set('n', '<leader>mF', function()
        ts_swap.swap_previous('@function.outer')
      end, { desc = 'Move prev function' })
    end,
  },
  {
    'nvim-treesitter/nvim-treesitter-context',
    event = 'BufReadPre',
    opts = { max_lines = 3 },
  },
}
