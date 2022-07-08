import setuptools

REQUIRED_PACKAGES = [
    "PyHamcrest"

]

setuptools.setup(
    name='apache-beam-cicd',
    version='0.0.1',
    author='ragy-abraham',
    author_email='ragy@rna.digital',
    description='CICD For apache beam',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)
