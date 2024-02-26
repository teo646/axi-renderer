from setuptools import setup

setup(
    name='axi-renderer',
    version='0.1',
    description='module for converting 3d object to 2d lines',
    author='Tae Young Choi',
    author_email='tyul0529@naver.com',
    packages=['axiRenderer', 'objects'],
    install_requires=['numpy', 'opencv-python'],
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
