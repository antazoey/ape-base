from ape import plugins
from ape.api.networks import LOCAL_NETWORK_NAME, ForkedNetworkAPI, NetworkAPI, create_network_type
from ape_node import Node
from ape_test import LocalProvider

from .ecosystem import NETWORKS, Base, BaseConfig


@plugins.register(plugins.Config)
def config_class():
    return BaseConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield Base


@plugins.register(plugins.NetworkPlugin)
def networks():
    for network_name, network_params in NETWORKS.items():
        yield "base", network_name, create_network_type(*network_params)
        yield "base", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for local providers, as they get chain_id from themselves
    yield "base", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "base", network_name, Node

    yield "base", LOCAL_NETWORK_NAME, LocalProvider
