from setuptools import find_packages, setup

package_name = 'leg_point_pub'

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
    maintainer='tsaqip',
    maintainer_email='tsqifahmd@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'move_leg = leg_point_pub.movement_publisher:main',
            'test_loky_x = leg_point_pub.moveTest_tripod_sumbuX:main'
        ],
    },
)
