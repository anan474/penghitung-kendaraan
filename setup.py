from setuptools import setup
setup(
    name='sistempenghitungkendaraan',
    version='0.1.1',
    packages=['sistempenghitungkendaraan'],
    entry_points={
        'console_scripts': [
            'sistempenghitungkendaraan = sistempenghitungkendaraan.__main__:main'
        ]
    })
