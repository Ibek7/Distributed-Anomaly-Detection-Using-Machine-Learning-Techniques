"""
Unit tests for the Distributed Anomaly Detection System

This module contains comprehensive tests for the Node class and main system
functionality to ensure code quality and reliability.
"""

import unittest
import sys
import os

# Add the distributed_anomaly_detection directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'distributed_anomaly_detection'))

from node import Node
from main import DistributedAnomalyDetectionSystem
import config


class TestNode(unittest.TestCase):
    """Test cases for the Node class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.node_info = {"info": "Test Node", "node_type": "Regular Node"}
        self.node = Node(node_id="test_node_1", cluster_id=0, info=self.node_info)
    
    def test_node_initialization(self):
        """Test node initialization with correct attributes."""
        self.assertEqual(self.node.node_id, "test_node_1")
        self.assertEqual(self.node.cluster_id, 0)
        self.assertEqual(self.node.info, self.node_info)
        self.assertEqual(self.node.charge, 100)  # Default initial charge
        self.assertFalse(self.node.is_cluster_head)
        self.assertFalse(self.node.is_central_node)
        self.assertFalse(self.node.is_non_cluster_head)
    
    def test_set_as_cluster_head(self):
        """Test setting node as cluster head."""
        self.node.set_as_cluster_head(150)
        self.assertTrue(self.node.is_cluster_head)
        self.assertFalse(self.node.is_non_cluster_head)
        self.assertEqual(self.node.charge, 150)
    
    def test_set_as_central_node(self):
        """Test setting node as central node."""
        self.node.set_as_central_node(200)
        self.assertTrue(self.node.is_central_node)
        self.assertFalse(self.node.is_non_cluster_head)
        self.assertEqual(self.node.charge, 200)
    
    def test_set_as_non_cluster_head(self):
        """Test setting node as regular node."""
        self.node.set_as_non_cluster_head(75)
        self.assertTrue(self.node.is_non_cluster_head)
        self.assertFalse(self.node.is_cluster_head)
        self.assertEqual(self.node.charge, 75)
    
    def test_energy_management(self):
        """Test energy consumption and management."""
        initial_charge = self.node.charge
        self.node.set_charge(50)
        self.assertEqual(self.node.charge, 50)
        
        # Test that charge doesn't go below 0
        self.node.set_charge(-10)
        self.assertEqual(self.node.charge, 0)
        
        # Test energy consumption logging
        self.node.set_charge(100)
        self.node.set_charge(80)  # Consume 20 units
        self.assertEqual(len(self.node.energy_consumption_log), 1)
        self.assertEqual(self.node.energy_consumption_log[0]["energy_consumed"], 20)
    
    def test_is_alive(self):
        """Test node alive status based on energy."""
        self.assertTrue(self.node.is_alive())
        
        self.node.set_charge(0)
        self.assertFalse(self.node.is_alive())
        
        self.node.set_charge(1)
        self.assertTrue(self.node.is_alive())
    
    def test_monitor_management(self):
        """Test adding monitors and monitored nodes."""
        self.node.add_monitor("monitor_1")
        self.node.add_monitor("monitor_2")
        self.assertEqual(len(self.node.monitored_by), 2)
        
        self.node.add_monitored_node("monitored_1")
        self.node.add_monitored_node("monitored_2")
        self.assertEqual(len(self.node.monitors), 2)
        
        # Test no duplicates
        self.node.add_monitor("monitor_1")
        self.assertEqual(len(self.node.monitored_by), 2)
    
    def test_data_transmission(self):
        """Test data transmission with energy consumption."""
        data = {"temperature": 25, "timestamp": 1}
        
        # Successful transmission
        result = self.node.transmit_data(data, 5)
        self.assertTrue(result)
        self.assertEqual(self.node.charge, 95)
        self.assertEqual(len(self.node.communication_log), 1)
        
        # Insufficient energy
        self.node.set_charge(3)
        result = self.node.transmit_data(data, 5)
        self.assertFalse(result)
        self.assertEqual(self.node.charge, 3)  # Charge unchanged
    
    def test_charge_info_exchange(self):
        """Test charge information sending and receiving."""
        # Create cluster head
        cluster_head_info = {"info": "Cluster Head", "node_type": "Cluster Head"}
        cluster_head = Node("cluster_head", 1, cluster_head_info)
        cluster_head.set_as_cluster_head()
        
        # Test successful charge info sending
        result = self.node.send_charge_info(cluster_head)
        self.assertTrue(result)
        
        # Test sending to non-cluster head (should fail)
        regular_node = Node("regular", 1, {"info": "Regular"})
        result = self.node.send_charge_info(regular_node)
        self.assertFalse(result)
    
    def test_anomaly_detection(self):
        """Test basic anomaly detection functionality."""
        # Set as cluster head to enable anomaly detection
        self.node.set_as_cluster_head()
        
        # Test normal case
        result = self.node.check_for_attack()
        self.assertFalse(result["attack_detected"])
        
        # Test with suspicious charge information
        self.node.charge_info = {"source_node": "test_source", "charge": -5}
        result = self.node.check_for_attack()
        self.assertTrue(result["attack_detected"])
        self.assertEqual(result["attack_type"], "Invalid Charge")
    
    def test_energy_stats(self):
        """Test energy statistics generation."""
        # Consume some energy
        self.node.set_charge(80)
        self.node.set_charge(60)
        
        stats = self.node.get_energy_stats()
        
        self.assertEqual(stats["node_id"], "test_node_1")
        self.assertEqual(stats["current_charge"], 60)
        self.assertEqual(stats["total_energy_consumed"], 40)
        self.assertTrue(stats["is_alive"])
        self.assertEqual(stats["consumption_events"], 2)


class TestDistributedAnomalyDetectionSystem(unittest.TestCase):
    """Test cases for the main system class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use smaller network for faster testing
        self.original_network_size = config.NETWORK_SIZE
        self.original_num_clusters = config.NUM_CLUSTERS
        config.NETWORK_SIZE = 20
        config.NUM_CLUSTERS = 3
        
        self.system = DistributedAnomalyDetectionSystem()
    
    def tearDown(self):
        """Restore original configuration after tests."""
        config.NETWORK_SIZE = self.original_network_size
        config.NUM_CLUSTERS = self.original_num_clusters
    
    def test_network_generation(self):
        """Test network generation with correct number of nodes."""
        self.system.generate_network()
        
        self.assertEqual(len(self.system.dataset), config.NETWORK_SIZE)
        self.assertEqual(len(self.system.node_info), config.NETWORK_SIZE)
        self.assertIn(self.system.central_node_id, self.system.node_info)
    
    def test_node_object_creation(self):
        """Test creation of node objects."""
        self.system.generate_network()
        self.system.create_node_objects()
        
        self.assertEqual(len(self.system.node_objects), config.NETWORK_SIZE)
        
        # Check central node is properly set
        central_node = self.system.node_objects[self.system.central_node_id]
        self.assertTrue(central_node.is_central_node)
    
    def test_clustering(self):
        """Test K-means clustering functionality."""
        self.system.generate_network()
        self.system.create_node_objects()
        self.system.perform_clustering()
        
        self.assertLessEqual(len(self.system.clusters), config.NUM_CLUSTERS)
        self.assertEqual(len(self.system.cluster_centers), config.NUM_CLUSTERS)
    
    def test_cluster_head_assignment(self):
        """Test cluster head assignment."""
        self.system.generate_network()
        self.system.create_node_objects()
        self.system.perform_clustering()
        self.system.assign_cluster_heads()
        
        # Check that cluster heads are assigned
        cluster_heads_count = sum(
            1 for node in self.system.node_objects.values() 
            if node.is_cluster_head
        )
        self.assertGreater(cluster_heads_count, 0)
        self.assertLessEqual(cluster_heads_count, config.NUM_CLUSTERS)
    
    def test_simulation_stats_tracking(self):
        """Test that simulation statistics are properly tracked."""
        initial_stats = self.system.simulation_stats.copy()
        
        # All stats should start at 0
        for key, value in initial_stats.items():
            self.assertEqual(value, 0)
        
        # Stats should be updated during simulation
        # (This would be more thoroughly tested in integration tests)


class TestConfiguration(unittest.TestCase):
    """Test cases for configuration management."""
    
    def test_config_values(self):
        """Test that configuration values are reasonable."""
        self.assertGreater(config.NETWORK_SIZE, 0)
        self.assertGreater(config.NUM_CLUSTERS, 0)
        self.assertGreater(config.INITIAL_CHARGE, 0)
        self.assertGreaterEqual(config.TRANSMISSION_COST, 0)
        self.assertGreaterEqual(config.RECEPTION_COST, 0)
        self.assertGreater(config.SIMULATION_TIME, 0)


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)