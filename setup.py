from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pryme',
    version='0.2',
    description='A number theory package',
    url='http://github.com/calamitizer/pryme',
    author='J. Alex Ruble',
    author_email='jaruble@ncsu.edu',
    license='Unlicense',
    packages=['pryme'],
    zip_safe=False
)
