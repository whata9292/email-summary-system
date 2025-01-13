"""Email summary system package configuration."""

from setuptools import find_packages, setup

setup(
    name="email-summary-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib",
        "google-auth",
        "google-api-python-client",
    ],
)
