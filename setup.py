from setuptools import setup

_VERSION = '0.0.1'

def readme():
    with open('README.md') as desc:
        return desc.read()

setup(
    name='video_analyzer',
    packages=['video_analyzer'],
    version=_VERSION,
    description='Analyzes video files using Amazon Rekognition',
    long_description=readme(),
    author='Sharath Rao',
    url='https://github.com/sharathgopinath/video-analyzer',
)