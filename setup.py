from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='vlivepy',
    version='0.3.2',
    packages=['vlivepy'],
    url='https://github.com/box-archived/vlive-py',
    license='MIT License',
    author='box-archived',
    author_email='box.cassette@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='vlivepy is unofficial, Python-based, API of VLIVE(vlive.tv)',
    install_requires=[
        'requests>=2.*',
        'reqWrapper>=0.2.*',
        'beautifulsoup4>=4.*'
    ]
)
