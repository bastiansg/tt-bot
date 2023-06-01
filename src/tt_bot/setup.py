from setuptools import find_packages, setup

setup(
    name="tt-bot",
    packages=find_packages(),
    version="1.0.0",
    install_requires=[
        "pydantic==1.10.8",
        "more-itertools==9.1.0",
        "rich==13.4.1",
        "python-telegram-bot==20.3",
        "langchain==0.0.187",
        "unstructured==0.7.0",
        "google-api-python-client==2.88.0",
        "openai==0.27.7",
        "tiktoken==0.4.0",
        "beautifulsoup4==4.12.2",
    ],
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
