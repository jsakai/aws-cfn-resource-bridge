import unittest2 as unittest

from aws.cfn.bridge.resources import CustomResource


class CfnBridgeConfigProvider(object):

    def get_option(self):
        return {
            'queue_url': 'https://queue.us-east-1.amazonaws.com',
            'default_action': 'action-default'
        }


class TestConfigProvider(unittest.TestCase):

    def test_override_custome_resource_by_config_provider(self):
        options = {
            'config_provider': (
                'test_config_provider.CfnBridgeConfigProvider.get_option')
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

    def test_override_custome_resource_with_incorrect_class(self):
        options = {
            'config_provider': 'test_config_provider.XXXXXX.get_option',
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)

    def test_override_custome_resource_with_incorrect_fnunc(self):
        options = {
            'config_provider': (
                'test_config_provider.CfnBridgeConfigProvider.XXXXXX')
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)

    def test_override_custome_resource_not_enough_params(self):
        options = {
            'config_provider': 'XXXXXX.XXXXXX',
        }
        with self.assertRaises(ValueError):
            CustomResource('name', 'file', options)


if __name__ == "__main__":
    unittest.main()
