"""
Configuration file for Distributed Anomaly Detection System

This module contains all configurable parameters for the distributed
anomaly detection system including network parameters, clustering settings,
and simulation parameters.
"""

# Network Configuration
NETWORK_SIZE = 201  # Number of nodes in the network
COORDINATE_RANGE = (1, 50)  # Range for generating random coordinates
DIMENSIONS = 3  # Number of dimensions for node coordinates

# Clustering Configuration
NUM_CLUSTERS = 20  # Number of clusters for K-means
INITIAL_SEED = None  # Random seed for reproducibility (None for random)

# Energy Model Configuration
INITIAL_CHARGE = 100  # Initial energy charge for all nodes
TRANSMISSION_COST = 1  # Energy cost for transmitting data
RECEPTION_COST = 0.5  # Energy cost for receiving data (cluster heads)

# Simulation Parameters
SIMULATION_TIME = 10  # Total simulation time in minutes
DATA_COLLECTION_INTERVAL = 1  # How often nodes collect data (minutes)
CENTRAL_TRANSMISSION_INTERVAL = 5  # How often cluster heads send to central node

# Temperature Simulation
TEMP_MIN = 20  # Minimum temperature reading
TEMP_MAX = 30  # Maximum temperature reading

# Monitoring Configuration
MONITORS_PER_NODE = 2  # Number of monitors assigned to each node

# Logging Configuration
ENABLE_DETAILED_LOGGING = True
LOG_COMMUNICATION = True
LOG_ENERGY_CONSUMPTION = True

# Visualization Configuration
SHOW_CLUSTER_VISUALIZATION = True
FIGURE_SIZE = (12, 8)