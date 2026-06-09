"""Tests for Azure CLI security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestAzureBlock:
    """Tests for Azure CLI operations that should be blocked."""

    # --- Credential exposure ---

    def test_block_az_account_get_access_token(self):
        assert_asks('Bash', {'command': 'az account get-access-token'})

    def test_block_az_account_get_access_token_with_resource(self):
        assert_asks('Bash', {'command': 'az account get-access-token --resource https://management.azure.com'})

    # --- Specific block pattern ---

    def test_block_az_backup_protection_disable(self):
        """backup protection disable is a command pattern: prompt to confirm."""
        assert_asks('Bash', {'command': 'az backup protection disable --container-name myvm --item-name myvm'})

    # --- Block catch-all: "az ... delete" or "az ... purge" ---

    def test_block_az_group_delete(self):
        assert_asks('Bash', {'command': 'az group delete --name my-rg'})

    def test_block_az_vm_delete(self):
        assert_asks('Bash', {'command': 'az vm delete --resource-group rg --name vm1'})

    def test_block_az_sql_server_delete(self):
        assert_asks('Bash', {'command': 'az sql server delete --name srv'})

    def test_block_az_sql_db_delete(self):
        assert_asks('Bash', {'command': 'az sql db delete --name mydb'})

    def test_block_az_storage_account_delete(self):
        assert_asks('Bash', {'command': 'az storage account delete --name mystorage'})

    def test_block_az_aks_delete(self):
        assert_asks('Bash', {'command': 'az aks delete --resource-group rg --name cluster'})

    def test_block_az_webapp_delete(self):
        assert_asks('Bash', {'command': 'az webapp delete --name myapp'})

    def test_block_az_functionapp_delete(self):
        assert_asks('Bash', {'command': 'az functionapp delete --name myfunc'})

    def test_block_az_keyvault_delete(self):
        assert_asks('Bash', {'command': 'az keyvault delete --name myvault'})

    def test_block_az_keyvault_purge(self):
        assert_asks('Bash', {'command': 'az keyvault purge --name myvault'})

    def test_block_az_cosmosdb_delete(self):
        assert_asks('Bash', {'command': 'az cosmosdb delete --name mydb'})

    def test_block_az_network_vnet_delete(self):
        assert_asks('Bash', {'command': 'az network vnet delete --name myvnet'})

    def test_block_az_cognitiveservices_account_delete(self):
        assert_asks('Bash', {'command': 'az cognitiveservices account delete --name myai --resource-group rg'})

    def test_block_az_container_delete(self):
        assert_asks('Bash', {'command': 'az container delete --name mycontainer --resource-group rg'})

    def test_block_az_acr_delete(self):
        assert_asks('Bash', {'command': 'az acr delete --name myregistry'})

    def test_block_az_acr_repository_delete(self):
        assert_asks('Bash', {'command': 'az acr repository delete --name myregistry --repository myimage'})

    def test_block_az_logic_workflow_delete(self):
        assert_asks('Bash', {'command': 'az logic workflow delete --name mylogicapp --resource-group rg'})

    def test_block_az_apim_delete(self):
        assert_asks('Bash', {'command': 'az apim delete --name myapim --resource-group rg'})

    def test_block_az_eventgrid_topic_delete(self):
        assert_asks('Bash', {'command': 'az eventgrid topic delete --name mytopic'})

    def test_block_az_servicebus_namespace_delete(self):
        assert_asks('Bash', {'command': 'az servicebus namespace delete --name myns --resource-group rg'})

    def test_block_az_servicebus_queue_delete(self):
        assert_asks('Bash', {'command': 'az servicebus queue delete --name myqueue --namespace-name myns'})

    def test_block_az_eventhubs_namespace_delete(self):
        assert_asks('Bash', {'command': 'az eventhubs namespace delete --name myns --resource-group rg'})

    def test_block_az_cdn_profile_delete(self):
        assert_asks('Bash', {'command': 'az cdn profile delete --name myprofile --resource-group rg'})

    def test_block_az_disk_delete(self):
        assert_asks('Bash', {'command': 'az disk delete --name mydisk --resource-group rg'})

    def test_block_az_snapshot_delete(self):
        assert_asks('Bash', {'command': 'az snapshot delete --name mysnap --resource-group rg'})

    def test_block_az_backup_delete(self):
        assert_asks('Bash', {'command': 'az backup vault delete --name myvault --resource-group rg'})

    def test_block_az_iot_hub_delete(self):
        assert_asks('Bash', {'command': 'az iot hub delete --name myhub'})

    def test_block_az_ml_workspace_delete(self):
        assert_asks('Bash', {'command': 'az ml workspace delete --name myworkspace --resource-group rg'})

    def test_block_az_network_nsg_delete(self):
        assert_asks('Bash', {'command': 'az network nsg delete --name mynsg --resource-group rg'})

    def test_block_az_keyvault_secret_delete(self):
        assert_asks('Bash', {'command': 'az keyvault secret delete --vault-name myvault --name mysecret'})

    def test_block_az_keyvault_secret_purge(self):
        assert_asks('Bash', {'command': 'az keyvault secret purge --vault-name myvault --name mysecret'})

    def test_block_az_keyvault_key_delete(self):
        assert_asks('Bash', {'command': 'az keyvault key delete --vault-name myvault --name mykey'})

    def test_block_az_monitor_action_group_delete(self):
        assert_asks('Bash', {'command': 'az monitor action-group delete --name mygroup --resource-group rg'})

    def test_block_az_monitor_alert_rule_delete(self):
        assert_asks('Bash', {'command': 'az monitor alert-rule delete --name myrule --resource-group rg'})

    def test_block_az_devops_project_delete(self):
        assert_asks('Bash', {'command': 'az devops project delete --id abc123'})

    def test_block_az_redis_delete(self):
        assert_asks('Bash', {'command': 'az redis delete --name mycache --resource-group rg'})

    def test_block_az_appservice_plan_delete(self):
        assert_asks('Bash', {'command': 'az appservice plan delete --name myplan'})


class TestAzureAsk:
    """Tests for Azure CLI operations that should prompt for confirmation."""

    # --- Specific ask patterns ---

    def test_ask_az_vm_start(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az vm start --name myvm --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_vm_stop(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az vm stop --name myvm --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_vm_restart(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az vm restart --name myvm --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_vm_deallocate(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az vm deallocate --name myvm --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_webapp_start(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az webapp start --name myapp --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_webapp_stop(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az webapp stop --name myapp --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_webapp_restart(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "az webapp restart --name myapp --resource-group rg"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_functionapp_start(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "az functionapp start --name myfunc --resource-group rg"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_aks_upgrade(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az aks upgrade --name mycluster --resource-group rg --kubernetes-version 1.28"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_keyvault_secret_set(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az keyvault secret set --vault-name myvault --name mysecret --value s3cr3t"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_deployment_group_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az deployment group create --resource-group rg --template-file template.json"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_deployment_sub_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az deployment sub create --location eastus --template-file template.json"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- Ask catch-all: create/update/set/start/stop/restart/deploy ---

    def test_ask_az_vm_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az vm create --name myvm --resource-group rg --image Ubuntu2204"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_group_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "az group create --name my-rg --location eastus"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_storage_account_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az storage account create --name mystorage --resource-group rg"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_webapp_update(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "az webapp update --name myapp --resource-group rg"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_aks_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az aks create --name mycluster --resource-group rg --node-count 3"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_webapp_deploy(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az webapp deploy --name myapp --resource-group rg --src-path app.zip"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_az_network_nsg_rule_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "az network nsg rule create --name allow-ssh --nsg-name mynsg --priority 100"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAzureAllow:
    """Tests for Azure CLI read-only operations that should be allowed."""

    def test_allow_az_vm_list(self):
        code, _, _ = run_hook("Bash", {"command": "az vm list"})
        assert code == 0

    def test_allow_az_group_list(self):
        code, _, _ = run_hook("Bash", {"command": "az group list"})
        assert code == 0

    def test_allow_az_account_show(self):
        code, _, _ = run_hook("Bash", {"command": "az account show"})
        assert code == 0

    def test_allow_az_keyvault_secret_show(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "az keyvault secret show --vault-name myvault --name mysecret"},
        )
        assert code == 0

    def test_allow_az_storage_account_list(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az storage account list --resource-group rg"}
        )
        assert code == 0

    def test_allow_az_network_vnet_list(self):
        code, _, _ = run_hook(
            "Bash", {"command": "az network vnet list --resource-group rg"}
        )
        assert code == 0


class TestAzureSessionCredentialAsk:
    def test_ask_vm_run_command(self):
        assert_asks("Bash", {"command": "az vm run-command invoke -g g -n n --command-id RunShellScript"})

    def test_ask_login(self):
        assert_asks("Bash", {"command": "az login"})
