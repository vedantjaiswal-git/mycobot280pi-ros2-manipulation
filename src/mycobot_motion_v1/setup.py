from setuptools import find_packages, setup

package_name = 'mycobot_motion_v1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Project CoBOT Team',
    maintainer_email='project-cobot@example.com',
    description='Vision-driven MyCobot 280Pi pick-and-place motion node.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['motion_node = mycobot_motion_v1.motion_node:main'],
    },
)
