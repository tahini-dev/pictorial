from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

install_requires = [
    'pandas>=1.1.0',
    'plotly',
    'numpy',
]

extras_require = {
    # 'plotly': ['plotly'],
}

extras_require['all'] = sorted(set(sum(extras_require.values(), [])))

setup(
    name='pictorial',
    version='2021.11.2',
    author='tahini-dev',
    author_email='tahini.dev@gmail.com',
    description='Python package for plotting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tahini-dev/pictorial',
    packages=find_packages(exclude=('tests',)),
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.7',
    include_package_data=True,
)
