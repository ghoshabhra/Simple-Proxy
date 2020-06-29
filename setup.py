from setuptools import setup, find_packages

setup(
    name='simple_proxy',
    version='1.0.0',
    url='',
    license='MIT',
    author='Abhra Ghosh',
    author_email='ghoshabhra1993@gmail.com',
    description='A proxy server implementation using python',
    packages=find_packages(exclude=["*.tests"]),
    install_requires = [
        "gunicorn==20.0.4",
        "django-validators",
        "flask==1.1.2",
    ],
    python_requires='>=3.6',
)
