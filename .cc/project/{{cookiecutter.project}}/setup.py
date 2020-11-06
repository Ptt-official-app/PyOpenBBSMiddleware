import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="{{cookiecutter.project_name}}",
    version="0.0.1",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["test*"]),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
