from distutils.core import setup
setup(
  name = 'EmailParser',         # How you named your package folder (MyLib)
  packages = ['EmailParser'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Email for parsing raw email texts',   # Give a short description about your library
  author = 'Steven Chen',                   # Type in your name
  author_email = 's_chen@hotmail.ca',      # Type in your E-Mail
  url = 'https://github.com/steven938/EmailParser',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/steven938/EmailParser/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['EMAIL', 'PARSER', 'REGEX', 'OUTLOOK'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'talon',
          'dateutil'      
	],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
  ],
)