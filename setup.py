from setuptools import setup, find_packages
from os.path import join, dirname
import ya360

setup(
    name='ya360',
    version=ya360.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Igor Kuptsov',
    author_email='i.kuptsov@uh.net.ru',
    entry_points={
        'console_scripts':
            ['ya360 = ya360.__main__:start'],
    },
    install_requires=[
		'requests',
    ],
    include_package_data=True,
)
