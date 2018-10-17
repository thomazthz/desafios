from setuptools import setup, find_packages

setup(
    name='idwall_tools',
    version='0.1',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        idwall-tools=idwall_tools.cli:cli
    ''',
)
