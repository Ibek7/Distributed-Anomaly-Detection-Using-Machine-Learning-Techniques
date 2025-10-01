import logging
from typing import List, Dict, Optional, Any


class Node:
    """
    Represents a node in the distributed IoT network.
    
    A node can serve multiple roles: regular node, cluster head, or central node.
    Each node has monitoring capabilities and energy management features.
    """
    
    def __init__(self, node_id: str, cluster_id: int, info: Dict[str, Any]):
        """
        Initialize a Node instance.

        Args:
            node_id (str): Unique identifier for the node.
            cluster_id (int): Identifier for the cluster to which the node belongs.
            info (Dict[str, Any]): Information or description associated with the node.
        """
        # Basic node properties
        self.node_id = node_id
        self.cluster_id = cluster_id
        self.info = info
        
        # Communication and monitoring
        self.communication_log: List[Dict[str, Any]] = []
        self.monitors: List[str] = []  # Nodes this node is monitoring
        self.monitored_by: List[str] = []  # Nodes monitoring this node
        
        # Energy management
        self.charge = 100  # Initial energy charge
        self.energy_consumption_log: List[Dict[str, Any]] = []
        
        # Node roles
        self.is_cluster_head = False
        self.is_central_node = False
        self.is_non_cluster_head = False
        
        # Charge information exchange
        self.charge_info = {"source_node": None, "charge": None}
        
        # Initialize logging
        self.logger = logging.getLogger(f"Node-{self.node_id}")
        
    def __str__(self) -> str:
        """String representation of the node."""
        roles = []
        if self.is_cluster_head:
            roles.append("Cluster Head")
        if self.is_central_node:
            roles.append("Central Node")
        if self.is_non_cluster_head:
            roles.append("Regular Node")
        
        role_str = ", ".join(roles) if roles else "Unassigned"
        return f"Node {self.node_id} ({role_str}) - Charge: {self.charge}"

    def set_as_cluster_head(self, initial_charge: int = 100) -> None:
        """
        Designate this node as a cluster head.
        
        Args:
            initial_charge (int): Initial energy charge for the cluster head.
        """
        self.is_cluster_head = True
        self.is_non_cluster_head = False
        self.set_charge(initial_charge)
        self.logger.info(f"Node {self.node_id} assigned as cluster head")

    def set_as_central_node(self, initial_charge: int = 100) -> None:
        """
        Designate this node as the central node.
        
        Args:
            initial_charge (int): Initial energy charge for the central node.
        """
        self.is_central_node = True
        self.is_non_cluster_head = False
        self.set_charge(initial_charge)
        self.logger.info(f"Node {self.node_id} assigned as central node")

    def set_as_non_cluster_head(self, initial_charge: int = 100) -> None:
        """
        Designate this node as a regular (non-cluster head) node.
        
        Args:
            initial_charge (int): Initial energy charge for the regular node.
        """
        self.is_non_cluster_head = True
        self.is_cluster_head = False
        self.set_charge(initial_charge)
        self.logger.info(f"Node {self.node_id} assigned as regular node")

    def set_charge(self, charge: int) -> None:
        """
        Set the energy charge for this node.
        
        Args:
            charge (int): New charge value.
        """
        old_charge = self.charge
        self.charge = max(0, charge)  # Ensure charge doesn't go below 0
        
        # Log energy consumption if charge decreased
        if charge < old_charge:
            energy_consumed = old_charge - charge
            self.energy_consumption_log.append({
                "timestamp": len(self.energy_consumption_log),
                "energy_consumed": energy_consumed,
                "remaining_charge": self.charge
            })
        
        # Warn if energy is critically low
        if self.charge <= 10:
            self.logger.warning(f"Node {self.node_id} has critically low energy: {self.charge}")
    
    def is_alive(self) -> bool:
        """Check if the node has enough energy to operate."""
        return self.charge > 0
    
    def add_monitor(self, monitor_node_id: str) -> None:
        """
        Add a node to monitor this node.
        
        Args:
            monitor_node_id (str): ID of the monitoring node.
        """
        if monitor_node_id not in self.monitored_by:
            self.monitored_by.append(monitor_node_id)
            self.logger.debug(f"Node {monitor_node_id} now monitoring Node {self.node_id}")
    
    def add_monitored_node(self, monitored_node_id: str) -> None:
        """
        Add a node for this node to monitor.
        
        Args:
            monitored_node_id (str): ID of the node to monitor.
        """
        if monitored_node_id not in self.monitors:
            self.monitors.append(monitored_node_id)
            self.logger.debug(f"Node {self.node_id} now monitoring Node {monitored_node_id}")
    
    def transmit_data(self, data: Dict[str, Any], energy_cost: int = 1) -> bool:
        """
        Transmit data and consume energy.
        
        Args:
            data (Dict[str, Any]): Data to transmit.
            energy_cost (int): Energy cost for transmission.
            
        Returns:
            bool: True if transmission successful, False if insufficient energy.
        """
        if self.charge < energy_cost:
            self.logger.warning(f"Node {self.node_id} insufficient energy for transmission")
            return False
        
        self.communication_log.append(data)
        self.set_charge(self.charge - energy_cost)
        self.logger.debug(f"Node {self.node_id} transmitted data, energy cost: {energy_cost}")
        return True

    def send_charge_info(self, destination_cluster_head: 'Node') -> bool:
        """
        Send charge information to the cluster head.

        Args:
            destination_cluster_head (Node): The cluster head to receive the charge information.
            
        Returns:
            bool: True if information sent successfully, False otherwise.
        """
        if not destination_cluster_head.is_cluster_head:
            self.logger.error(f"Cannot send charge info to non-cluster head {destination_cluster_head.node_id}")
            return False
        
        if not self.is_alive():
            self.logger.warning(f"Node {self.node_id} has no energy to send charge info")
            return False
        
        success = destination_cluster_head.receive_charge_info(self.charge, self.node_id)
        if success:
            self.logger.debug(f"Sent charge info to cluster head {destination_cluster_head.node_id}")
        return success

    def receive_charge_info(self, charge: int, source_node_id: str) -> bool:
        """
        Receive charge information from another node.

        Args:
            charge (int): The received charge information.
            source_node_id (str): The identifier of the source node.
            
        Returns:
            bool: True if information received successfully, False otherwise.
        """
        if not self.is_cluster_head:
            self.logger.error(f"Non-cluster head {self.node_id} cannot receive charge info")
            return False
        
        if not self.is_alive():
            self.logger.warning(f"Cluster head {self.node_id} has no energy to receive charge info")
            return False
        
        self.charge_info = {"source_node": source_node_id, "charge": charge}
        self.logger.debug(f"Received charge info from {source_node_id}: {charge}")
        return True

    def check_for_attack(self) -> Dict[str, Any]:
        """
        Check for attacks based on received charge information and node behavior.
        
        Returns:
            Dict[str, Any]: Attack detection results with status and details.
        """
        result = {
            "attack_detected": False,
            "attack_type": None,
            "details": "",
            "node_id": self.node_id
        }
        
        # Check for charge inconsistencies
        if self.charge_info["charge"] is not None and self.charge_info["source_node"]:
            source_charge = self.charge_info["charge"]
            
            # Simple anomaly detection: check for impossible charge values
            if source_charge < 0:
                result["attack_detected"] = True
                result["attack_type"] = "Invalid Charge"
                result["details"] = f"Node {self.charge_info['source_node']} reported negative charge: {source_charge}"
            elif source_charge > 1000:  # Assuming max charge is 1000
                result["attack_detected"] = True
                result["attack_type"] = "Suspicious High Charge"
                result["details"] = f"Node {self.charge_info['source_node']} reported unusually high charge: {source_charge}"
        
        # Check for communication anomalies
        if len(self.communication_log) > 100:  # Too many communications in short time
            result["attack_detected"] = True
            result["attack_type"] = "Communication Flood"
            result["details"] = f"Node {self.node_id} has excessive communication activity"
        
        if result["attack_detected"]:
            self.logger.warning(f"Attack detected on node {self.node_id}: {result['details']}")
        else:
            result["details"] = "No anomalies detected"
            
        return result
    
    def get_energy_stats(self) -> Dict[str, Any]:
        """
        Get energy consumption statistics for this node.
        
        Returns:
            Dict[str, Any]: Energy statistics including current charge and consumption history.
        """
        total_consumed = sum(log["energy_consumed"] for log in self.energy_consumption_log)
        
        return {
            "node_id": self.node_id,
            "current_charge": self.charge,
            "total_energy_consumed": total_consumed,
            "energy_efficiency": self.charge / (self.charge + total_consumed) if (self.charge + total_consumed) > 0 else 0,
            "is_alive": self.is_alive(),
            "consumption_events": len(self.energy_consumption_log)
        }
    
    def reset_communication_log(self) -> None:
        """Clear the communication log (typically after data is sent to central node)."""
        self.communication_log.clear()
        self.logger.debug(f"Communication log cleared for node {self.node_id}")
