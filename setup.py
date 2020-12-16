from setuptools import setup
setup(
    name='penghitungkendaraan',
    version='0.1.0',
    packages=['penghitungkendaraan'],
    entry_points={
        'console_scripts': [
            'penghitungkendaraan = penghitungkendaraan.__main__:main'
        ]
    })
