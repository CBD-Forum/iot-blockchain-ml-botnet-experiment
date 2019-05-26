class Container(object):
    """Imitates container objects"""

    def __init__(self, id, name, attrs):
        self.id = id
        self.name = name
        self.attrs = attrs


container_1 = Container(
    id='1',
    name='remote-thermometer-1',
    attrs={
        'NetworkSettings': {
            'Bridge': '',
            'SandboxID': '0fa959d967cb608b441a3',
            'HairpinMode': False,
            'LinkLocalIPv6Address': '',
            'LinkLocalIPv6PrefixLen': 0,
            'Ports': {
                '22/tcp': None,
                '23/tcp': None,
                '80/tcp': None
            },
            'Networks': {
                'experiment_net': {
                    'IPAMConfig': {
                        'IPv4Address': '192.168.0.2'
                    },
                    'Links': None,
                    'Aliases': [
                        'remote-thermometer-1',
                        'f1eb32b177e2'
                    ],
                    'NetworkID': '259be3fa2711542cfacd96a92a9784',
                    'EndpointID': '27623ac1206f3bbeb4549585632cb',
                    'Gateway': '192.168.0.1',
                    'IPAddress': '192.168.0.2',
                    'IPPrefixLen': 16,
                    'IPv6Gateway': '',
                    'GlobalIPv6Address': '',
                    'GlobalIPv6PrefixLen': 0,
                    'MacAddress': '02:42:c0:a8:00:1a',
                    'DriverOpts': None
                }
            }
        }
    }
)

container_2 = Container(
    id='2',
    name='remote-thermometer-2',
    attrs={
        'NetworkSettings': {
            'Bridge': '',
            'SandboxID': '0fa9d967cb608b1a09441a3',
            'HairpinMode': False,
            'LinkLocalIPv6Address': '',
            'LinkLocalIPv6PrefixLen': 0,
            'Ports': {
                '22/tcp': None,
                '23/tcp': None,
                '80/tcp': None
            },
            'Networks': {
                'experiment_net': {
                    'IPAMConfig': {
                        'IPv4Address': '192.168.0.3'
                    },
                    'Links': None,
                    'Aliases': [
                        'remote-thermometer-2',
                        'f1eb32b177e2'
                    ],
                    'NetworkID': '259be3fa2711542cfacd96a92a9784',
                    'EndpointID': '27623ac1206f3bbeb4549585632cb',
                    'Gateway': '192.168.0.1',
                    'IPAddress': '192.168.0.3',
                    'IPPrefixLen': 16,
                    'IPv6Gateway': '',
                    'GlobalIPv6Address': '',
                    'GlobalIPv6PrefixLen': 0,
                    'MacAddress': '02:42:c0:8a:00:1a',
                    'DriverOpts': None
                }
            }
        }
    }
)

container_3 = Container(
    id='3',
    name='remote-thermometer-3',
    attrs={
        'NetworkSettings': {
            'Bridge': '',
            'SandboxID': '0fa959d967c08b1a09441a3',
            'HairpinMode': False,
            'LinkLocalIPv6Address': '',
            'LinkLocalIPv6PrefixLen': 0,
            'Ports': {
                '22/tcp': None,
                '23/tcp': None,
                '80/tcp': None
            },
            'Networks': {
                'experiment_net': {
                    'IPAMConfig': {
                        'IPv4Address': '192.168.0.4'
                    },
                    'Links': None,
                    'Aliases': [
                        'remote-thermometer-3',
                        'f1eb32b177e2'
                    ],
                    'NetworkID': '259be3fa2711542cfacd96a92a9784',
                    'EndpointID': '27623ac1206f3bbeb4549585632cb',
                    'Gateway': '192.168.0.1',
                    'IPAddress': '192.168.0.4',
                    'IPPrefixLen': 16,
                    'IPv6Gateway': '',
                    'GlobalIPv6Address': '',
                    'GlobalIPv6PrefixLen': 0,
                    'MacAddress': '02:24:c0:a8:00:1a',
                    'DriverOpts': None
                }
            }
        }
    }
)

containers = [container_1, container_2, container_3]
