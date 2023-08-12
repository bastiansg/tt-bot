from setuptools import find_packages, setup


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="tt-bot",
    packages=find_packages(),
    version="1.0.0",
    install_requires=required,
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
