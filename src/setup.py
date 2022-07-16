import setuptools

REQUIRED_PACKAGES = [
    "wheel",
    "setuptools",
    "python-dotenv",
    "cryptography",
    "google-cloud-redis",
    "google-api-python-client",
    "google-cloud-bigquery",
    "google-cloud-redis",
    "google-cloud-core",
    "google-cloud-secret-manager",
    "inflection",
    "pycryptodome",
    "PyMySQL",
    "ua-parser",
    "user-agents",
    "redis"
]

setuptools.setup(
    name='beam-summit-streaming-pipeline',
    version='1.0.0',
    author='ragy-abraham',
    author_email='ragy@rna.digital',
    description='This is a streaming pipeline used as a demo at the beam summit 2022',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)
