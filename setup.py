from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='inmetpy',
      version="0.1.1",
      description="An unofficial package to consume the API of the Brazilian National Institute of Meteorology",
      packages=find_packages(),
      author="Felippe Galdino, Tobias Ferreira",
      author_email="ocfgaldino@gmail.com",
      license="GPLv3+",
      url="https://github.com/ocfgaldino/inmetpy",
      install_requires=requirements,
      test_suite='tests',
      include_package_data=True,
      scripts=['scripts/inmetpy'],
      zip_safe=False)
