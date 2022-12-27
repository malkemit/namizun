from setuptools import setup

setup(name='namizun_menu',
      version='1.0.0',
      description='namizun menu',
      author='MalKeMit',
      author_email='khodemalkemit@gmail.com',
      url='https://github.com/malkemit/namizun',
      setup_requires=['wheel'],
      install_requires=['colored~=1.4.4',
                        'pyfiglet~=0.8.post1',
                        'prettytable~=3.5.0']
      )
