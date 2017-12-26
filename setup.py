from distutils.core import setup


setup(name='ccapi', version='0.1.0', author='Jonathan',
      author_email='imyme6yo@gmail.com',
      url="https://github.com/paragonjh/ccapi.git",
      packages=['ccapi', 'ccapi.api', 'ccapis.api.WSS', 'ccapis.api.REST',
      #packages=['ccapi', 'ccapi.api', 'ccapis.api.REST',
                'ccapi.interfaces', 'ccapi.formatters'],
      install_requires=['requests', 'grequests', 'autobahn', 'pusherclient'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers']
      )
