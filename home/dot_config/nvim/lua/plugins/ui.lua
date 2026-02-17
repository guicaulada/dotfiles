return {
  -- Colorscheme
  {
    'navarasu/onedark.nvim',
    priority = 1000,
    opts = {
      style = 'darker',
      transparent = true,
      term_colors = true,
      code_style = {
        comments = 'italic',
        keywords = 'none',
        functions = 'bold',
        strings = 'none',
        variables = 'none',
      },
      lualine = { transparent = true },
      highlights = {
        CursorLine = { bg = '#2c313a' },
        SnacksIndent = { fg = '#3b4048' },
        SnacksIndentScope = { fg = '#61afef' },
        -- Transparent backgrounds for floating windows and terminals
        NormalFloat = { bg = 'NONE' },
        FloatBorder = { bg = 'NONE' },
        FloatTitle = { bg = 'NONE' },
      },
      diagnostics = {
        darker = true,
        undercurl = true,
        background = true,
      },
    },
    config = function(_, opts)
      require('onedark').setup(opts)
      require('onedark').load()
    end,
  },

  -- Catppuccin colorscheme (for light mode)
  {
    'catppuccin/nvim',
    name = 'catppuccin',
    lazy = true,
    opts = { flavour = 'latte' },
  },

  -- Auto dark mode based on system appearance
  {
    'f-person/auto-dark-mode.nvim',
    opts = {
      update_interval = 1000,
      set_dark_mode = function()
        vim.opt.background = 'dark'
        vim.cmd.colorscheme('onedark')
        local ok, lualine = pcall(require, 'lualine')
        if ok then lualine.setup({ options = { theme = 'onedark' } }) end
      end,
      set_light_mode = function()
        vim.opt.background = 'light'
        vim.cmd.colorscheme('catppuccin-latte')
        local ok, lualine = pcall(require, 'lualine')
        if ok then lualine.setup({ options = { theme = 'catppuccin' } }) end
      end,
    },
  },

  -- Icons
  {
    'nvim-tree/nvim-web-devicons',
    lazy = true,
    opts = {
      default = true,
      strict = true,
      color_icons = true,
    },
  },

  -- Bufferline (tabs for buffers)
  {
    'akinsho/bufferline.nvim',
    version = '*',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    event = 'VeryLazy',
    config = function()
      require('bufferline').setup({
        options = {
          style_preset = require('bufferline').style_preset.minimal,
          mode = 'buffers',
          themable = true,
          numbers = 'none',
          close_command = 'bdelete! %d',
          right_mouse_command = 'bdelete! %d',
          indicator = { style = 'none' },
          buffer_close_icon = '󰅖',
          modified_icon = '●',
          close_icon = '',
          left_trunc_marker = '',
          right_trunc_marker = '',
          max_name_length = 18,
          max_prefix_length = 10,
          truncate_names = true,
          tab_size = 0,
          diagnostics = 'nvim_lsp',
          diagnostics_indicator = function(count, level)
            local icon = level:match('error') and '' or ''
            return icon .. count
          end,
          offsets = {
            {
              filetype = 'snacks_explorer',
              text = 'File Explorer',
              highlight = 'Directory',
              separator = true,
            },
          },
          show_buffer_icons = true,
          show_buffer_close_icons = false,
          show_close_icon = false,
          show_tab_indicators = false,
          separator_style = { '', '' },
          always_show_bufferline = true,
          hover = {
            enabled = true,
            delay = 200,
            reveal = { 'close' },
          },
        },
      })
    end,
    keys = {
      { '<leader>bp', '<cmd>BufferLinePick<cr>', desc = 'Pick buffer' },
      { '<leader>bc', '<cmd>BufferLinePickClose<cr>', desc = 'Pick buffer to close' },
      { '<leader>bP', '<cmd>BufferLineTogglePin<cr>', desc = 'Toggle pin' },
      -- Delete operations moved to delete group
      { '<leader>dl', '<cmd>BufferLineCloseLeft<cr>', desc = 'Delete buffers to left' },
      { '<leader>dr', '<cmd>BufferLineCloseRight<cr>', desc = 'Delete buffers to right' },
      -- Navigation
      { '<S-h>', '<cmd>BufferLineCyclePrev<cr>', desc = 'Previous buffer' },
      { '<S-l>', '<cmd>BufferLineCycleNext<cr>', desc = 'Next buffer' },
      { '[b', '<cmd>BufferLineCyclePrev<cr>', desc = 'Previous buffer' },
      { ']b', '<cmd>BufferLineCycleNext<cr>', desc = 'Next buffer' },
    },
  },

  -- Statusline
  {
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    event = 'VeryLazy',
    opts = {
      options = {
        theme = 'onedark',
        globalstatus = true,
        component_separators = { left = '', right = '' },
        section_separators = { left = '', right = '' },
        disabled_filetypes = { statusline = { 'dashboard', 'alpha', 'lazy', 'snacks_dashboard' } },
      },
      sections = {
        lualine_a = { 'mode' },
        lualine_b = {
          'branch',
          'diff',
          {
            'diagnostics',
            symbols = {
              error = '\u{ea87} ',
              warn = '\u{ea6c} ',
              hint = '\u{f400} ',
              info = '\u{ea74} ',
            },
          },
        },
        lualine_c = { { 'filename', path = 1 } },
        lualine_x = {
          {
            function()
              local clients = vim.lsp.get_clients({ bufnr = 0 })
              if #clients == 0 then
                return ''
              end
              local names = {}
              for _, client in ipairs(clients) do
                table.insert(names, client.name)
              end
              return ' ' .. table.concat(names, ', ')
            end,
            cond = function()
              return #vim.lsp.get_clients({ bufnr = 0 }) > 0
            end,
          },
          'encoding',
          'fileformat',
          'filetype',
        },
        lualine_y = { 'progress' },
        lualine_z = { 'location' },
      },
      extensions = { 'lazy', 'quickfix' },
    },
  },

  -- Snacks.nvim - unified UI components
  -- Replaces: telescope, oil, indent-blankline, nvim-notify, noice, dressing, fidget
  {
    'folke/snacks.nvim',
    priority = 1000,
    lazy = false,
    ---@type snacks.Config
    opts = {
      -- Notifications (replaces nvim-notify, fidget for LSP progress)
      notifier = {
        enabled = true,
        timeout = 3000,
      },
      -- Indent guides (replaces indent-blankline)
      indent = {
        enabled = true,
        char = '│',
        scope = { enabled = true },
      },
      -- Better vim.ui.input
      input = { enabled = true },
      -- Performance
      bigfile = { enabled = true },
      quickfile = { enabled = true },
      -- Buffer management
      bufdelete = { enabled = true },
      -- Git integration
      lazygit = { enabled = true },
      gitbrowse = { enabled = true },
      git = { enabled = true },
      -- Focus & zen
      zen = { enabled = true },
      dim = { enabled = true },
      -- LSP enhancements
      words = { enabled = true },
      rename = { enabled = true },
      scope = { enabled = true },
      -- Utilities
      scratch = { enabled = true },
      terminal = { enabled = true },
      toggle = { enabled = true },
      scroll = { enabled = true },
      statuscolumn = { enabled = true },
      image = { enabled = true },
      -- Debug & profiling
      debug = { enabled = true },
      profiler = { enabled = true },
      -- Dashboard
      dashboard = {
        enabled = true,
        preset = {
          keys = {
            { icon = ' ', key = 'f', desc = 'Find File', action = ':lua Snacks.picker.files()' },
            { icon = ' ', key = 'n', desc = 'New File', action = ':ene | startinsert' },
            { icon = ' ', key = 'g', desc = 'Find Text', action = ':lua Snacks.picker.grep()' },
            { icon = ' ', key = 'r', desc = 'Recent Files', action = ':lua Snacks.picker.recent()' },
            { icon = ' ', key = 'c', desc = 'Config', action = ':lua Snacks.picker.files({ cwd = vim.fn.stdpath("config") })' },
            { icon = ' ', key = 's', desc = 'Restore Session', action = ':AutoSession restore' },
            { icon = '󰒲 ', key = 'l', desc = 'Lazy', action = ':Lazy' },
            { icon = ' ', key = 'q', desc = 'Quit', action = ':qa' },
          },
        },
        sections = {
          { section = 'header' },
          { section = 'keys', gap = 1, padding = 1 },
          { section = 'startup' },
        },
      },
      -- File explorer (replaces oil.nvim)
      explorer = {
        enabled = true,
        replace_netrw = false,
      },
      -- Picker (replaces telescope)
      picker = {
        enabled = true,
        sources = {
          files = { hidden = true },
          grep = { hidden = true },
          explorer = {
            hidden = true,
            layout = { preset = 'sidebar', layout = { width = 30 } },
          },
        },
        win = {
          input = {
            keys = {
              ['<c-t>'] = { 'edit_tab', mode = { 'i', 'n' } },
              ['<c-s>'] = { 'edit_split', mode = { 'i', 'n' } },
              ['<c-v>'] = { 'edit_vsplit', mode = { 'i', 'n' } },
            },
          },
        },
      },
    },
    keys = {
      -- Find group (picker/telescope replacement)
      { '<leader>ff', function() Snacks.picker.files() end, desc = 'Find files' },
      { '<leader>fg', function() Snacks.picker.grep() end, desc = 'Find grep' },
      { '<leader>fw', function() Snacks.picker.grep_word() end, desc = 'Find word', mode = { 'n', 'v' } },
      { '<leader>fh', function() Snacks.picker.help() end, desc = 'Find help' },
      { '<leader>fk', function() Snacks.picker.keymaps() end, desc = 'Find keymaps' },
      { '<leader>fp', function() Snacks.picker() end, desc = 'Find picker' },
      { '<leader>fd', function() Snacks.picker.diagnostics() end, desc = 'Find diagnostics' },
      { '<leader>fr', function() Snacks.picker.resume() end, desc = 'Find resume' },
      { '<leader>f.', function() Snacks.picker.recent() end, desc = 'Find recent files' },
      { '<leader>fc', function() Snacks.picker.commands() end, desc = 'Find commands' },
      { '<leader>fb', function() Snacks.picker.buffers() end, desc = 'Find buffers' },
      { '<leader><leader>', function() Snacks.picker.buffers() end, desc = 'Find buffers' },
      { '<leader>/', function() Snacks.picker.lines() end, desc = 'Fuzzily search in buffer' },
      { '<leader>f/', function() Snacks.picker.grep_buffers() end, desc = 'Find in open files' },
      { '<leader>fn', function() Snacks.picker.files({ cwd = vim.fn.stdpath('config') }) end, desc = 'Find neovim files' },
      { '<leader>ft', function() Snacks.picker.todo_comments() end, desc = 'Find TODOs' },
      -- Git pickers
      { '<leader>gc', function() Snacks.picker.git_log() end, desc = 'Git commits' },
      { '<leader>gs', function() Snacks.picker.git_status() end, desc = 'Git status' },
      { '<leader>gb', function() Snacks.picker.git_branches() end, desc = 'Git branches' },
      -- LSP pickers
      { 'grr', function() Snacks.picker.lsp_references() end, desc = 'LSP references' },
      { 'gri', function() Snacks.picker.lsp_implementations() end, desc = 'LSP implementations' },
      { 'grd', function() Snacks.picker.lsp_definitions() end, desc = 'LSP definitions' },
      { 'grt', function() Snacks.picker.lsp_type_definitions() end, desc = 'LSP type definitions' },
      { 'gO', function() Snacks.picker.lsp_symbols() end, desc = 'LSP document symbols' },
      { 'gW', function() Snacks.picker.lsp_workspace_symbols() end, desc = 'LSP workspace symbols' },
      -- Explorer (oil replacement)
      { '<leader>e', function() Snacks.explorer() end, desc = 'File explorer' },
      { '<leader>E', function() Snacks.explorer.open({ win = { style = 'float' } }) end, desc = 'File explorer (float)' },
      { '-', function() Snacks.explorer() end, desc = 'File explorer' },
      -- UI/Toggles
      { '<leader>un', function() Snacks.notifier.hide() end, desc = 'Dismiss notifications' },
      { '<leader>uN', function() Snacks.notifier.show_history() end, desc = 'Notification history' },
      { '<leader>uz', function() Snacks.zen() end, desc = 'Toggle zen mode' },
      { '<leader>ud', function() Snacks.dim() end, desc = 'Toggle dim mode' },
      -- Delete group
      { '<leader>db', function() Snacks.bufdelete() end, desc = 'Delete buffer' },
      { '<leader>dB', function() Snacks.bufdelete.other() end, desc = 'Delete other buffers' },
      { '<leader>-', function() Snacks.bufdelete() end, desc = 'Delete current buffer' },
      -- Open group
      { '<leader>og', function() Snacks.lazygit() end, desc = 'Open Lazygit' },
      { '<leader>ol', function() Snacks.lazygit.log() end, desc = 'Open Lazygit log' },
      { '<leader>ot', function() Snacks.terminal() end, desc = 'Open terminal' },
      { '<leader>oe', function() Snacks.explorer() end, desc = 'Open explorer' },
      { '<leader>oE', function() Snacks.explorer.open({ win = { style = 'float' } }) end, desc = 'Open explorer (float)' },
      { '<leader>os', function() Snacks.scratch() end, desc = 'Open scratch buffer' },
      { '<leader>oS', function() Snacks.scratch.select() end, desc = 'Open scratch picker' },
      -- Git (keep some in git group too)
      { '<leader>gB', function() Snacks.gitbrowse() end, desc = 'Browse in browser' },
      { '<leader>gL', function() Snacks.git.blame_line() end, desc = 'Git blame line' },
      -- Terminal
      { '<C-/>', function() Snacks.terminal() end, desc = 'Toggle terminal', mode = { 'n', 't' } },
      -- LSP words navigation
      { ']r', function() Snacks.words.jump(vim.v.count1) end, desc = 'Next reference' },
      { '[r', function() Snacks.words.jump(-vim.v.count1) end, desc = 'Prev reference' },
      -- Profile group
      { '<leader>ps', function() Snacks.debug.stats() end, desc = 'Profile stats' },
      { '<leader>pp', function() Snacks.profiler.toggle() end, desc = 'Toggle profiler' },
      { '<leader>ph', function() Snacks.profiler.highlight() end, desc = 'Profiler highlight' },
      -- Buffer operations (keep some in buffer group)
      { '<leader>bp', '<cmd>BufferLinePick<cr>', desc = 'Pick buffer' },
    },
  },

  -- Floating filename labels (useful in splits)
  {
    'b0o/incline.nvim',
    event = 'BufReadPre',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    opts = {
      window = {
        placement = { horizontal = 'right', vertical = 'top' },
        margin = { horizontal = 0, vertical = 0 },
        padding = 1,
        winhighlight = { Normal = 'NormalFloat' },
      },
      hide = {
        cursorline = true,
        only_win = true, -- Hide when only one window
      },
      render = function(props)
        local filename = vim.fn.fnamemodify(vim.api.nvim_buf_get_name(props.buf), ':t')
        if filename == '' then
          filename = '[No Name]'
        end
        local ft_icon, ft_color = require('nvim-web-devicons').get_icon_color(filename)
        local modified = vim.bo[props.buf].modified and ' ●' or ''
        return {
          { ft_icon or '', guifg = ft_color },
          { ' ' .. filename, gui = props.focused and 'bold' or 'none' },
          { modified, guifg = '#e5c07b' },
        }
      end,
    },
  },
}
