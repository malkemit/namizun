from setuptools import setup

setup(name='namizun_core',
      version='1.3.3',
      description='Asymmetric upload and download',
      author='MalKeMit',
      author_email='khodemalkemit@gmail.com',
      url='https://github.com/malkemit/namizun',
      setup_requires=['wheel'],
      install_requires=['psutil==5.9.4',
                        'colored~=1.4.4',
                        'pyfiglet~=0.8.post1',
                        'prettytable~=3.5.0',
                        'redis==4.3.5',
                        'pytz==2022.6']
      )
