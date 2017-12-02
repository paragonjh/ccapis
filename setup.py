from distutils.core import setup


setup(name='ccapis', version='0.2.4', author='Jonathan',
      author_email='imyme6yo@gmail.com',
      url="https://github.com/paragonjh/ccapis.git",
      packages=['ccapis', 'ccapis.apis', 'ccapis.apis.WSS', 'ccapis.apis.REST',
      #packages=['ccapis', 'ccapis.apis', 'ccapis.apis.REST',
                'ccapis.interfaces', 'ccapis.formatters'],
      install_requires=['requests', 'autobahn', 'pusherclient'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers']
      )
