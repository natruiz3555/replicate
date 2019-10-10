from setuptools import setup

setup(
    name="replicate",
    version="1.0",
    packages=["replicate"],
    install_requires=["requests", "flask", "furl", "aws-wsgi"],
    package_data={
        "replicate": ["templates/*"]
    }
)
