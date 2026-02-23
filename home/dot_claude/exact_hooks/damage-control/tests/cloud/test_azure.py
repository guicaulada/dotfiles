"""Tests for Azure CLI security patterns."""

from tests.conftest import run_hook


class TestAzureBlock:
    def test_block_az_group_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az group delete --name my-rg"})
        assert code == 2

    def test_block_az_vm_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az vm delete --resource-group rg --name vm1"}
        )
        assert code == 2

    def test_block_az_sql_server_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az sql server delete --name srv"})
        assert code == 2

    def test_block_az_sql_db_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az sql db delete --name mydb"})
        assert code == 2

    def test_block_az_storage_account_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az storage account delete --name mystorage"}
        )
        assert code == 2

    def test_block_az_aks_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az aks delete --resource-group rg --name cluster"}
        )
        assert code == 2

    def test_block_az_webapp_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az webapp delete --name myapp"})
        assert code == 2

    def test_block_az_functionapp_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az functionapp delete --name myfunc"}
        )
        assert code == 2

    def test_block_az_keyvault_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az keyvault delete --name myvault"})
        assert code == 2

    def test_block_az_keyvault_purge(self):
        code, _, _ = run_hook("Bash", {"command": "az keyvault purge --name myvault"})
        assert code == 2

    def test_block_az_cosmosdb_delete(self):
        code, _, _ = run_hook("Bash", {"command": "az cosmosdb delete --name mydb"})
        assert code == 2

    def test_block_az_network_vnet_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az network vnet delete --name myvnet"}
        )
        assert code == 2

    def test_block_az_redis_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az redis delete --name mycache --resource-group rg"}
        )
        assert code == 2

    def test_block_az_appservice_plan_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az appservice plan delete --name myplan"}
        )
        assert code == 2

    def test_block_az_monitor_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az monitor action-group delete --name mygroup"}
        )
        assert code == 2
