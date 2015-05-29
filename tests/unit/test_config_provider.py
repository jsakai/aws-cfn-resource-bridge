import unittest2 as unittest

from aws.cfn.bridge.resources import CustomResource


class CfnBridgeConfigProvider(object):

    def get_options(self):
        return {
            'queue_url': 'https://queue.us-east-1.amazonaws.com',
            'default_action': 'action-default'
        }


class RaiseCfnBridgeConfigProvider(object):

    def get_options(self):
        raise Exception('Raise')


class NotDefiendCfnBridgeConfigProvider(object):
    pass


class TestConfigProvider(unittest.TestCase):

    def test_override_custome_resource_by_config_provider(self):
        options = {
            'config_provider': (
                'test_config_provider.CfnBridgeConfigProvider')
        }
        resource = CustomResource('name', 'file', options)
        self.assertEqual(
            resource.queue_url, 'https://queue.us-east-1.amazonaws.com')

    def test_override_custome_resource_with_incorrect_module(self):
        options = {
            'config_provider': 'XXXXXX.CfnBridgeConfigProvider.get_option',
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)

    def test_override_custome_resource_get_option_not_defiend(self):
        options = {
            'config_provider': (
                'test_config_provider.NotDefinedCfnBridgeConfigProvider')
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)

    def test_override_custome_resource_get_option_raise(self):
        options = {
            'config_provider': (
                'test_config_provider.RaiseCfnBridgeConfigProvider')
        }
        with self.assertRaises(Exception):
            CustomResource('name', 'file', options)

    def test_override_custome_resource_not_enough_params(self):
        options = {
            'config_provider': 'XXXXXX.XXXXXX',
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)


if __name__ == "__main__":
    unittest.main()
