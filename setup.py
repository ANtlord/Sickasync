from distutils.core import setup

setup(
    name='sickasync',
    version='',
    packages=['sickasync'],
    url='',
    license='',
    author='ANtlord',
    author_email='',
    description='',
    install_requires=[
        'Cython==0.27.3',
        'aiohttp==2.3.10',
        'cchardet==2.1.1',
        'uvloop==0.9.1',
    ],
    dependency_links=[
        'git+https://github.com/MagicStack/uvloop.git@0.9.1#egg=mayo-0.9.1',
    ]
)
