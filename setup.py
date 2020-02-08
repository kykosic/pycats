import os
from setuptools import setup, find_packages


def get_requirements():
    """ Get requirements from the requirements.txt """
    dirname = os.path.dirname(os.path.realpath(__file__))
    requirements_file = os.path.join(dirname, "requirements.txt")
    with open(requirements_file, "r") as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="pycats",
    version="0.1.0",
    description="Typeclasses and categories for Python.",
    author="Kyle Kosic",
    author_email="kylekosic@gmail.com",
    url="https://github.com/kykosic/pycats",
    python_requires=">=3.6.8",
    packages=find_packages(exclude=["pycats/tests", "examples", "scripts"]),
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest",
            "flake8"
        ]
    }
)
