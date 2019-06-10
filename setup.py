from setuptools import setup, find_packages

setup(
    name='pypact',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ed25519',
        'requests',
    ]
)

