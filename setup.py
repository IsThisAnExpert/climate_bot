from setuptools import setup

setup(name='climabot',
      version='0.1',
      description='bot for credibility score',
      url='https://github.com/IsThisAnExpert/climate_bot',
      author='Francisco Arcila',
      author_email='farcilas@gmail.com',
      license='GNU Affero General Public License v3.0',
      packages =  ['climabot'],
      # package_data={'climabot': ['src/*']},
      keywords=['Climate Change', 'fact-checking', 'FFF', 'scientist for future', 'S4FHD'],
      scripts=[''],
      install_requires=[
          'pandas',
            'pymysql',
            'mysqlclient',
            'configobj',
      ],

      zip_safe=False)
