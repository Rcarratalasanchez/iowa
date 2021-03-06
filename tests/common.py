import pytest


@pytest.fixture()
def Variables(SystemInfo):
    global debian_packages
    global rhel_packages
    global debian_services
    global rhel_services
    global ports
    global component
    global configuration_files

    def f(args):
        version = SystemInfo.distribution
        if args == 'packages':
            if version in ['debian', 'ubuntu']:
                return debian_packages
            else:
                return rhel_packages
        elif args == 'services':
            if version in ['debian', 'ubuntu']:
                return debian_services
            else:
                return rhel_services
        elif args == 'ports':
                return ports
        elif args == 'conf':
                conf = []
                for configuration_file in configuration_files:
                    if configuration_file.startswith('/etc'):
                        conf.append(configuration_file)
                    elif '/' in configuration_file:
                        conf.append('/etc/%s' % configuration_file)
                    else:
                        conf.append("/etc/%s/%s" % (component, configuration_file))
                return conf
    return f


def test_packages(Package, Variables):
    packages = Variables('packages')
    for package in packages:
        print package
        assert Package(package).is_installed


def test_services(Service, Variables):
    for service in Variables('services'):
        assert Service(service).is_running
        assert Service(service).is_enabled


def test_ports(Socket, Variables):
    for port in Variables('ports'):
        socket = Socket("tcp://0.0.0.0:%s" % port)
        print port
        assert socket.is_listening


def test_configuration_files(File, Variables):
    for conf in Variables('conf'):
        _file = File(conf)
        assert _file.exists
