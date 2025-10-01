#!/usr/bin/env python3
"""
Example usage of the Distributed Anomaly Detection System

This script demonstrates how to use the improved system with custom configurations
and shows various features including energy monitoring and anomaly detection.
"""

import sys
import os
import logging

# Add the distributed_anomaly_detection directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'distributed_anomaly_detection'))

from main import DistributedAnomalyDetectionSystem
import config

# Configure logging for demo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_basic_example():
    """Run a basic example with default configuration."""
    logger.info("Running basic example with default configuration")
    
    system = DistributedAnomalyDetectionSystem()
    
    # Generate and set up the network
    system.generate_network()
    system.create_node_objects()
    system.perform_clustering()
    system.assign_cluster_heads()
    system.assign_monitors_and_charges()
    
    # Run simulation
    system.run_simulation()
    
    # Print results
    system.print_network_summary()


def run_custom_example():
    """Run an example with custom configuration."""
    logger.info("Running custom example with modified configuration")
    
    # Temporarily modify configuration
    original_network_size = config.NETWORK_SIZE
    original_simulation_time = config.SIMULATION_TIME
    original_num_clusters = config.NUM_CLUSTERS
    
    try:
        # Use smaller network for faster execution
        config.NETWORK_SIZE = 50
        config.SIMULATION_TIME = 5
        config.NUM_CLUSTERS = 8
        
        system = DistributedAnomalyDetectionSystem()
        
        # Setup and run
        system.generate_network()
        system.create_node_objects()
        system.perform_clustering()
        system.assign_cluster_heads()
        system.assign_monitors_and_charges()
        system.run_simulation()
        
        # Display results
        system.print_network_summary()
        
        # Demonstrate energy analysis
        print("\n" + "="*50)
        print("DETAILED ENERGY ANALYSIS")
        print("="*50)
        
        for node_id, node in list(system.node_objects.items())[:5]:  # Show first 5 nodes
            stats = node.get_energy_stats()
            print(f"Node {stats['node_id'][:15]}...")
            print(f"  Current Charge: {stats['current_charge']}")
            print(f"  Total Consumed: {stats['total_energy_consumed']}")
            print(f"  Efficiency: {stats['energy_efficiency']:.2%}")
            print(f"  Status: {'Alive' if stats['is_alive'] else 'Dead'}")
            print()
            
    finally:
        # Restore original configuration
        config.NETWORK_SIZE = original_network_size
        config.SIMULATION_TIME = original_simulation_time
        config.NUM_CLUSTERS = original_num_clusters


def demonstrate_node_features():
    """Demonstrate individual node features."""
    logger.info("Demonstrating individual node features")
    
    from node import Node
    
    print("\n" + "="*50)
    print("NODE FEATURE DEMONSTRATION")
    print("="*50)
    
    # Create sample nodes
    node_info = {"info": "Demo IoT Sensor", "node_type": "Regular Node"}
    node1 = Node("demo_node_1", 0, node_info)
    node2 = Node("demo_cluster_head", 0, node_info)
    
    # Demonstrate role assignment
    node2.set_as_cluster_head(150)
    node1.set_as_non_cluster_head(100)
    
    print(f"Node 1: {node1}")
    print(f"Node 2: {node2}")
    
    # Demonstrate monitoring setup
    node1.add_monitor("monitor_node_1")
    node1.add_monitor("monitor_node_2")
    print(f"Node 1 monitored by: {node1.monitored_by}")
    
    # Demonstrate data transmission
    sensor_data = {"temperature": 22.5, "humidity": 65, "timestamp": 1234567890}
    success = node1.transmit_data(sensor_data, energy_cost=2)
    print(f"Data transmission successful: {success}")
    print(f"Node 1 energy after transmission: {node1.charge}")
    
    # Demonstrate energy statistics
    stats = node1.get_energy_stats()
    print(f"Energy efficiency: {stats['energy_efficiency']:.2%}")
    
    # Demonstrate anomaly detection
    attack_result = node2.check_for_attack()
    print(f"Attack detection result: {attack_result['details']}")


def main():
    """Main function to run all examples."""
    print("Distributed Anomaly Detection System - Examples")
    print("=" * 60)
    
    try:
        # Run different examples
        print("\n1. BASIC EXAMPLE")
        print("-" * 20)
        # Note: Commenting out to avoid long execution during demo
        # Uncomment the next line to run the full basic example
        # run_basic_example()
        print("Skipping basic example (uncomment in script to run)")
        
        print("\n2. CUSTOM CONFIGURATION EXAMPLE")
        print("-" * 35)
        run_custom_example()
        
        print("\n3. NODE FEATURES DEMONSTRATION")
        print("-" * 35)
        demonstrate_node_features()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Example execution failed: {e}")
        raise


if __name__ == "__main__":
    main()