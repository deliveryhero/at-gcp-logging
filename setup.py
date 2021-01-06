from setuptools import setup

setup(name='at_gcp_logging',
      version='0.1',
      description='Format logs to appropriate format for GCP',
      url='https://github.com/deliveryhero/at-gcp-logging',
      author='Delivery Hero',
      packages=['at_gcp_logging'],
      install_requires=[
            'django>=3.0.0'
      ])
