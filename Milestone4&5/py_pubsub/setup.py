from setuptools import find_packages, setup

package_name = 'py_pubsub'

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
    description='Examples of minimal publisher/subscriber using rclpy',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'talker_fk = py_pubsub.publisher_fk:main',
            'listener = py_pubsub.subscriber_member_function:main',
            'listener_ik = py_pubsub.listener_ik:main',
        ],
    },
)
