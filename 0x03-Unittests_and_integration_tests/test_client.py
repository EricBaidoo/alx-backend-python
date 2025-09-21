#!/usr/bin/env python3
"""Unit tests for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD, org_payload, repos_payload, expected_repos, apache2_repos
from parameterized import parameterized_class

# Integration test for GithubOrgClient
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect for requests.get().json()
        def side_effect(url):
            class MockResponse:
                def json(self_inner):
                    if url.endswith("/orgs/test_org"):
                        return cls.org_payload
                    elif url.endswith("/orgs/test_org/repos"):
                        return cls.repos_payload
            return MockResponse()
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org, mock_get_json):
        mock_get_json.return_value = {"login": org}
        client = GithubOrgClient(org)
        self.assertEqual(client.org, {"login": org})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://some_url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
        ]
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://some_url")

    @parameterized.expand([
        ( {"license": {"key": "my_license"}}, "my_license", True ),
        ( {"license": {"key": "other_license"}}, "my_license", False ),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
