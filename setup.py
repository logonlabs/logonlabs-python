import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logonlabs-python",
    version="1.5.1",
    author="Edward Guan",
    author_email="eguan@logonlabs.com",
    description="Logonlabs Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logonlabs/logonlabs-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)