from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import logging
from google import genai
from ..core.config import settings
from ..models.workflow import WorkflowModel, WorkflowTrigger, WorkflowTriggerType, WorkflowAction, WorkflowCondition, WorkflowEdge, WorkflowStatus

logger = logging.getLogger(__name__)

# Initialize Gemini Client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def generate_workflow_from_description(description: str, user_id: str) -> WorkflowModel:
    """
    Generate a workflow based on a natural language description using AI
    """
    try:
        # For the hackathon, we'll use a simple prompt to generate a workflow
        # In a production system, you'd want to use a more sophisticated approach
        
        prompt = f"""
        Based on the following description, design a workflow:
        "{description}"
        
        **IMPORTANT INSTRUCTIONS**:
        1. Extract any text, data, or content mentioned in the description
        2. If the user provides text to process (e.g., "Summarize this text: ..."), extract that text and put it in the action's config
        3. Use ONLY these action types:
           - "summarize" - for text summarization tasks
           - "extract" - for extracting information from text
           - "classify" - for classification tasks  
           - "generate" - for content generation
           - "http_request" - for making HTTP API calls (use real, working APIs only)
           - "send_email" - for sending emails
           - "data_transformation" - for transforming data
        
        4. For AI tasks (summarize, extract, classify, generate), the config MUST include:
           - "text": the actual text to process (extract this from the user's description)
           - "task_type": the type of task (optional, will be inferred from action type)
        
        5. For http_request, use ONLY real, working public APIs like:
           - https://official-joke-api.appspot.com/random_joke
           - https://api.github.com/users/github
           - https://jsonplaceholder.typicode.com/posts/1
        
        Return the result as a JSON object with the following structure:
        {{
            "name": "Workflow name",
            "description": "Workflow description",
            "trigger": {{
                "type": "manual",
                "config": {{}}
            }},
            "actions": [
                {{
                    "name": "Action name",
                    "type": "summarize|extract|classify|generate|http_request|send_email|data_transformation",
                    "config": {{
                        "text": "THE ACTUAL TEXT FROM USER'S DESCRIPTION (for AI tasks)",
                        "url": "REAL WORKING API URL (for http_request)",
                        "method": "GET or POST (for http_request)",
                        "to": "recipient (for send_email)",
                        "subject": "email subject (for send_email)",
                        "body": "email body (for send_email)"
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
        
        full_prompt = f"You are a workflow automation assistant. Your task is to design workflows based on natural language descriptions.\n\n{prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
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