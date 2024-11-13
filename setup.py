from setuptools import find_packages,setup


setup(
    name='mcqgenerator',
    version='0.0.1',
    author='praneeth reddy',
    author_email='praneethreddy954@gmail.com',
    install_requires=['huggingface_hub','transformers','langchain','streamlit','torch','python-dotenv','PyPDF2'],
    packages=find_packages()
)