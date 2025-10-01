"""
Improved Distributed Anomaly Detection System using K-means Clustering

This module implements a distributed anomaly detection system for IoT networks
using K-means clustering, with improved error handling, logging, and configuration management.
"""

import warnings
import random
import logging
import numpy as np
from typing import List, Dict, Tuple, Any
import matplotlib.pyplot as plt

from node import Node
from config import *
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from scipy.spatial.distance import euclidean

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress future warnings to maintain clean output
warnings.simplefilter(action='ignore', category=FutureWarning)


class DistributedAnomalyDetectionSystem:
    """
    Main class for the distributed anomaly detection system.
    
    This class manages the entire IoT network simulation including:
    - Node generation and clustering
    - Role assignment (cluster heads, monitors)
    - Energy management
    - Anomaly detection
    - Data collection and analysis
    """
    
    def __init__(self):
        """Initialize the distributed anomaly detection system."""
        self.dataset: List[List[int]] = []
        self.node_info: Dict[str, Dict[str, Any]] = {}
        self.node_objects: Dict[str, Node] = {}
        self.central_node_id: str = ""
        self.clusters: List[List[int]] = []
        self.cluster_centers: List[List[float]] = []
        self.cluster_heads: Dict[int, str] = {}  # cluster_id -> node_id mapping
        
        # Statistics tracking
        self.simulation_stats = {
            "total_energy_consumed": 0,
            "anomalies_detected": 0,
            "messages_transmitted": 0,
            "nodes_failed": 0
        }
        
        logger.info("Distributed Anomaly Detection System initialized")
    
    def generate_network(self) -> None:
        """Generate the IoT network with random node positions."""
        logger.info(f"Generating network with {NETWORK_SIZE} nodes")
        
        # Set random seed for reproducibility if specified
        if INITIAL_SEED is not None:
            random.seed(INITIAL_SEED)
            np.random.seed(INITIAL_SEED)
        
        # Generate dataset with random points in 3D space
        self.dataset = [
            [random.randint(*COORDINATE_RANGE) for _ in range(DIMENSIONS)] 
            for _ in range(NETWORK_SIZE)
        ]
        
        # Assign unique information to each point in the dataset
        for i, point in enumerate(self.dataset):
            point_key = str(point)
            self.node_info[point_key] = {
                "info": f"IoT Sensor Node {i}",
                "node_type": "Regular Node",
                "temperature_readings": [],
                "creation_time": 0
            }
        
        # Randomly select a node as the central node
        self.central_node_id = random.choice(list(self.node_info.keys()))
        
        logger.info(f"Network generated with central node: {self.central_node_id}")
    
    def create_node_objects(self) -> None:
        """Create Node objects for all points in the network."""
        logger.info("Creating node objects")
        
        for i, (point_key, info) in enumerate(self.node_info.items()):
            self.node_objects[point_key] = Node(
                node_id=point_key, 
                cluster_id=i, 
                info=info
            )
            
            # Set central node
            if point_key == self.central_node_id:
                self.node_objects[point_key].set_as_central_node(INITIAL_CHARGE)
        
        logger.info(f"Created {len(self.node_objects)} node objects")
    
    def perform_clustering(self) -> None:
        """Perform K-means clustering on the network nodes."""
        logger.info(f"Performing K-means clustering with {NUM_CLUSTERS} clusters")
        
        # Prepare initial centers
        initial_centers = np.array(self.dataset)[
            np.random.choice(len(self.dataset), size=NUM_CLUSTERS, replace=False)
        ]
        
        # Create and run K-means instance
        kmeans_instance = kmeans(self.dataset, initial_centers)
        kmeans_instance.process()
        
        self.clusters = kmeans_instance.get_clusters()
        self.cluster_centers = kmeans_instance.get_centers()
        
        logger.info(f"Clustering completed. Created {len(self.clusters)} clusters")
        
        # Show visualization if enabled
        if SHOW_CLUSTER_VISUALIZATION:
            try:
                plt.figure(figsize=FIGURE_SIZE)
                kmeans_visualizer.show_clusters(self.dataset, self.clusters, self.cluster_centers)
                logger.info("Cluster visualization displayed")
            except Exception as e:
                logger.warning(f"Could not display visualization: {e}")
    
    def assign_cluster_heads(self) -> None:
        """Assign cluster heads based on proximity to cluster centers."""
        logger.info("Assigning cluster heads")
        
        for cluster_id, cluster in enumerate(self.clusters):
            if not cluster:  # Skip empty clusters
                continue
                
            cluster_points = [self.dataset[idx] for idx in cluster]
            cluster_center = self.cluster_centers[cluster_id]
            
            # Find point closest to cluster center
            min_distance = float('inf')
            cluster_head_point = None
            
            for point in cluster_points:
                distance = euclidean(cluster_center, point)
                if distance < min_distance:
                    min_distance = distance
                    cluster_head_point = point
            
            if cluster_head_point is not None:
                cluster_head_key = str(cluster_head_point)
                cluster_head_node = self.node_objects[cluster_head_key]
                cluster_head_node.set_as_cluster_head(INITIAL_CHARGE)
                
                # Update node info and tracking
                self.node_info[cluster_head_key]["node_type"] = "Cluster Head"
                self.cluster_heads[cluster_id] = cluster_head_key
                
                logger.debug(f"Cluster {cluster_id} head assigned to node {cluster_head_key}")
        
        logger.info(f"Assigned {len(self.cluster_heads)} cluster heads")
    
    def assign_monitors_and_charges(self) -> None:
        """Assign monitoring relationships between nodes."""
        logger.info("Assigning monitors and charges")
        
        for cluster_id, cluster in enumerate(self.clusters):
            if cluster_id not in self.cluster_heads:
                continue
                
            cluster_head_key = self.cluster_heads[cluster_id]
            cluster_head_node = self.node_objects[cluster_head_key]
            
            # Get all non-cluster head nodes in this cluster
            cluster_points = [self.dataset[idx] for idx in cluster]
            non_cluster_head_points = [
                point for point in cluster_points 
                if not self.node_objects[str(point)].is_cluster_head
            ]
            
            if len(non_cluster_head_points) < MONITORS_PER_NODE:
                logger.warning(f"Cluster {cluster_id} has insufficient nodes for monitoring")
                continue
            
            # Assign monitors for each non-cluster head node
            for point in non_cluster_head_points:
                node_key = str(point)
                node = self.node_objects[node_key]
                node.set_as_non_cluster_head(INITIAL_CHARGE)
                
                # Update node info
                self.node_info[node_key]["node_type"] = "Regular Node"
                
                # Choose monitors (other nodes in the same cluster)
                available_monitors = [
                    str(p) for p in non_cluster_head_points 
                    if p != point
                ]
                
                if len(available_monitors) >= MONITORS_PER_NODE:
                    selected_monitors = random.sample(available_monitors, MONITORS_PER_NODE)
                    
                    for monitor_id in selected_monitors:
                        node.add_monitor(monitor_id)
                        self.node_objects[monitor_id].add_monitored_node(node_key)
                    
                    # Send charge info to cluster head
                    node.send_charge_info(cluster_head_node)
        
        logger.info("Monitor and charge assignment completed")
    
    def simulate_data_collection(self, minute: int) -> None:
        """
        Simulate data collection for one time interval.
        
        Args:
            minute (int): Current simulation minute.
        """
        for node_id, node in self.node_objects.items():
            if not node.is_alive():
                continue
                
            # Generate temperature reading
            temperature = random.randint(TEMP_MIN, TEMP_MAX)
            
            # Create data packet
            data_packet = {
                "timestamp": minute,
                "node_id": node_id,
                "temperature": temperature,
                "charge_level": node.charge,
                "data_type": "sensor_reading"
            }
            
            # Transmit data with energy cost
            if node.transmit_data(data_packet, TRANSMISSION_COST):
                self.simulation_stats["messages_transmitted"] += 1
                
                # If node is a cluster head, it also receives data (additional cost)
                if node.is_cluster_head:
                    node.set_charge(node.charge - RECEPTION_COST)
    
    def send_to_central_node(self, minute: int) -> None:
        """
        Send collected data from cluster heads to central node.
        
        Args:
            minute (int): Current simulation minute.
        """
        logger.info(f"Minute {minute}: Sending data to central node")
        
        central_node = self.node_objects[self.central_node_id]
        total_data_packets = 0
        
        # Collect data from all cluster heads
        for cluster_head_id in self.cluster_heads.values():
            cluster_head = self.node_objects[cluster_head_id]
            
            if cluster_head.is_alive() and cluster_head.communication_log:
                total_data_packets += len(cluster_head.communication_log)
                cluster_head.reset_communication_log()
        
        # Central node consumes energy proportional to data received
        energy_cost = min(total_data_packets, central_node.charge)
        central_node.set_charge(central_node.charge - energy_cost)
        
        logger.info(f"Central node processed {total_data_packets} data packets")
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        Perform anomaly detection across all cluster heads.
        
        Returns:
            List[Dict[str, Any]]: List of detected anomalies.
        """
        anomalies = []
        
        for cluster_head_id in self.cluster_heads.values():
            cluster_head = self.node_objects[cluster_head_id]
            
            if cluster_head.is_alive():
                attack_result = cluster_head.check_for_attack()
                
                if attack_result["attack_detected"]:
                    anomalies.append(attack_result)
                    self.simulation_stats["anomalies_detected"] += 1
        
        return anomalies
    
    def run_simulation(self) -> None:
        """Run the complete simulation for the specified time interval."""
        logger.info(f"Starting simulation for {SIMULATION_TIME} minutes")
        
        for minute in range(SIMULATION_TIME):
            logger.info(f"Simulation minute {minute + 1}/{SIMULATION_TIME}")
            
            # Collect data from all nodes
            self.simulate_data_collection(minute)
            
            # Send data to central node every N minutes
            if (minute + 1) % CENTRAL_TRANSMISSION_INTERVAL == 0:
                self.send_to_central_node(minute)
            
            # Detect anomalies
            anomalies = self.detect_anomalies()
            if anomalies:
                logger.warning(f"Detected {len(anomalies)} anomalies at minute {minute + 1}")
                for anomaly in anomalies:
                    logger.warning(f"  - {anomaly['attack_type']}: {anomaly['details']}")
            
            # Check for failed nodes
            failed_nodes = [
                node_id for node_id, node in self.node_objects.items() 
                if not node.is_alive()
            ]
            
            new_failures = len(failed_nodes) - self.simulation_stats["nodes_failed"]
            if new_failures > 0:
                self.simulation_stats["nodes_failed"] = len(failed_nodes)
                logger.warning(f"Total failed nodes: {len(failed_nodes)}")
        
        logger.info("Simulation completed")
    
    def print_network_summary(self) -> None:
        """Print a summary of the network configuration and simulation results."""
        print("\n" + "="*50)
        print("NETWORK SUMMARY")
        print("="*50)
        
        print(f"Total Nodes: {len(self.node_objects)}")
        print(f"Central Node: {self.central_node_id}")
        print(f"Number of Clusters: {len(self.clusters)}")
        print(f"Cluster Heads: {len(self.cluster_heads)}")
        
        # Energy statistics
        total_energy = sum(node.charge for node in self.node_objects.values())
        avg_energy = total_energy / len(self.node_objects)
        
        print(f"\nENERGY STATISTICS:")
        print(f"Average Node Energy: {avg_energy:.2f}")
        print(f"Failed Nodes: {self.simulation_stats['nodes_failed']}")
        
        print(f"\nSIMULATION RESULTS:")
        print(f"Messages Transmitted: {self.simulation_stats['messages_transmitted']}")
        print(f"Anomalies Detected: {self.simulation_stats['anomalies_detected']}")
        
        # Print cluster head information
        print(f"\nCLUSTER HEADS:")
        for cluster_id, head_id in self.cluster_heads.items():
            head_node = self.node_objects[head_id]
            print(f"Cluster {cluster_id}: Node {head_id} (Energy: {head_node.charge})")
        
        print("="*50)


def main():
    """Main function to run the distributed anomaly detection system."""
    logger.info("Starting Distributed Anomaly Detection System")
    
    try:
        # Initialize system
        system = DistributedAnomalyDetectionSystem()
        
        # Setup network
        system.generate_network()
        system.create_node_objects()
        system.perform_clustering()
        system.assign_cluster_heads()
        system.assign_monitors_and_charges()
        
        # Run simulation
        system.run_simulation()
        
        # Print results
        system.print_network_summary()
        
        logger.info("System execution completed successfully")
        
    except Exception as e:
        logger.error(f"System execution failed: {e}")
        raise


if __name__ == "__main__":
    main()