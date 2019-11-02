from distutils.core import setup

setup(
    name='RankBasedMonteCarlo',
    version='0.1dev',
    packages=['RankBasedMonteCarlo',],
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'scipy'
    ],
    author='Ben Smith',
    author_email='bosmith@unomaha.edu'
)
