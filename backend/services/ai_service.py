from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import logging
from google import genai
from ..core.config import settings
from ..models.workflow import WorkflowModel, WorkflowTrigger, WorkflowTriggerType, WorkflowAction, WorkflowCondition, WorkflowEdge, WorkflowStatus

logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_workflow_from_description(description: str, user_id: str) -> WorkflowModel:
    """
    Generate a workflow based on a natural language description using AI
    """
    try:
        # For the hackathon, we'll use a simple prompt to generate a workflow
        # In a production system, you'd want to use a more sophisticated approach
        
        prompt = f"""
        Create a workflow based on this description:
        "{description}"
        
        The workflow should include:
        1. A trigger (manual, scheduled, webhook, or event)
        2. A series of actions with their configurations
        3. Any conditions for branching logic
        4. How the actions are connected
        
        Return the result as a JSON object with the following structure:
        {{
            "name": "Workflow name",
            "description": "Workflow description",
            "trigger": {{
                "type": "manual|scheduled|webhook|event",
                "config": {{
                    // Trigger-specific configuration
                }}
            }},
            "actions": [
                {{
                    "name": "Action name",
                    "type": "action_type",
                    "config": {{
                        // Action-specific configuration
                    }},
                    "position": {{ "x": 100, "y": 100 }}
                }}
            ],
            "conditions": [
                {{
                    "name": "Condition name",
                    "condition": "condition expression",
                    "true_path": "next_node_id_if_true",
                    "false_path": "next_node_id_if_false",
                    "position": {{ "x": 300, "y": 100 }}
                }}
            ],
            "edges": [
                {{
                    "source": "source_node_id",
                    "target": "target_node_id"
                }}
            ]
        }}
        """
        
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"You are a workflow automation assistant. Your task is to design workflows based on natural language descriptions.\n\n{prompt}"
        
        response = await model.generate_content_async(full_prompt)
        
        # Parse the AI response
        ai_response = response.text
        
        # Extract JSON from the response
        import json
        import re
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            workflow_json = json.loads(json_match.group(0))
        else:
            # Fallback to a simple workflow if we can't parse the AI response
            workflow_json = {
                "name": f"Workflow from description",
                "description": description,
                "trigger": {"type": "manual", "config": {}},
                "actions": [
                    {
                        "name": "Default Action",
                        "type": "http_request",
                        "config": {"url": "https://example.com"},
                        "position": {"x": 100, "y": 100}
                    }
                ],
                "conditions": [],
                "edges": []
            }
        
        # Generate IDs for nodes
        action_ids = {}
        condition_ids = {}
        
        # Process actions
        actions = []
        for i, action_data in enumerate(workflow_json.get("actions", [])):
            action_id = str(uuid.uuid4())
            action_ids[i] = action_id
            actions.append(
                WorkflowAction(
                    id=action_id,
                    name=action_data.get("name", f"Action {i+1}"),
                    type=action_data.get("type", "http_request"),
                    config=action_data.get("config", {}),
                    position=action_data.get("position", {"x": 100 * (i+1), "y": 100})
                )
            )
        
        # Process conditions
        conditions = []
        for i, condition_data in enumerate(workflow_json.get("conditions", [])):
            condition_id = str(uuid.uuid4())
            condition_ids[i] = condition_id
            conditions.append(
                WorkflowCondition(
                    id=condition_id,
                    name=condition_data.get("name", f"Condition {i+1}"),
                    condition=condition_data.get("condition", "true"),
                    true_path=condition_data.get("true_path", ""),
                    false_path=condition_data.get("false_path", ""),
                    position=condition_data.get("position", {"x": 100 * (i+1), "y": 200})
                )
            )
        
        # Process trigger
        trigger_data = workflow_json.get("trigger", {"type": "manual", "config": {}})
        trigger = WorkflowTrigger(
            type=trigger_data.get("type", "manual"),
            config=trigger_data.get("config", {})
        )
        
        # Process edges
        edges = []
        for edge_data in workflow_json.get("edges", []):
            # For hackathon simplicity, we'll just connect all actions in sequence
            edge_id = str(uuid.uuid4())
            edges.append(
                WorkflowEdge(
                    id=edge_id,
                    source=edge_data.get("source", ""),
                    target=edge_data.get("target", "")
                )
            )
        
        # If no edges and multiple actions, create sequential edges
        if not edges and len(actions) > 1:
            for i in range(len(actions) - 1):
                edge_id = str(uuid.uuid4())
                edges.append(
                    WorkflowEdge(
                        id=edge_id,
                        source=actions[i].id,
                        target=actions[i+1].id
                    )
                )
        
        # Create workflow model
        workflow = WorkflowModel(
            id=str(uuid.uuid4()),
            name=workflow_json.get("name", "Generated Workflow"),
            description=workflow_json.get("description", description),
            status=WorkflowStatus.DRAFT,
            trigger=trigger,
            actions=actions,
            conditions=conditions,
            edges=edges,
            created_by=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return workflow
        
    except Exception as e:
        logger.error(f"Error generating workflow: {str(e)}")
        # Return a simple fallback workflow
        return WorkflowModel(
            id=str(uuid.uuid4()),
            name="Simple Workflow",
            description=description,
            status=WorkflowStatus.DRAFT,
            trigger=WorkflowTrigger(type=WorkflowTriggerType.MANUAL, config={}),
            actions=[
                WorkflowAction(
                    id=str(uuid.uuid4()),
                    name="Default Action",
                    type="http_request",
                    config={"url": "https://example.com"},
                    position={"x": 100, "y": 100}
                )
            ],
            conditions=[],
            edges=[],
            created_by=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )