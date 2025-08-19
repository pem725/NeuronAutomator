#!/usr/bin/env python3
"""
Setup script for Neuron Newsletter Automation
=============================================

Cross-platform automation system for opening the Neuron Daily newsletter
with all article links in separate browser tabs every weekday morning.
"""

from setuptools import setup, find_packages
from pathlib import Path
import platform

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Platform-specific dependencies
install_requires = [
    "selenium>=4.0.0",
    "webdriver-manager>=3.8.0",
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
]

# Platform-specific extras
extras_require = {
    'dev': [
        'pytest>=7.0.0',
        'pytest-cov>=4.0.0',
        'black>=22.0.0',
        'flake8>=5.0.0',
    ],
}

# Entry points for command-line interface
entry_points = {
    'console_scripts': [
        'neuron-automation=neuron_automation:main',
    ],
}

setup(
    name="neuron-automation",
    version="1.4.0",
    author="AI Assistant",
    author_email="noreply@anthropic.com",
    description="Cross-platform automation for Neuron Daily newsletter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pem725/NeuronAutomator",
    
    # Package discovery
    packages=find_packages(),
    py_modules=["neuron_automation", "config"],
    
    # Dependencies
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.6",
    
    # Entry points
    entry_points=entry_points,
    
    # Package data
    package_data={
        '': ['README.md', 'CLAUDE.md', '*.sh', '*.ps1'],
        'installers': ['*.sh', '*.ps1', '*.plist', '*.xml'],
    },
    include_package_data=True,
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Office/Business :: News/Diary",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    
    # Keywords
    keywords="automation, newsletter, browser, selenium, news, daily",
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/pem725/NeuronAutomator/issues",
        "Source": "https://github.com/pem725/NeuronAutomator",
        "Documentation": "https://github.com/pem725/NeuronAutomator/blob/main/README.md",
    },
    
    # License
    license="MIT",
    
    # Zip safety
    zip_safe=False,
)