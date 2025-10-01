"""
Distributed Anomaly Detection Using Machine Learning Techniques

This package implements a distributed anomaly detection system for IoT networks
using K-means clustering and machine learning techniques.

Modules:
    - main: Main simulation runner
    - node: Node class implementation with energy management
    - config: Configuration parameters for the system
"""

__version__ = "1.1.0"
__author__ = "Contributors"
__email__ = "see GitHub repository for contact info"

from .node import Node
from .config import *

__all__ = [
    'Node',
    'DistributedAnomalyDetectionSystem'
]