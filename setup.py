#!/usr/bin/env python3
"""
Setup script for Notion CLI
"""

from setuptools import setup, find_packages

setup(
    name="notion-ai-cli",
    version="1.0.0", 
    description="AI development workflow CLI for uploading markdown files to Notion (Claude Code, Cursor, Windsurf)",
    author="DVPS",
    author_email="admin@dvps.engineer",
    url="https://github.com/j2d3/notion-ai-cli",
    py_modules=["notion_cli"],
    install_requires=[
        "notion-client>=2.0.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "notion-cli=notion_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)