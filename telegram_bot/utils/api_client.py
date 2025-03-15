import httpx
import logging
from typing import List, Dict, Any, Optional
from ..config import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = f"http://{settings.API_HOST}:{settings.API_PORT}"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def get_user_workflows(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all workflows for a user."""
        response = await self.client.get(f"{self.base_url}/api/workflows", params={"user_id": user_id})
        response.raise_for_status()
        return response.json()

    async def create_workflow(self, user_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow for a user."""
        response = await self.client.post(
            f"{self.base_url}/api/workflows",
            json={"user_id": user_id, **workflow_data}
        )
        response.raise_for_status()
        return response.json()

    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID."""
        response = await self.client.get(f"{self.base_url}/api/workflows/{workflow_id}")
        response.raise_for_status()
        return response.json()

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow."""
        response = await self.client.post(f"{self.base_url}/api/workflows/{workflow_id}/execute")
        response.raise_for_status()
        return response.json()

    async def delete_workflow(self, workflow_id: str) -> None:
        """Delete a workflow."""
        response = await self.client.delete(f"{self.base_url}/api/workflows/{workflow_id}")
        response.raise_for_status()

    async def get_workflow_details(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific workflow.
        
        Args:
            workflow_id (str): The ID of the workflow to get details for
            
        Returns:
            Dict[str, Any]: Detailed workflow information
        """
        try:
            # For now, return mock data
            return {
                "id": workflow_id,
                "name": "Sample Workflow",
                "type": "email",
                "status": "active",
                "created_at": "2024-03-15T10:00:00Z",
                "last_executed": "2024-03-15T12:00:00Z",
                "execution_count": 5,
                "description": "This workflow handles email automation",
                "triggers": ["schedule", "manual"],
                "actions": ["send_email", "notify"],
                "settings": {
                    "schedule": "daily",
                    "recipients": ["user@example.com"]
                }
            }
        except Exception as e:
            logger.error(f"Error getting workflow details: {e}")
            raise

# Create a singleton instance
api_client = APIClient()

# Export functions for easy access
async def get_user_workflows(user_id: str) -> List[Dict[str, Any]]:
    return await api_client.get_user_workflows(user_id)

async def create_workflow(user_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    return await api_client.create_workflow(user_id, workflow_data)

async def get_workflow(workflow_id: str) -> Dict[str, Any]:
    return await api_client.get_workflow(workflow_id)

async def get_workflow_details(workflow_id: str) -> Dict[str, Any]:
    return await api_client.get_workflow_details(workflow_id)

async def execute_workflow(workflow_id: str) -> Dict[str, Any]:
    return await api_client.execute_workflow(workflow_id)

async def delete_workflow(workflow_id: str) -> None:
    await api_client.delete_workflow(workflow_id)

async def analyze_user_request(user_id: str, message: str) -> Dict[str, Any]:
    """
    Analyze user message and determine appropriate workflow action.
    
    Args:
        user_id (str): The ID of the user making the request
        message (str): The message content to analyze
        
    Returns:
        Dict[str, Any]: Analysis results including intent and extracted parameters
    """
    try:
        # TODO: Implement actual API call to your backend
        # For now, return a mock response
        return {
            "intent": "create_workflow",
            "confidence": 0.9,
            "parameters": {
                "workflow_type": "email",
                "trigger": "schedule",
                "action": "send_email"
            },
            "message": "I understand you want to create an email workflow."
        }
    except Exception as e:
        logger.error(f"Error analyzing user request: {e}")
        return {
            "intent": "unknown",
            "confidence": 0,
            "error": str(e)
        }

async def execute_workflow(workflow_id: str, input_data: Optional[Dict] = None) -> Dict:
    """Execute a specific workflow."""
    # TODO: Implement actual API call
    return {"status": "success", "message": "Workflow executed successfully"}
