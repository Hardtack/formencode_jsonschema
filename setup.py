from setuptools import setup, find_packages

setup(
    name='formencode_jsonschema',
    version='0.1.0',
    description='Dump formencode schema JSON schema using Marshmallow',
    author='Choi Geonu',
    author_email='6566gun@gmail.com',
    url='https://github.com/hardtack/formencode_jsonschema',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['marshmallow>=2.3.0', 'formencode'],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
