return {
  -- Git diff viewer
  {
    'sindrets/diffview.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    cmd = { 'DiffviewOpen', 'DiffviewFileHistory' },
    opts = {
      view = {
        merge_tool = { layout = 'diff3_mixed' },
      },
    },
    keys = {
      {
        '<leader>gd',
        function()
          if next(require('diffview.lib').views) == nil then
            vim.cmd('DiffviewOpen')
          else
            vim.cmd('DiffviewClose')
          end
        end,
        desc = 'Toggle Diffview',
      },
      { '<leader>gf', '<cmd>DiffviewFileHistory %<cr>', desc = 'File history' },
      { '<leader>gF', '<cmd>DiffviewFileHistory<cr>', desc = 'Branch history' },
    },
  },

  -- Git signs in gutter
  {
    'lewis6991/gitsigns.nvim',
    event = { 'BufReadPre', 'BufNewFile' },
    opts = {
      signs = {
        add = { text = '┃' },
        change = { text = '┃' },
        delete = { text = '▁' },
        topdelete = { text = '▔' },
        changedelete = { text = '┃' },
        untracked = { text = '┆' },
      },
      signs_staged = {
        add = { text = '┃' },
        change = { text = '┃' },
        delete = { text = '▁' },
        topdelete = { text = '▔' },
        changedelete = { text = '┃' },
      },
      signs_staged_enable = true,
      current_line_blame = true,
      current_line_blame_opts = {
        virt_text = true,
        virt_text_pos = 'eol',
        delay = 500,
      },
      on_attach = function(bufnr)
        local gs = require('gitsigns')
        local map = function(mode, l, r, desc)
          vim.keymap.set(mode, l, r, { buffer = bufnr, desc = desc })
        end

        -- Navigation
        map('n', ']h', function()
          if vim.wo.diff then
            vim.cmd.normal({ ']c', bang = true })
          else
            gs.nav_hunk('next')
          end
        end, 'Next hunk')
        map('n', '[h', function()
          if vim.wo.diff then
            vim.cmd.normal({ '[c', bang = true })
          else
            gs.nav_hunk('prev')
          end
        end, 'Previous hunk')

        -- Stage group actions
        map('n', '<leader>ss', gs.stage_hunk, 'Stage hunk')
        map('n', '<leader>sr', gs.reset_hunk, 'Reset hunk')
        map('v', '<leader>ss', function()
          gs.stage_hunk({ vim.fn.line('.'), vim.fn.line('v') })
        end, 'Stage hunk')
        map('v', '<leader>sr', function()
          gs.reset_hunk({ vim.fn.line('.'), vim.fn.line('v') })
        end, 'Reset hunk')
        map('n', '<leader>sS', gs.stage_buffer, 'Stage buffer')
        map('n', '<leader>su', gs.undo_stage_hunk, 'Undo stage hunk')
        map('n', '<leader>sR', gs.reset_buffer, 'Reset buffer')
        map('n', '<leader>sp', gs.preview_hunk, 'Preview hunk')
        map('n', '<leader>sI', gs.preview_hunk_inline, 'Preview hunk inline')
        map('n', '<leader>sb', function()
          gs.blame_line({ full = true })
        end, 'Blame line')
        map('n', '<leader>sB', gs.toggle_current_line_blame, 'Toggle line blame')
        map('n', '<leader>sd', gs.diffthis, 'Diff this')
        map('n', '<leader>sD', function()
          gs.diffthis('~')
        end, 'Diff this ~')
        map('n', '<leader>sw', gs.toggle_word_diff, 'Toggle word diff')
        map('n', '<leader>sq', function()
          gs.setqflist('all')
        end, 'Send hunks to quickfix')

        -- UI toggles (keep line blame toggle in UI group too)
        map('n', '<leader>ub', gs.toggle_current_line_blame, 'Toggle line blame')

        -- Text object
        map({ 'o', 'x' }, 'ih', ':<C-U>Gitsigns select_hunk<CR>', 'Select hunk')
      end,
    },
  },
}
