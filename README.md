## Summary

## Development environment
Code for generating the dataset, as well as the code for training the neural networks is developed on Ubuntu 19.04 OS. Following hardware specification consists of:
- CPU: Intel Core i7-4770 CPU @ 3.40GHz x 8
- GPU karta: GeForce GTX 1080 Ti/PCIe/SSE2
- RAM: Kingston HyperX Fury Red 16 GB (2 x 8 GB)

The chosen language is Python  3.6. The reason being is a wast number of functionalities, libraries and fast development rate. Most significant, used Python libraries, are:
- TensorFlow v1.11.0
- PyCrypto v2.6.1
- NumPy v1.16.3
- Scikit-learn v0.21
- TensorBoard v1.11.0

from which TensorFlow is the major for training the neural network, while PyCrypto for generating training dataset.

To execute experiments as optimal as possible, CUDA drivers are used alongside GPU drivers. This enables TensorFlow to do all calculations directly on GPU and by that to speed up the training process of the network.

For having an easier way for adjustment and setup, Docker is used with Nvidia support. This enables an isolated environment for development and testing.

## Results
