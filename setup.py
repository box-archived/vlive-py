from setuptools import setup

setup(
    name='vlivepy',
    version='0.0.3',
    packages=['vlivepy'],
    url='https://github.com/box-archived/vlive-py',
    license='MIT License',
    author='box-archived',
    author_email='box.cassette@gmail.com',
    description='vlivepy is reverse-engineered Python-based API of VLIVE(vlive.tv)',
    install_requires=[
        'requests>=2.*',
        'reqWrapper>=0.2.*',
        'beautifulsoup4>=4.*'
    ]
)
