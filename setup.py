import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_desc_py'

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths
extra_files = package_files('models')

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    py_modules=[
        'nodes.speed_controller'
    ],

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'sensors'), glob('sensors/*')),
        # (os.path.join('share', package_name, 'models'), glob('models/*')),
        # (os.path.join('share', package_name, 'models'), glob('models/**', recursive=True)),
        ('share/' + package_name + '/models', extra_files),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('lib', package_name), glob('nodes/*.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='msdelta',
    maintainer_email='m.munozs.2020@alumnos.urjc.es',
    description='MSR: robot description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tf_transformations_node = robot_desc_py.tf_transformations_node:main',
            'tf2_simple_node = robot_desc_py.tf2_simple_node:main',
            'speed_controller = nodes.speed_controller:main'
        ],
    },
)
