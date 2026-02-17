return {
  {
    'stevearc/conform.nvim',
    event = { 'BufWritePre' },
    cmd = { 'ConformInfo' },
    keys = {
      {
        '<leader>cf',
        function()
          require('conform').format({ async = true, lsp_format = 'fallback' })
        end,
        mode = '',
        desc = 'Code format',
      },
    },
    opts = {
      notify_on_error = false,
      format_on_save = function(bufnr)
        local disable_filetypes = { c = true, cpp = true }
        if disable_filetypes[vim.bo[bufnr].filetype] then
          return nil
        end
        return { timeout_ms = 500, lsp_format = 'fallback' }
      end,
      formatters_by_ft = {
        lua = { 'stylua' },
        -- TypeScript/JavaScript (prefer biome if available)
        typescript = { 'biome', 'prettier', stop_after_first = true },
        typescriptreact = { 'biome', 'prettier', stop_after_first = true },
        javascript = { 'biome', 'prettier', stop_after_first = true },
        javascriptreact = { 'biome', 'prettier', stop_after_first = true },
        -- Rust (uses rust_analyzer)
        rust = { lsp_format = 'prefer' },
        -- Python
        python = { 'ruff_format', 'ruff_organize_imports' },
        -- Go
        go = { 'goimports', 'gofumpt' },
        -- Jsonnet
        jsonnet = { 'jsonnetfmt' },
        -- Terraform/HCL
        terraform = { 'terraform_fmt' },
        ['terraform-vars'] = { 'terraform_fmt' },
        hcl = { 'terraform_fmt' },
        packer = { 'packer_fmt' },
        -- Common formats (prefer biome for json)
        json = { 'biome', 'prettier', stop_after_first = true },
        yaml = { 'prettier' },
        markdown = { 'prettier' },
        -- Just (justfile)
        just = { 'just' },
        -- Shell
        sh = { 'shfmt' },
        bash = { 'shfmt' },
      },
    },
  },
}
