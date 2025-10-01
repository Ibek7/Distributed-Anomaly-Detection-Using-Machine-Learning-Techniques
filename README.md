# Distributed Anomaly Detection Using Machine Learning Techniques

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🔍 Overview

This project implements a **distributed anomaly detection system** for IoT networks using machine learning techniques. The system addresses security concerns in IoT environments, particularly targeting denial of service (DoS) attacks and other malicious activities that could compromise network integrity.

### Key Features

- **🎯 Distributed Architecture**: Implements a charge-assignment algorithm for efficient monitoring
- **🤖 Machine Learning**: Uses K-means clustering for optimal network organization
- **⚡ Energy Efficient**: Minimizes power consumption through intelligent clustering
- **🛡️ Security Focused**: Real-time anomaly detection and threat identification
- **📊 Comprehensive Monitoring**: Dual-phase behavior analysis system
- **🔧 Configurable**: Easy-to-modify parameters for different network sizes

## 📊 Abstract

The Internet of Things (IoTs) represents a network of physical objects that use sensors to collect data and transmit them to a central hub. Security in IoT networks has become increasingly critical, especially in applications like healthcare where lives may be at stake. These networks are typically vulnerable to security attacks such as denial of service (DoS) attacks.

Our solution proposes a **distributed anomaly detection system** that:

1. Uses a **charge-assignment algorithm** to assign two charges to each node in a cluster
2. Implements **dual-role nodes** serving as both monitors and charges
3. Features a **behavior-analysis algorithm** with two phases:
   - Behavior assessment phase (learns normal node behavior)
   - Machine learning assessment phase (continuous behavior evaluation)
4. Enables **selective deactivation** of only faulty nodes while maintaining network integrity

## 🏗️ System Architecture

```
    Central Node
         |
    ┌────┴────┐
    │ Cluster │ Cluster Head
    │ Head 1  │ ← monitors → Charges
    └─────────┘
         |
    ┌────┴────┐
    │Regular  │ ← monitors → Other Nodes
    │Nodes    │
    └─────────┘
```

### Components

- **Central Node**: Collects and processes data from all cluster heads
- **Cluster Heads**: Manage their respective clusters and relay information
- **Regular Nodes**: IoT devices that collect sensor data and participate in monitoring
- **Monitoring System**: Each node monitors others for anomalous behavior

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mian-abd/Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques.git
   cd Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the simulation**:
   ```bash
   cd distributed_anomaly_detection
   python main.py
   ```

### Alternative: Install individual packages
```bash
pip install pyclustering scipy numpy matplotlib
```

## 📁 Project Structure

```
Distributed-Anomaly-Detection-ML/
├── distributed_anomaly_detection/
│   ├── main.py              # Main simulation runner (improved)
│   ├── node.py              # Enhanced Node class with better error handling
│   ├── config.py            # Configuration parameters
│   ├── Kmeans.py            # Original K-means implementation
│   ├── values3.txt          # Sample dataset
│   └── README.md            # Module documentation
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

## ⚙️ Configuration

The system can be easily configured by modifying `distributed_anomaly_detection/config.py`:

```python
# Network Configuration
NETWORK_SIZE = 201          # Number of nodes
NUM_CLUSTERS = 20           # Number of clusters
INITIAL_CHARGE = 100        # Starting energy for nodes

# Energy Model
TRANSMISSION_COST = 1       # Energy cost per transmission
RECEPTION_COST = 0.5        # Energy cost per reception

# Simulation Parameters
SIMULATION_TIME = 10        # Simulation duration (minutes)
```

## 🔧 Usage Examples

### Basic Simulation
```python
from main import DistributedAnomalyDetectionSystem

# Create and run system
system = DistributedAnomalyDetectionSystem()
system.generate_network()
system.create_node_objects()
system.perform_clustering()
system.assign_cluster_heads()
system.assign_monitors_and_charges()
system.run_simulation()
system.print_network_summary()
```

### Custom Configuration
```python
# Modify config.py or override parameters
import config
config.NETWORK_SIZE = 100
config.NUM_CLUSTERS = 10
config.SIMULATION_TIME = 5

# Run with custom settings
system = DistributedAnomalyDetectionSystem()
# ... rest of the setup
```

## 📈 Results and Analysis

The simulation provides comprehensive insights into:

- **Energy Consumption**: Track power usage across the network
- **Anomaly Detection**: Identify security threats and malicious behavior  
- **Network Performance**: Monitor communication efficiency
- **Node Reliability**: Assess individual node performance

### Sample Output
```
==================================================
NETWORK SUMMARY
==================================================
Total Nodes: 201
Central Node: [25, 30, 15]
Number of Clusters: 20
Cluster Heads: 18

ENERGY STATISTICS:
Average Node Energy: 85.23
Failed Nodes: 3

SIMULATION RESULTS:
Messages Transmitted: 1,847
Anomalies Detected: 2
==================================================
```

## 🧪 Testing and Validation

The system has been validated using:
- **Simulated IoT environments** with 24, 48, and 96 devices
- **NS-3 network simulator** for realistic network conditions
- **Various attack scenarios** including DoS and data injection attacks

### Performance Metrics
- ✅ **Single faulty node detection** per cluster
- ✅ **Distributed processing** capabilities
- ✅ **Energy-efficient** operation
- ✅ **Scalable architecture** for large networks

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Improve code, add features, fix bugs
4. **Add tests**: Ensure your changes work correctly
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution
- 🔧 Algorithm improvements
- 📊 Enhanced visualization
- 🧪 Additional test cases
- 📚 Documentation improvements
- 🛡️ New security features

## 📚 Research and References

This implementation is based on research in:
- Distributed systems security
- IoT network anomaly detection
- Machine learning for cybersecurity
- Energy-efficient networking protocols

### Key Research Areas
- **Behavioral Analysis**: Understanding normal vs. anomalous node behavior
- **Energy Optimization**: Minimizing power consumption in resource-constrained environments
- **Distributed Computing**: Efficient algorithm distribution across network nodes
- **Security Protocols**: Protecting against various attack vectors

## 🐛 Known Issues and Limitations

- **Scalability**: Performance may degrade with networks >1000 nodes
- **Energy Model**: Simplified energy consumption model
- **Attack Types**: Currently focuses on DoS and charge-based attacks
- **Real-time**: Simulation-based, not real-time implementation

## 🔮 Future Enhancements

- [ ] **Real-time Implementation**: Deploy on actual IoT hardware
- [ ] **Advanced ML Models**: Implement deep learning approaches
- [ ] **Enhanced Security**: Add cryptographic protections
- [ ] **Mobile Nodes**: Support for moving IoT devices
- [ ] **GUI Interface**: Web-based monitoring dashboard
- [ ] **Database Integration**: Persistent data storage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors and Acknowledgments

- **Original Authors**: Research team behind the distributed anomaly detection algorithm
- **Contributors**: Community members improving and extending the codebase
- **Special Thanks**: To the IoT security research community

## 📞 Support and Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/mian-abd/Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mian-abd/Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques/discussions)
- 📧 **Email**: Create an issue for direct contact

---

⭐ **Star this repository** if you find it useful!

**Keywords**: IoT Security, Anomaly Detection, Machine Learning, Distributed Systems, K-means Clustering, Energy Efficiency, Cybersecurity