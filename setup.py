"""
Setup script for Reusable Coding Framework
Based on CrewAI + Qdrant Memory Integration
"""

from setuptools import setup, find_packages
import os


# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [
            line.strip() for line in fh if line.strip() and not line.startswith("#")
        ]


setup(
    name="reusable-coding-framework",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A reusable coding framework based on CrewAI with enhanced Qdrant memory management",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reusable-coding-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "dashboard": [
            "flask>=2.3.0",
            "flask-cors>=4.0.0",
            "flask-socketio>=5.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rcf=reusable_coding_framework.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
