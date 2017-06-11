from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='ansible_jupyter_kernel',
    version='0.1',
    description='An Ansible kernel for Jupyter',
    long_description=readme,
    author='Beni Cherniavsky-Paskin',
    author_email='cben@redhat.com',
    url='https://github.com/cben/ansible_jupyter_kernel',
    license='GPLv3',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # TODO: Probably works on python 2 as well?
        'Programming Language :: Python :: 3',
    ],

    install_requires=[
        'ansible',
        'ipykernel',
        'jupyter_client >= 5.0.0', # allows 'python' without path in kernel.json
    ],

    py_modules=['ansible_jupyter_kernel'],
    data_files=[
        ('share/jupyter/kernels/ansible_jupyter', ['kernel.json']),
    ],
)
