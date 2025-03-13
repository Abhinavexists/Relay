import httpx
from typing import List, Dict, Any, Optional
from ..config import settings

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

# Create a singleton instance
api_client = APIClient()

# Export functions for easy access
async def get_user_workflows(user_id: str) -> List[Dict[str, Any]]:
    return await api_client.get_user_workflows(user_id)

async def create_workflow(user_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    return await api_client.create_workflow(user_id, workflow_data)

async def get_workflow(workflow_id: str) -> Dict[str, Any]:
    return await api_client.get_workflow(workflow_id)

async def execute_workflow(workflow_id: str) -> Dict[str, Any]:
    return await api_client.execute_workflow(workflow_id)

async def delete_workflow(workflow_id: str) -> None:
    await api_client.delete_workflow(workflow_id)
