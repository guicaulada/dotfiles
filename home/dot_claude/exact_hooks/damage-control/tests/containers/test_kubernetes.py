"""Tests for Kubernetes (kubectl, helm) and local k8s security patterns."""

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

    def test_block_kubectl_delete_all(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pods --all"})
        assert code == 2

    def test_block_kubectl_delete_all_namespaces(self):
        code, _, _ = run_hook("Bash", {"command": "kubectl delete pods -A"})
        assert code == 2

    def test_block_kubectl_delete_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "kubectl delete pod my-pod --force --grace-period=0"}
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

    def test_block_helm_delete(self):
        code, _, _ = run_hook("Bash", {"command": "helm delete my-release"})
        assert code == 2

    def test_block_kubectl_delete_namespace_precedence(self):
        """kubectl delete namespace must hit hard block, not the ask catch-all."""
        code, _, stderr = run_hook(
            "Bash", {"command": "kubectl delete namespace production"}
        )
        assert code == 2
        assert "SECURITY" in stderr


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

    def test_ask_kubectl_scale(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl scale deployment my-app --replicas=3"}
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

    def test_ask_kubectl_drain(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl drain node01 --ignore-daemonsets"}
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
