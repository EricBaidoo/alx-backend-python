
#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient in client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import (
    TEST_PAYLOAD, org_payload, repos_payload, expected_repos, apache2_repos
)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for requests.get."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

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
        """Stop patcher after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos with given license."""
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org, mock_get_json):
        """Test org property returns correct payload."""
        mock_get_json.return_value = {"login": org}
        client = GithubOrgClient(org)
        self.assertEqual(client.org, {"login": org})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL from org payload."""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://some_url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns repo names and calls mocks once."""
        payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
        ]
        mock_get_json.return_value = payload
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient("test")
            result = client.public_repos()
            expected = [repo["name"] for repo in payload]
            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://some_url")

    @parameterized.expand([
        ( {"license": {"key": "my_license"}}, "my_license", True ),
        ( {"license": {"key": "other_license"}}, "my_license", False ),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True if repo has given license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
