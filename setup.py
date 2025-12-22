"""
Setup configuration for intelligentOne
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intelligentone",
    version="0.1.0",
    author="intelligentOne Team",
    description="Transform the web into an executable operating system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/groupthinking/intelligentOne",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Operating System",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core has no external dependencies
    ],
    extras_require={
        "full": [
            "requests>=2.31.0",
            "aiohttp>=3.9.0",
            "beautifulsoup4>=4.12.0",
            "pyyaml>=6.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "intelligentone=intelligentone.cli:main",
        ],
    },
)
