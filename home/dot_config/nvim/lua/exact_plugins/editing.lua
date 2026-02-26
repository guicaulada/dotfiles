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
      {
        '<leader>r',
        function()
          require('substitute').operator()
        end,
        desc = 'Substitute with motion',
      },
      {
        '<leader>rr',
        function()
          require('substitute').line()
        end,
        desc = 'Substitute line',
      },
      {
        '<leader>R',
        function()
          require('substitute').eol()
        end,
        desc = 'Substitute to EOL',
      },
      {
        '<leader>r',
        function()
          require('substitute').visual()
        end,
        mode = 'x',
        desc = 'Substitute selection',
      },
      -- Exchange
      {
        'sx',
        function()
          require('substitute.exchange').operator()
        end,
        desc = 'Exchange with motion',
      },
      {
        'sxx',
        function()
          require('substitute.exchange').line()
        end,
        desc = 'Exchange line',
      },
      {
        'sxc',
        function()
          require('substitute.exchange').cancel()
        end,
        desc = 'Cancel exchange',
      },
      {
        'X',
        function()
          require('substitute.exchange').visual()
        end,
        mode = 'x',
        desc = 'Exchange selection',
      },
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

  -- Multi-cursor editing
  {
    'jake-stewart/multicursor.nvim',
    branch = '1.0',
    config = function()
      local mc = require('multicursor-nvim')
      mc.setup()

      local set = vim.keymap.set

      -- Add cursor above/below (like VSCode Cmd+Alt+Up/Down)
      set({ 'n', 'x' }, '<A-S-Up>', function()
        mc.lineAddCursor(-1)
      end, { desc = 'Add cursor above' })
      set({ 'n', 'x' }, '<A-S-Down>', function()
        mc.lineAddCursor(1)
      end, { desc = 'Add cursor below' })

      -- Match word/selection (like VSCode Cmd+D)
      set({ 'n', 'x' }, '<C-n>', function()
        mc.matchAddCursor(1)
      end, { desc = 'Add next occurrence' })
      set({ 'n', 'x' }, '<C-S-n>', function()
        mc.matchSkipCursor(1)
      end, { desc = 'Skip next occurrence' })

      -- Select all occurrences (like VSCode Cmd+Shift+L)
      set({ 'n', 'x' }, '<C-S-l>', function()
        mc.matchAllAddCursors()
      end, { desc = 'Select all occurrences' })

      -- Keymap layer only active when multiple cursors exist
      mc.addKeymapLayer(function(layerSet)
        layerSet({ 'n', 'x' }, '<Left>', mc.prevCursor)
        layerSet({ 'n', 'x' }, '<Right>', mc.nextCursor)
        layerSet({ 'n', 'x' }, '<leader>x', mc.deleteCursor)
        layerSet('n', '<Esc>', function()
          if not mc.cursorsEnabled() then
            mc.enableCursors()
          else
            mc.clearCursors()
          end
        end)
      end)

      local hl = vim.api.nvim_set_hl
      hl(0, 'MultiCursorCursor', { reverse = true })
      hl(0, 'MultiCursorVisual', { link = 'Visual' })
      hl(0, 'MultiCursorSign', { link = 'SignColumn' })
      hl(0, 'MultiCursorMatchPreview', { link = 'Search' })
      hl(0, 'MultiCursorDisabledCursor', { reverse = true })
      hl(0, 'MultiCursorDisabledVisual', { link = 'Visual' })
      hl(0, 'MultiCursorDisabledSign', { link = 'SignColumn' })
    end,
  },
}
