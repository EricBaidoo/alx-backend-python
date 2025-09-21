"""
client.py
This module contains the Client class for integration testing.
"""


# GithubOrgClient implementation for integration tests
import requests

class GithubOrgClient:
    """Client for GitHub organization data."""
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch organization data from GitHub API."""
        url = self.ORG_URL.format(self.org_name)
        return self.get_json(url)

    @staticmethod
    def get_json(url):
        """GET request to the given URL and return JSON response."""
        return requests.get(url).json()

    @property
    def _public_repos_url(self):
        """Return the repos_url from the org payload."""
        return self.org["repos_url"]

    def public_repos(self, license=None):
        """Return list of public repo names, optionally filtered by license."""
        repos = self.get_json(self._public_repos_url)
        names = [repo["name"] for repo in repos if not license or self.has_license(repo, license)]
        return names

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has the specified license key."""
        return repo.get("license", {}).get("key") == license_key
