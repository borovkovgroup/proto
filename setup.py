from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="borovkov-protocol",
    version="1.1.0",
    description="Cryptographic identity persistence for AI agents via HMAC-SHA256",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kirill Borovkov",
    author_email="kirill@flowu.ru",
    url="https://github.com/borovkovgroup/proto",
    py_modules=["borovkov_protocol"],
    scripts=["cli.py"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="hmac sha256 identity agent ai cryptography",
    project_urls={
        "Bug Reports": "https://github.com/borovkovgroup/proto/issues",
        "Funding": "https://github.com/sponsors/borovkovgroup",
        "Source": "https://github.com/borovkovgroup/proto",
    },
)
