from setuptools import setup, find_packages

setup(
    name="asmsim",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.11',
        'pywinstyles',
    ],
    entry_points={
        'console_scripts': [
            'asmsim=ui.main:main',
        ],
    },
    package_data={
        'ui': ['styles.qss', 'assets/*'],
    },
)