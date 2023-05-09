from setuptools import find_packages, setup

setup(
    name="tt-bot",
    packages=find_packages(),
    version="1.0.0",
    install_requires=[
        "pydantic==1.10.7",
        "more-itertools==9.1.0",
        "rich==13.3.5",
        "python-telegram-bot==20.3",
        "langchain==0.0.161",
        "unstructured==0.6.4",
        "google-api-python-client==2.86.0",
        "openai==0.27.6",
        "tiktoken==0.4.0",
    ],
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
