from setuptools import setup, find_packages

setup(
    name="rig",  
    version="0.1.0",  
    packages=find_packages(),  
    include_package_data=True,  
    description="A lightweight and extensible Python web framework",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Your Name",  # Replace with your name
    author_email="cxsperb@gmail.com",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: none",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[],  # Add dependencies if needed
)
