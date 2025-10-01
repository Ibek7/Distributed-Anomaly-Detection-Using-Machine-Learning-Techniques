# Distributed Anomaly Detection Module

This directory contains the core implementation of the distributed anomaly detection system.

## Files

- **`main.py`**: Enhanced main simulation runner with improved error handling, logging, and modular design
- **`node.py`**: Improved Node class with comprehensive energy management, type hints, and better documentation
- **`config.py`**: Centralized configuration file for easy parameter management
- **`Kmeans.py`**: Original K-means clustering implementation (preserved for compatibility)
- **`values3.txt`**: Sample dataset with node coordinates and cluster information

## Key Improvements

### Enhanced Node Class (`node.py`)
- Added type hints for better code documentation
- Improved energy management with consumption tracking
- Better monitoring system with lists instead of fixed variables
- Enhanced anomaly detection with multiple attack types
- Comprehensive logging support
- Energy statistics and node health monitoring

### Modular Design (`main.py`)
- Object-oriented approach with `DistributedAnomalyDetectionSystem` class
- Separation of concerns with dedicated methods for each phase
- Comprehensive error handling and logging
- Statistics tracking throughout simulation
- Configurable parameters via `config.py`
- Better visualization support

### Configuration Management (`config.py`)
- Centralized parameter management
- Easy customization of network size, energy models, and simulation settings
- Clear documentation for each parameter
- Separation of different configuration categories

## Usage

```python
# Import the improved system
from main import DistributedAnomalyDetectionSystem

# Create and run simulation
system = DistributedAnomalyDetectionSystem()
system.generate_network()
system.create_node_objects()
system.perform_clustering()
system.assign_cluster_heads()
system.assign_monitors_and_charges()
system.run_simulation()
system.print_network_summary()
```

## Backward Compatibility

The original `Kmeans.py` file is preserved to maintain backward compatibility with existing usage patterns while the new modular system provides enhanced functionality.