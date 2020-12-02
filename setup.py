import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="openbbs-middleware",
    version='0.0.1',
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["test*"]),
    install_requires=[
        "Flask-Security-Too==3.4.4",
        "flask-mongoengine==0.9.5",
        "email-validator==1.1.1",
        "Werkzeug==0.16.1",
        "gevent==20.9.0",
        "requests==2.25.0",

        "flask-swagger @ git+https://github.com/chhsiao1981/flask-swagger.git@flaskswagger-with-from-file-keyword#egg=pyutil_cfg",

        "pyutil_cfg @ git+https://github.com/chhsiao1981/pyutil_cfg.git@v0.0.3#egg=pyutil_cfg",
        "pyutil_mongo @ git+https://github.com/chhsiao1981/pyutil_mongo.git@v1.1.1#egg=pyutil_mongo",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
