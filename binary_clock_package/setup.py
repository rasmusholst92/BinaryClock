from setuptools import setup, find_packages

setup(
    name='bin_clock',
    version='1.0',
    author='Rasmus, Martin, Oskar',
    description='Et binært ur',
    packages=find_packages(),
    install_requires=['sense_hat'],
    entry_points={
        'console_scripts': [
            'bin_clock = bin_clock:main'
        ]
    }
)