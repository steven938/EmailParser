from distutils.core import setup
setup(
  name = 'EmailParser',         
  packages = ['EmailParser'],  
  version = '0.2',     
  license='MIT',       
  description = 'Email for parsing raw email texts',   
  author = 'Steven Chen',                   
  author_email = 's_chen@hotmail.ca',     
  url = 'https://github.com/steven938/EmailParser',
  download_url = 'https://github.com/steven938/EmailParser/archive/0.1.tar.gz',   
  keywords = ['EMAIL', 'PARSER', 'REGEX', 'OUTLOOK'],   
  install_requires=[           
          'talon',
          'python-dateutil'      
	],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
  ],
)