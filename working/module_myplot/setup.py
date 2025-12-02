from setuptools import setup, find_packages

setup(name='module_myplot_2025',
      description='test module for the SciComp class',
      url='https://github.com/rnovara1',
      author='Rebecca Novara',
      author_email='r.novara1@campus.unimib.it',
      license='MIT',
      version='0.0.1',
      packages=find_packages(),
      install_requires=['functools', 'os', 'matplotlib'])