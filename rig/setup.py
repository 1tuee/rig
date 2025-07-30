from setuptools import setup, find_packages

setup(
    name="rig",  # Name of your library
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,  # Include static files if specified in MANIFEST.in
    description="A lightweight and extensible Python web framework",  # Short description
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # Specify markdown format
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/yourusername/rig",  # Replace with your GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[],  # Add dependencies if needed
)