"""
Memory management for GHC Travel Planner.
Stores and retrieves user preferences across agent interactions.
"""
from typing import Dict, Any, Optional
from datetime import datetime

class TravelMemory:
    """
    Simple in-memory storage for user travel preferences.
    In production, this could be replaced with a database or persistent storage.
    """
    
    def __init__(self):
        self._memory: Dict[str, Any] = {}
        self._created_at = datetime.now()
    
    def store_preference(self, key: str, value: Any) -> None:
        """
        Store a user preference.
        
        Args:
            key: Preference key (e.g., 'travel_dates', 'flight_preference', 'budget')
            value: Preference value
        """
        self._memory[key] = value
        print(f"[MEMORY] Stored: {key} = {value}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a user preference.
        
        Args:
            key: Preference key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
        value = self._memory.get(key, default)
        print(f"[MEMORY] Retrieved: {key} = {value}")
        return value
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """
        Get all stored preferences.
        
        Returns:
            Dictionary of all preferences
        """
        return self._memory.copy()
    
    def clear(self) -> None:
        """Clear all stored preferences."""
        self._memory.clear()
        print("[MEMORY] Cleared all preferences")
    
    def to_context_string(self) -> str:
        """
        Convert memory to a context string for agents.
        
        Returns:
            Formatted string of user preferences
        """
        if not self._memory:
            return "No previous preferences stored."
        
        context_parts = ["User Preferences:"]
        for key, value in self._memory.items():
            context_parts.append(f"- {key}: {value}")
        
        return "\n".join(context_parts)


# Global memory instance (shared across agents in a session)
_travel_memory = TravelMemory()

def get_memory() -> TravelMemory:
    """Get the global travel memory instance."""
    return _travel_memory

def reset_memory() -> None:
    """Reset the global travel memory."""
    global _travel_memory
    _travel_memory = TravelMemory()
