import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt","r") as file:
    reqs = file.readlines()

setuptools.setup(
    name="phpipam",
    version="0.0.1",
    author="Philip Bove",
    author_email="pgbson@gmail.com",
    description="phpipam python api wrapper",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/bandit145/phpipam-py",
    packages=["phpipam"],
    install_requires=reqs,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ),
)