from setuptools import find_packages, setup

install_reqs = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name="nomark",
    version="0.1-beta",
    license="MIT",
    author="jen6",
    author_email="work.jen6@gmail.com",
    description="notion to markdown with image uploader using google drive",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jen6/nomark",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    scripts=["nomark"],
    setup_requires=install_reqs,
)
