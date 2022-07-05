from setuptools import setup, find_packages
from os.path import join, dirname
import ya360

setup(
    name='ya360',
    version=ya360.__version__,
    packages=find_packages(),
    description='ya360 - Yandex 360 admin cli tool',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Igor Kuptsov',
    author_email='i.kuptsov@uh.net.ru',
    maintainer='Igor Kuptsov',
    maintainer_email='i.kuptsov@uh.net.ru',
    download_url='https://github.com/imercury13/ya360',
    url='https://imercury13.github.io/ya360',
    license='GPL-3.0',
    entry_points={
        'console_scripts':
            ['ya360 = ya360.__main__:start'],
    },
    install_requires=[
		'requests',
    ],
    include_package_data=True,
)
