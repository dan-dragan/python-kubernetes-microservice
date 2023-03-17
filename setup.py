from setuptools import find_packages, setup

setup(name="Cinema",
      version = "0.1",
      description = "Example of Microservices using Flask",
      author = "Dan Dragan",
      platforms = ["any"],
      license = "BSD",
      packages = find_packages(),
      install_requires = ["Flask==2.0.3", "requests==2.20.0" ],
      )
