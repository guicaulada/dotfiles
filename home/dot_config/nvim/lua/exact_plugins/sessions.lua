-- Session management for automatic save/restore (VSCode-like behavior)
return {
  'rmagatti/auto-session',
  lazy = false, -- Load immediately for session restoration
  priority = 1000, -- Load early to capture argv before other plugins transform it
  init = function()
    -- Disable netrw - we'll handle directories with snacks explorer
    vim.g.loaded_netrw = 1
    vim.g.loaded_netrwPlugin = 1

    -- Track if we're restoring a session
    vim.g.session_restoring = false

    -- Open snacks explorer for directories (but not during session restore)
    vim.api.nvim_create_autocmd('BufEnter', {
      callback = function(args)
        if vim.g.session_restoring then
          return
        end
        local bufname = vim.api.nvim_buf_get_name(args.buf)
        if bufname ~= '' and vim.fn.isdirectory(bufname) == 1 then
          -- Delete the directory buffer and open explorer
          vim.api.nvim_buf_delete(args.buf, { force = true })
          vim.schedule(function()
            if package.loaded['snacks'] then
              require('snacks').explorer()
            end
          end)
        end
      end,
    })

    -- Open explorer on fresh start (no session restored)
    vim.api.nvim_create_autocmd('VimEnter', {
      callback = function()
        -- Delay to allow session restore to happen first
        vim.defer_fn(function()
          -- Only open if no session was restored and explorer not already open
          if not vim.g.session_restored then
            if package.loaded['snacks'] then
              require('snacks').explorer()
            end
          end
        end, 100)
      end,
    })
  end,
  config = function()
    -- Recommended sessionoptions for proper session saving
    vim.o.sessionoptions = 'blank,buffers,curdir,folds,help,tabpages,winsize,winpos,localoptions'

    require('auto-session').setup({
      -- Automatically save session on exit
      auto_save = true,
      -- Automatically restore session when opening nvim in a directory
      auto_restore = true,
      -- Automatically create session if none exists
      auto_create = true,
      -- Directories where sessions should not be created/restored
      suppressed_dirs = { '~/', '~/Downloads', '~/Desktop', '/' },
      -- Disable git branch in session name (causes auto-save bug when no session exists)
      git_use_branch_name = false,
      -- Allow auto-save when launched with file/directory arguments (needed for oil.nvim compatibility)
      args_allow_files_auto_save = true,
      -- Close unsupported windows (like nvim-tree, neo-tree) before saving
      close_unsupported_windows = true,
      -- Bypass saving when only these filetypes are open
      bypass_save_filetypes = { 'alpha', 'dashboard', 'lazy', 'netrw', 'snacks_dashboard', 'snacks_explorer' },
      -- Set flag before restoring to prevent snacks explorer race
      pre_restore_cmds = {
        function()
          vim.g.session_restoring = true
        end,
      },
      -- Close snacks explorer and wipe buffer before saving
      pre_save_cmds = {
        function()
          for _, buf in ipairs(vim.api.nvim_list_bufs()) do
            if vim.api.nvim_buf_is_valid(buf) then
              local name = vim.api.nvim_buf_get_name(buf)
              local ft = vim.bo[buf].filetype
              if ft == 'snacks_explorer' or name:match('snacks_explorer') or name:match('explorer://') then
                vim.api.nvim_buf_delete(buf, { force = true })
              end
            end
          end
        end,
      },
      -- Fix layout after restore and open explorer
      post_restore_cmds = {
        function()
          vim.g.session_restored = true
          vim.defer_fn(function()
            vim.g.session_restoring = false
            for _, buf in ipairs(vim.api.nvim_list_bufs()) do
              if vim.api.nvim_buf_is_valid(buf) then
                local name = vim.api.nvim_buf_get_name(buf)
                local ft = vim.bo[buf].filetype
                -- Clean up any stray explorer or directory buffers
                if
                  ft == 'snacks_explorer'
                  or name:match('snacks_explorer')
                  or name:match('explorer://')
                  or vim.fn.isdirectory(name) == 1
                then
                  vim.api.nvim_buf_delete(buf, { force = true })
                end
              end
            end
            vim.cmd('wincmd =')
            -- Open explorer after session restore
            if package.loaded['snacks'] then
              require('snacks').explorer()
            end
          end, 50)
        end,
      },
    })
  end,
  keys = {
    { '<leader>qs', '<cmd>AutoSession save<cr>', desc = 'Save session' },
    { '<leader>qr', '<cmd>AutoSession restore<cr>', desc = 'Restore session' },
    { '<leader>qd', '<cmd>AutoSession delete<cr>', desc = 'Delete session' },
    { '<leader>qf', '<cmd>AutoSession search<cr>', desc = 'Search sessions' },
  },
}
