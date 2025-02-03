from setuptools import setup, find_packages

setup(
    name="py-fast-api",  
    version="0.1.0",  
    packages=find_packages(),  
    install_requires=[  
        "fastapi",  
        "uvicorn",
        "psycopg2",
        "python-dotenv",
        "redis",
        "google-generativeai",
        "langchain-google-genai",
        "PyPDF2",
        "streamlit",
    ],
    author="İdris Aladağ",  
    author_email="aladag2345@gmail.com",  
    description="-",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/nosohuh/async-task-pro",  
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
