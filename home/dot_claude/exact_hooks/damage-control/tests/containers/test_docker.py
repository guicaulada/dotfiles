"""Tests for Docker, Podman, and docker-compose security patterns."""

import json

from tests.conftest import run_hook


class TestDockerBlock:
    def test_block_docker_system_prune(self):
        code, _, _ = run_hook("Bash", {"command": "docker system prune -a"})
        assert code == 2

    def test_block_docker_rm_force_subshell(self):
        code, _, _ = run_hook("Bash", {"command": "docker rm -f $(docker ps -aq)"})
        assert code == 2

    def test_block_docker_rmi_force(self):
        code, _, _ = run_hook("Bash", {"command": "docker rmi -f myimage:latest"})
        assert code == 2

    def test_block_docker_volume_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker volume rm myvol"})
        assert code == 2

    def test_block_docker_volume_prune(self):
        code, _, _ = run_hook("Bash", {"command": "docker volume prune"})
        assert code == 2

    def test_block_docker_network_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker network rm my-network"})
        assert code == 2

    def test_block_docker_container_prune(self):
        code, _, _ = run_hook("Bash", {"command": "docker container prune"})
        assert code == 2

    def test_block_docker_image_prune_all(self):
        code, _, _ = run_hook("Bash", {"command": "docker image prune -a"})
        assert code == 2

    def test_block_docker_builder_prune(self):
        code, _, _ = run_hook("Bash", {"command": "docker builder prune"})
        assert code == 2

    def test_block_docker_builder_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker builder rm my-builder"})
        assert code == 2

    def test_block_docker_stack_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker stack rm my-stack"})
        assert code == 2

    def test_block_docker_swarm_leave_force(self):
        code, _, _ = run_hook("Bash", {"command": "docker swarm leave --force"})
        assert code == 2

    def test_block_docker_service_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker service rm my-service"})
        assert code == 2

    def test_block_docker_secret_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker secret rm my-secret"})
        assert code == 2

    def test_block_docker_buildx_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker buildx rm my-builder"})
        assert code == 2

    def test_block_docker_buildx_prune(self):
        code, _, _ = run_hook("Bash", {"command": "docker buildx prune"})
        assert code == 2

    def test_block_docker_context_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker context rm my-context"})
        assert code == 2

    def test_block_docker_trust_revoke(self):
        code, _, _ = run_hook("Bash", {"command": "docker trust revoke myrepo/myimage"})
        assert code == 2

    def test_block_docker_plugin_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker plugin rm my-plugin"})
        assert code == 2

    def test_block_docker_config_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker config rm my-config"})
        assert code == 2

    def test_block_docker_image_rm(self):
        code, _, _ = run_hook("Bash", {"command": "docker image rm myimage:latest"})
        assert code == 2

    def test_block_docker_compose_down_volumes(self):
        code, _, _ = run_hook("Bash", {"command": "docker compose down -v"})
        assert code == 2

    def test_block_docker_compose_down_volumes_long(self):
        code, _, _ = run_hook("Bash", {"command": "docker compose down --volumes"})
        assert code == 2


class TestDockerAsk:
    def test_ask_docker_compose_down(self):
        code, stdout, _ = run_hook("Bash", {"command": "docker compose down"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_docker_push(self):
        code, stdout, _ = run_hook("Bash", {"command": "docker push myimage:latest"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_docker_manifest_push(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "docker manifest push myimage:latest"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_docker_run_privileged(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "docker run --privileged ubuntu bash"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_docker_run_root_volume_mount(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "docker run -v /:/host ubuntu bash"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_docker_run_root_mount_syntax(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "docker run --mount type=bind,src=/,dst=/host ubuntu bash"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestPodmanBlock:
    def test_block_podman_system_prune(self):
        code, _, _ = run_hook("Bash", {"command": "podman system prune -a"})
        assert code == 2

    def test_block_podman_rm_force(self):
        code, _, _ = run_hook("Bash", {"command": "podman rm -f container1"})
        assert code == 2

    def test_block_podman_rmi_force(self):
        code, _, _ = run_hook("Bash", {"command": "podman rmi -f image1"})
        assert code == 2

    def test_block_podman_volume_rm(self):
        code, _, _ = run_hook("Bash", {"command": "podman volume rm myvol"})
        assert code == 2

    def test_block_podman_volume_prune(self):
        code, _, _ = run_hook("Bash", {"command": "podman volume prune"})
        assert code == 2

    def test_block_podman_network_rm(self):
        code, _, _ = run_hook("Bash", {"command": "podman network rm mynet"})
        assert code == 2

    def test_block_podman_container_prune(self):
        code, _, _ = run_hook("Bash", {"command": "podman container prune"})
        assert code == 2

    def test_block_podman_image_prune_all(self):
        code, _, _ = run_hook("Bash", {"command": "podman image prune -a"})
        assert code == 2

    def test_block_podman_secret_rm(self):
        code, _, _ = run_hook("Bash", {"command": "podman secret rm mysecret"})
        assert code == 2


class TestPodmanAsk:
    def test_ask_podman_push(self):
        code, stdout, _ = run_hook("Bash", {"command": "podman push myimage:latest"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_podman_run_privileged(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "podman run --privileged ubuntu bash"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestDockerComposeHyphen:
    def test_block_docker_compose_hyphen_down_volumes(self):
        code, _, _ = run_hook("Bash", {"command": "docker-compose down -v"})
        assert code == 2

    def test_ask_docker_compose_hyphen_down(self):
        code, stdout, _ = run_hook("Bash", {"command": "docker-compose down"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestRegistryTools:
    def test_block_skopeo_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "skopeo delete docker://registry.example.com/myimage:latest"},
        )
        assert code == 2

    def test_block_crane_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "crane delete registry.example.com/myimage:latest"},
        )
        assert code == 2
