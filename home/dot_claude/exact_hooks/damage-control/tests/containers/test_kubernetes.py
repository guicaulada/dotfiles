"""Tests for Kubernetes (kubectl, helm) and related orchestration security patterns."""

import json

from tests.conftest import run_hook


class TestKubernetesBlock:
    def test_block_kubectl_delete_namespace(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete namespace production"}
        )
        assert code == 2

    def test_block_kubectl_delete_ns(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete ns production"})
        assert code == 2

    def test_block_kubectl_delete_pv(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pv my-volume"})
        assert code == 2

    def test_block_kubectl_delete_persistentvolume(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete persistentvolume my-volume"}
        )
        assert code == 2

    def test_block_kubectl_delete_pvc(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pvc my-claim"})
        assert code == 2

    def test_block_kubectl_delete_persistentvolumeclaim(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete persistentvolumeclaim my-claim"}
        )
        assert code == 2

    def test_block_kubectl_delete_all(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pods --all"})
        assert code == 2

    def test_block_kubectl_delete_all_namespaces_short(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pods -A"})
        assert code == 2

    def test_block_kubectl_delete_all_namespaces_long(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete pods --all-namespaces"}
        )
        assert code == 2

    def test_block_kubectl_delete_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete pod my-pod --force --grace-period=0"}
        )
        assert code == 2

    def test_block_kubectl_config_delete_context(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl config delete-context my-context"}
        )
        assert code == 2

    def test_block_kubectl_config_delete_cluster(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl config delete-cluster my-cluster"}
        )
        assert code == 2

    def test_block_kubectl_config_delete_user(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl config delete-user my-user"})
        assert code == 2

    def test_block_kubectl_config_unset(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl config unset current-context"}
        )
        assert code == 2

    def test_block_kubectl_drain_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl drain node01 --force --ignore-daemonsets"}
        )
        assert code == 2

    def test_block_kubectl_drain_delete_emptydir(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl drain node01 --delete-emptydir-data"}
        )
        assert code == 2

    def test_block_kubectl_replace_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl replace --force -f deployment.yaml"}
        )
        assert code == 2

    def test_block_kubectl_delete_namespace_precedence(self):
        """kubectl delete namespace must hit hard block, not the ask catch-all."""
        code, _, stderr = run_hook(
            "Bash", {"command": "kubectl delete namespace production"}
        )
        assert code == 2
        assert "SECURITY" in stderr


class TestHelmBlock:
    def test_block_helm_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "helm uninstall my-release"})
        assert code == 2

    def test_block_helm_delete(self):
        code, _, _ = run_hook("Bash", {"command": "helm delete my-release"})
        assert code == 2


class TestServiceMeshBlock:
    def test_block_istioctl_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "istioctl uninstall --purge"})
        assert code == 2

    def test_block_istioctl_remove_from_cluster(self):
        code, _, _ = run_hook("Bash", {"command": "istioctl remove-from-cluster"})
        assert code == 2

    def test_block_linkerd_uninstall(self):
        code, _, _ = run_hook(
            "Bash", {"command": "linkerd uninstall | kubectl apply -f -"}
        )
        assert code == 2

    def test_block_consul_leave(self):
        code, _, _ = run_hook("Bash", {"command": "consul leave"})
        assert code == 2

    def test_block_consul_force_leave(self):
        code, _, _ = run_hook("Bash", {"command": "consul force-leave node01"})
        assert code == 2

    def test_block_consul_kv_delete(self):
        code, _, _ = run_hook("Bash", {"command": "consul kv delete my-key"})
        assert code == 2


class TestLocalKubernetes:
    def test_block_kind_delete_cluster(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kind delete cluster --name mycluster"}
        )
        assert code == 2

    def test_block_minikube_delete(self):
        code, _, _ = run_hook("Bash", {"command": "minikube delete"})
        assert code == 2

    def test_block_k3d_cluster_delete(self):
        code, _, _ = run_hook("Bash", {"command": "k3d cluster delete mycluster"})
        assert code == 2


class TestNomadBlock:
    def test_block_nomad_job_stop(self):
        code, _, _ = run_hook("Bash", {"command": "nomad job stop my-job"})
        assert code == 2

    def test_block_nomad_namespace_delete(self):
        code, _, _ = run_hook("Bash", {"command": "nomad namespace delete my-ns"})
        assert code == 2

    def test_block_nomad_volume_delete(self):
        code, _, _ = run_hook("Bash", {"command": "nomad volume delete my-vol"})
        assert code == 2


class TestKubernetesAsk:
    def test_ask_kubectl_delete_pod(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl delete pod my-pod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_apply(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl apply -f deployment.yaml"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl create namespace staging"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_patch(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": 'kubectl patch deployment my-app -p \'{"spec":{"replicas":2}}\''
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_replace(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl replace -f deployment.yaml"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_scale(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl scale deployment my-app --replicas=3"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_rollout_restart(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl rollout restart deployment/my-app"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_rollout_undo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl rollout undo deployment/my-app"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_drain(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl drain node01 --ignore-daemonsets"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_cordon(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl cordon node01"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_uncordon(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl uncordon node01"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_taint(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl taint nodes node01 key=value:NoSchedule"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_exec(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl exec -it my-pod -- bash"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_set_image(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl set image deployment/my-app my-app=myimage:v2"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_set_env(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl set env deployment/my-app MY_VAR=value"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_set_resources(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl set resources deployment/my-app --limits=cpu=200m"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl edit deployment my-app"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_run(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl run my-pod --image=nginx"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_expose(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl expose deployment my-app --port=80"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_cp(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl cp /tmp/file my-pod:/tmp/file"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_label_overwrite(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl label pod my-pod env=prod --overwrite"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_annotate_overwrite(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl annotate pod my-pod note=updated --overwrite"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_port_forward(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl port-forward pod/my-pod 8080:80"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_config_set_context(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl config set-context my-context --namespace=dev"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_config_use_context(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl config use-context my-context"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_config_set_credentials(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kubectl config set-credentials my-user --token=abc123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_debug(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl debug my-pod --image=busybox"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_kubectl_auth_reconcile(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl auth reconcile -f rbac.yaml"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_linkerd_inject(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "linkerd inject deployment.yaml"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_helm_install(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "helm install my-release my-chart"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_helm_upgrade(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "helm upgrade my-release my-chart"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_helm_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "helm rollback my-release 1"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_nomad_job_run(self):
        code, stdout, _ = run_hook("Bash", {"command": "nomad job run my-job.nomad"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
