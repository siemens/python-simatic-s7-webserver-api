from setuptools import setup, find_packages

# Read the content from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-simatic-step7-webserver-api",
    version="0.1.0",
    author="Jesus Lopez Fernandez, Felix Krueger",
    author_email="jesus.lopez-fernandez@siemens.com",
    description="Python client library to interact with Simatic STEP 7 Webserver API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siemens/python-simatic-step7-webserver-api",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests"
        # all external dependencies here
    ],
    include_package_data=True,
    package_data={
        '': ['docs/*', '*.md', '*.pdf'],
    },
)
