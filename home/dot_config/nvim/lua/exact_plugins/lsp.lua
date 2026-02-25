return {
  {
    'neovim/nvim-lspconfig',
    dependencies = {
      { 'mason-org/mason.nvim', opts = {} },
      'WhoIsSethDaniel/mason-tool-installer.nvim',
      'saghen/blink.cmp',
    },
    config = function()
      vim.api.nvim_create_autocmd('LspAttach', {
        group = vim.api.nvim_create_augroup('lsp-attach', { clear = true }),
        callback = function(event)
          local client = vim.lsp.get_client_by_id(event.data.client_id)
          local map = function(keys, func, desc, mode)
            mode = mode or 'n'
            vim.keymap.set(mode, keys, func, { buffer = event.buf, desc = 'LSP: ' .. desc })
          end

          -- grn, gra, grD are Neovim 0.11+ built-in defaults

          -- Code group aliases
          map('<leader>ca', vim.lsp.buf.code_action, 'Code action', { 'n', 'x' })
          map('<leader>cr', vim.lsp.buf.rename, 'Code rename')
          map('<leader>cd', vim.lsp.buf.declaration, 'Code declaration')
          map('<leader>cs', vim.lsp.buf.signature_help, 'Code signature help')
          map('<leader>ch', vim.lsp.buf.hover, 'Code hover')

          -- Call hierarchy
          map('<leader>ci', vim.lsp.buf.incoming_calls, 'Code incoming calls')
          map('<leader>co', vim.lsp.buf.outgoing_calls, 'Code outgoing calls')

          if client and client:supports_method('textDocument/documentHighlight', event.buf) then
            local highlight_augroup = vim.api.nvim_create_augroup('lsp-highlight', { clear = false })
            vim.api.nvim_create_autocmd({ 'CursorHold', 'CursorHoldI' }, {
              buffer = event.buf,
              group = highlight_augroup,
              callback = vim.lsp.buf.document_highlight,
            })
            vim.api.nvim_create_autocmd({ 'CursorMoved', 'CursorMovedI' }, {
              buffer = event.buf,
              group = highlight_augroup,
              callback = vim.lsp.buf.clear_references,
            })
            vim.api.nvim_create_autocmd('LspDetach', {
              group = vim.api.nvim_create_augroup('lsp-detach', { clear = true }),
              callback = function(event2)
                vim.lsp.buf.clear_references()
                vim.api.nvim_clear_autocmds({ group = 'lsp-highlight', buffer = event2.buf })
              end,
            })
          end

          if client and client:supports_method('textDocument/inlayHint', event.buf) then
            map('<leader>uh', function()
              vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled({ bufnr = event.buf }))
            end, 'Toggle inlay hints')
          end
        end,
      })

      vim.lsp.config('*', {
        capabilities = require('blink.cmp').get_lsp_capabilities(),
      })

      local servers = {
        -- TypeScript/JavaScript
        ts_ls = {},
        biome = {},
        -- Rust: handled by rustaceanvim (rust.lua)
        -- Python
        pyright = {},
        -- Go
        gopls = {
          settings = {
            gopls = {
              gofumpt = true,
              analyses = { unusedparams = true, shadow = true },
              staticcheck = true,
            },
          },
        },
        -- Jsonnet
        jsonnet_ls = {
          cmd = { 'jsonnet-language-server', '-J', 'vendor', '-J', 'lib', '-J', 'ksonnet/lib', '-J', 'ksonnet/vendor' },
        },
        -- Terraform/HCL/Packer
        terraformls = {},
        -- Docker
        dockerls = {},
        docker_compose_language_service = {},
        -- Web (HTML/CSS)
        emmet_language_server = {},
        cssls = {},
        -- Nix
        nixd = {},
        -- Shell
        bashls = {},
      }

      local ensure_installed = {
        -- LSP servers (Mason package names)
        'lua-language-server',
        'typescript-language-server',
        'biome',
        'pyright',
        'gopls',
        'jsonnet-language-server',
        'terraform-ls',
        'dockerfile-language-server',
        'docker-compose-language-service',
        'emmet-language-server',
        'css-lsp',
        -- nixd must be installed via system package manager (not in Mason)
        -- Shell
        'bash-language-server',
        'shfmt',
        'shellcheck',
        -- Linters
        'eslint_d',
        'markdownlint-cli2',
        -- Formatters
        'stylua',
        'prettier',
        'ruff',
        'goimports',
        'gofumpt',
        'jsonnetfmt',
      }
      require('mason-tool-installer').setup({ ensure_installed = ensure_installed })

      for name, server in pairs(servers) do
        vim.lsp.config(name, server)
        vim.lsp.enable(name)
      end

      -- lua_ls: workspace config handled by lazydev.nvim
      vim.lsp.config('lua_ls', { settings = { Lua = {} } })
      vim.lsp.enable('lua_ls')
    end,
  },

  -- Neovim Lua development (replaces manual lua_ls on_init)
  {
    'folke/lazydev.nvim',
    ft = 'lua',
    opts = {
      library = {
        { path = '${3rd}/luv/library', words = { 'vim%.uv' } },
      },
    },
  },
}
