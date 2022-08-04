from setuptools import setup, find_packages
from os.path import join, dirname
import ya360

setup(
    name='ya360',
    version=ya360.__version__,
    python_requires='>=3.6.9',
    packages=find_packages(),
    description='ya360 - Yandex 360 admin cli tool',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author=ya360.__author__,
    author_email='ya360@uh.net.ru',
    maintainer=ya360.__author__,
    maintainer_email='ya360@uh.net.ru',
    download_url='https://github.com/imercury13/ya360',
    url='https://ya360.uh.net.ru',
    license='MIT',
    project_urls={
        "Documentation": "https://ya360.readthedocs.io/",
        "Bug Tracker": "https://github.com/imercury13/ya360/issues"
    },
    entry_points={
        'console_scripts':
            ['ya360 = ya360.cmd:start'],
    },
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: System Administrators'

    ],
    install_requires=[
        'yandex-oauth>=1.1.1',
        'yandex-360>=1.1.3'
    ],
    include_package_data=True,
)
