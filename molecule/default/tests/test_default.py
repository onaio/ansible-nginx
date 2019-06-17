import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nginx_service(host):
    nginx = host.service("nginx")

    assert nginx.is_running
    assert nginx.is_enabled


def test_packages(host):
    pkg = host.package("nginx")

    assert pkg.is_installed
    # assert pkg.version.startswith("")


def test_deployed_site(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_copied_files(host):
    dhFile = host.file("/etc/ssl/certs/dhparam.pem")
    assert dhFile.exists

    # first ssl site
    certDir = host.file("/etc/nginx/ssl/tests/example.org")
    assert certDir.exists
    assert certDir.user == "root"
    assert certDir.group == "root"
    assert certDir.is_directory
    assert oct(certDir.mode) == "0o700"

    certFile = host.file("/etc/nginx/ssl/tests/example.org/certificate.pem")
    crtHsh = "46723fb5c01c28680e9a4cb255e7e935c8dfaa918ece61f589902e59d9048892"
    assert certFile.exists
    assert certFile.user == "root"
    assert certFile.group == "root"
    assert certFile.is_file
    assert certFile.sha256sum == crtHsh
    assert oct(certFile.mode) == "0o600"

    keyFile = host.file("/etc/nginx/ssl/tests/example.org/key.pem")
    keyHsh = "e696471a11dc497c458d6d1b42d82a514901d854bbd94a7f7ef4ac06be8d4c3c"
    assert keyFile.exists
    assert keyFile.user == "root"
    assert keyFile.group == "root"
    assert keyFile.is_file
    assert keyFile.sha256sum == keyHsh
    assert oct(keyFile.mode) == "0o600"

    sslCnf = host.file("/etc/nginx/example.org.conf")
    sslALog = "/var/log/nginx/foo-ssl-access.log example_com_access_format;"
    assert sslALog in sslCnf.content_string

    ngxCnf = host.file("/etc/nginx/nginx.conf")
    aLogLn = str("log_format  example_com_access_format  $http_x_forwarded_for"
                 " - $remote_user [$time_local] $status $body_bytes_sent"
                 " $request_length;")
    assert aLogLn in ngxCnf.content_string

    # second ssl site
    certDir = host.file("/etc/nginx/ssl/tests/example2.org")
    assert certDir.exists
    assert certDir.user == "root"
    assert certDir.group == "root"
    assert certDir.is_directory
    assert oct(certDir.mode) == "0o700"

    certFile = host.file("/etc/nginx/ssl/tests/example2.org/certificate.pem")
    assert certFile.exists
    assert certFile.user == "root"
    assert certFile.group == "root"
    assert certFile.is_symlink

    keyFile = host.file("/etc/nginx/ssl/tests/example2.org/key.pem")
    assert keyFile.exists
    assert keyFile.user == "root"
    assert keyFile.group == "root"
    assert keyFile.is_symlink


def test_basic_auth_files(host):
    pwFile = host.file("/tmp/etc/nginx/.htpasswd")
    assert pwFile.exists
    assert pwFile.user == "www-data"
    assert pwFile.group == "www-data"
