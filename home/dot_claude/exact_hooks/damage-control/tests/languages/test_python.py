"""Tests for Python ecosystem security patterns."""

import json

from tests.conftest import run_hook


class TestPythonBlock:
    def test_block_python_exec(self):
        code, _, _ = run_hook(
            "Bash", {"command": 'python -c "exec(\'import os; os.system(\\"id\\")\'))"'}
        )
        assert code == 2

    def test_block_python3_eval(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": 'python3 -c "eval(\'__import__(\\"os\\").system(\\"id\\")\')"'},
        )
        assert code == 2

    def test_block_python_compile(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python -c \"compile('print(1)', '<s>', 'exec')\""}
        )
        assert code == 2

    def test_block_python_import(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python3 -c \"__import__('os').system('id')\""}
        )
        assert code == 2

    def test_block_pipx_uninstall_all(self):
        code, _, _ = run_hook("Bash", {"command": "pipx uninstall-all"})
        assert code == 2

    def test_block_conda_env_remove(self):
        code, _, _ = run_hook("Bash", {"command": "conda env remove -n myenv"})
        assert code == 2

    def test_block_mamba_env_remove(self):
        code, _, _ = run_hook("Bash", {"command": "mamba env remove -n myenv"})
        assert code == 2

    def test_block_conda_clean_all(self):
        code, _, _ = run_hook("Bash", {"command": "conda clean -a"})
        assert code == 2

    def test_block_conda_clean_all_long(self):
        code, _, _ = run_hook("Bash", {"command": "conda clean --all"})
        assert code == 2

    def test_block_poetry_env_remove(self):
        code, _, _ = run_hook("Bash", {"command": "poetry env remove python3.11"})
        assert code == 2

    def test_block_pyenv_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "pyenv uninstall 3.11.0"})
        assert code == 2

    def test_block_pyenv_virtualenv_delete(self):
        code, _, _ = run_hook("Bash", {"command": "pyenv virtualenv-delete myenv"})
        assert code == 2

    def test_block_pipenv_rm(self):
        code, _, _ = run_hook("Bash", {"command": "pipenv --rm"})
        assert code == 2

    def test_block_django_flush(self):
        code, _, _ = run_hook("Bash", {"command": "python manage.py flush"})
        assert code == 2

    def test_block_django_flush_python3(self):
        code, _, _ = run_hook("Bash", {"command": "python3 manage.py flush"})
        assert code == 2

    def test_block_django_migrate_zero(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python manage.py migrate myapp zero"}
        )
        assert code == 2

    def test_block_django_migrate_zero_python3(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python3 manage.py migrate myapp zero"}
        )
        assert code == 2


class TestPythonAsk:
    def test_ask_pipx_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "pipx install black"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pipx_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "pipx uninstall black"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_conda_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "conda remove numpy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_conda_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "conda uninstall numpy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_poetry_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "poetry remove requests"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_uv_pip_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "uv pip uninstall requests"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_uv_cache_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "uv cache clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
