import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Figure out how to test the service's state
# Docker containers don't ship with init systems
#
# def test_nginx_service(host):
#     nginx = host.service("nginx")
#
#
#     assert nginx.is_running
#     assert nginx.is_enabled


def test_packages(host):
    pkg = host.package("nginx")

    assert pkg.is_installed
    # assert pkg.version.startswith("")


def test_deployed_site(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening
