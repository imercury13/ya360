from setuptools import setup, find_packages
from os.path import join, dirname
import ya360

setup(
    name='ya360',
    version=ya360.__version__,
    packages=find_packages(),
    description='ya360 - Yandex 360 admin cli tool',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author=ya360.__author__,
    author_email='ya360@uh.net.ru',
    maintainer=ya360.__author__,
    maintainer_email='ya360@uh.net.ru',
    download_url='https://github.com/imercury13/ya360',
    url='https://ya360.uh.net.ru',
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
