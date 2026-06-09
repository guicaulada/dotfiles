"""Tests for Docker, Podman, and docker-compose security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestDockerBlock:
    def test_block_docker_system_prune(self):
        assert_asks('Bash', {'command': 'docker system prune -a'})

    def test_block_docker_rm_force_subshell(self):
        assert_asks('Bash', {'command': 'docker rm -f $(docker ps -aq)'})

    def test_block_docker_rmi_force(self):
        assert_asks('Bash', {'command': 'docker rmi -f myimage:latest'})

    def test_block_docker_volume_rm(self):
        assert_asks('Bash', {'command': 'docker volume rm myvol'})

    def test_block_docker_volume_prune(self):
        assert_asks('Bash', {'command': 'docker volume prune'})

    def test_block_docker_network_rm(self):
        assert_asks('Bash', {'command': 'docker network rm my-network'})

    def test_block_docker_container_prune(self):
        assert_asks('Bash', {'command': 'docker container prune'})

    def test_block_docker_image_prune_all(self):
        assert_asks('Bash', {'command': 'docker image prune -a'})

    def test_block_docker_builder_prune(self):
        assert_asks('Bash', {'command': 'docker builder prune'})

    def test_block_docker_builder_rm(self):
        assert_asks('Bash', {'command': 'docker builder rm my-builder'})

    def test_block_docker_stack_rm(self):
        assert_asks('Bash', {'command': 'docker stack rm my-stack'})

    def test_block_docker_swarm_leave_force(self):
        assert_asks('Bash', {'command': 'docker swarm leave --force'})

    def test_block_docker_service_rm(self):
        assert_asks('Bash', {'command': 'docker service rm my-service'})

    def test_block_docker_secret_rm(self):
        assert_asks('Bash', {'command': 'docker secret rm my-secret'})

    def test_block_docker_buildx_rm(self):
        assert_asks('Bash', {'command': 'docker buildx rm my-builder'})

    def test_block_docker_buildx_prune(self):
        assert_asks('Bash', {'command': 'docker buildx prune'})

    def test_block_docker_context_rm(self):
        assert_asks('Bash', {'command': 'docker context rm my-context'})

    def test_block_docker_trust_revoke(self):
        assert_asks('Bash', {'command': 'docker trust revoke myrepo/myimage'})

    def test_block_docker_plugin_rm(self):
        assert_asks('Bash', {'command': 'docker plugin rm my-plugin'})

    def test_block_docker_config_rm(self):
        assert_asks('Bash', {'command': 'docker config rm my-config'})

    def test_block_docker_image_rm(self):
        assert_asks('Bash', {'command': 'docker image rm myimage:latest'})

    def test_block_docker_compose_down_volumes(self):
        assert_asks('Bash', {'command': 'docker compose down -v'})

    def test_block_docker_compose_down_volumes_long(self):
        assert_asks('Bash', {'command': 'docker compose down --volumes'})


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
        assert_asks('Bash', {'command': 'podman system prune -a'})

    def test_block_podman_rm_force(self):
        assert_asks('Bash', {'command': 'podman rm -f container1'})

    def test_block_podman_rmi_force(self):
        assert_asks('Bash', {'command': 'podman rmi -f image1'})

    def test_block_podman_volume_rm(self):
        assert_asks('Bash', {'command': 'podman volume rm myvol'})

    def test_block_podman_volume_prune(self):
        assert_asks('Bash', {'command': 'podman volume prune'})

    def test_block_podman_network_rm(self):
        assert_asks('Bash', {'command': 'podman network rm mynet'})

    def test_block_podman_container_prune(self):
        assert_asks('Bash', {'command': 'podman container prune'})

    def test_block_podman_image_prune_all(self):
        assert_asks('Bash', {'command': 'podman image prune -a'})

    def test_block_podman_secret_rm(self):
        assert_asks('Bash', {'command': 'podman secret rm mysecret'})


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
        assert_asks('Bash', {'command': 'docker-compose down -v'})

    def test_ask_docker_compose_hyphen_down(self):
        code, stdout, _ = run_hook("Bash", {"command": "docker-compose down"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestRegistryTools:
    def test_block_skopeo_delete(self):
        assert_asks('Bash', {'command': 'skopeo delete docker://registry.example.com/myimage:latest'})

    def test_block_crane_delete(self):
        assert_asks('Bash', {'command': 'crane delete registry.example.com/myimage:latest'})
