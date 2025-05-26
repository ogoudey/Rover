from setuptools import find_packages, setup

package_name = 'rover'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'gpiozero', 'pygame'],
    zip_safe=True,
    maintainer='olin',
    maintainer_email='olin.goog@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
        'keyboard = rover.input:main',
        'motors = rover.motors:main',
        ],
    },
)
