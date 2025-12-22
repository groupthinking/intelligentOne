"""
Process Manager - Manages web service lifecycle as OS processes
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ProcessState(Enum):
    """Process lifecycle states"""
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "terminated"


@dataclass
class Process:
    """Represents a web capability as an OS process"""
    pid: int
    capability_name: str
    state: ProcessState
    params: Dict[str, Any]
    result: Any = None
    error: Any = None


class ProcessManager:
    """
    Manages web capabilities as OS processes
    
    Treats each capability execution as a process with:
    - Process ID (PID)
    - State management
    - Resource allocation
    - Lifecycle management
    """
    
    def __init__(self):
        self.processes: Dict[int, Process] = {}
        self.next_pid = 1000
        
    def spawn(self, capability_name: str, params: Dict[str, Any]) -> int:
        """
        Spawn a new process for capability execution
        
        Args:
            capability_name: Name of capability to execute
            params: Parameters for the capability
            
        Returns:
            Process ID (PID)
        """
        pid = self._allocate_pid()
        
        process = Process(
            pid=pid,
            capability_name=capability_name,
            state=ProcessState.READY,
            params=params
        )
        
        self.processes[pid] = process
        return pid
    
    def start(self, pid: int):
        """Start a process"""
        if pid not in self.processes:
            raise ValueError(f"Process {pid} not found")
        
        self.processes[pid].state = ProcessState.RUNNING
    
    def wait(self, pid: int):
        """Wait for process to complete"""
        if pid not in self.processes:
            raise ValueError(f"Process {pid} not found")
        
        self.processes[pid].state = ProcessState.WAITING
    
    def terminate(self, pid: int):
        """Terminate a process"""
        if pid not in self.processes:
            raise ValueError(f"Process {pid} not found")
        
        self.processes[pid].state = ProcessState.TERMINATED
    
    def get_process(self, pid: int) -> Process:
        """Get process by PID"""
        return self.processes.get(pid)
    
    def list_processes(self) -> List[Process]:
        """List all processes"""
        return list(self.processes.values())
    
    def kill(self, pid: int):
        """Kill a process and remove it"""
        if pid in self.processes:
            del self.processes[pid]
    
    def _allocate_pid(self) -> int:
        """Allocate a new process ID"""
        pid = self.next_pid
        self.next_pid += 1
        return pid
