from ..models.workflow import WorkflowModel, WorkflowExecution
from ..database.mongodb import (
    create_workflow,
    get_workflow,
    get_workflows_by_user,
    update_workflow,
    delete_workflow,
    create_execution,
    get_execution,
    get_executions_by_workflow,
    update_execution
)
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional
import uuid

logger = logging.getLogger(__name__)

async def create_new_workflow(workflow: WorkflowModel) -> WorkflowModel:
    """
    Create a new workflow in the database
    """
    workflow_dict = workflow.dict()
    workflow_id = await create_workflow(workflow_dict)
    return workflow

async def get_workflow_by_id(workflow_id: str) -> Optional[WorkflowModel]:
    """
    Get a workflow by its ID
    """
    workflow_dict = await get_workflow(workflow_id)
    if not workflow_dict:
        return None
    return WorkflowModel(**workflow_dict)

async def get_user_workflows(user_id: str, skip: int = 0, limit: int = 100) -> List[WorkflowModel]:
    """
    Get all workflows created by a specific user
    """
    workflows_dict = await get_workflows_by_user(user_id, skip, limit)
    return [WorkflowModel(**workflow) for workflow in workflows_dict]

async def update_existing_workflow(workflow_id: str, workflow: WorkflowModel) -> Optional[WorkflowModel]:
    """
    Update an existing workflow
    """
    workflow_dict = workflow.dict()
    success = await update_workflow(workflow_id, workflow_dict)
    if not success:
        return None
    return workflow

async def delete_workflow_by_id(workflow_id: str) -> bool:
    """
    Delete a workflow by its ID
    """
    return await delete_workflow(workflow_id)

async def execute_workflow(workflow_id: str, input_data: Dict[str, Any]) -> WorkflowExecution:
    """
    Execute a workflow with the given input data
    """
    workflow_dict = await get_workflow(workflow_id)
    if not workflow_dict:
        raise ValueError(f"Workflow with ID {workflow_id} not found")
    
    workflow = WorkflowModel(**workflow_dict)
    
    # Create execution record
    execution_id = str(uuid.uuid4())
    execution = WorkflowExecution(
        id=execution_id,
        workflow_id=workflow_id,
        status="running",
        started_at=datetime.now(),
        input_data=input_data,
        output_data={},
        logs=[{"timestamp": datetime.now().isoformat(), "message": "Execution started"}]
    )
    
    await create_execution(execution.dict())
    
    try:
        # Process workflow nodes
        output_data = await process_workflow(workflow, input_data)
        
        # Update execution record
        execution.status = "completed"
        execution.completed_at = datetime.now()
        execution.output_data = output_data
        execution.logs.append({"timestamp": datetime.now().isoformat(), "message": "Execution completed successfully"})
        
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
        execution.status = "failed"
        execution.completed_at = datetime.now()
        execution.logs.append({"timestamp": datetime.now().isoformat(), "message": f"Execution failed: {str(e)}"})
    
    # Update execution in database
    await update_execution(execution_id, execution.dict())
    
    return execution

async def process_workflow(workflow: WorkflowModel, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a workflow by executing its actions in order
    """
    # In a real implementation, this would navigate the workflow graph
    # For the hackathon, we'll implement a simplified version
    
    context = {**input_data}  # Start with input data
    
    # Find the first action (no incoming edges)
    action_map = {action.id: action for action in workflow.actions}
    condition_map = {condition.id: condition for condition in workflow.conditions}
    
    # Create a map of incoming edges
    incoming_edges = {}
    for edge in workflow.edges:
        if edge.target not in incoming_edges:
            incoming_edges[edge.target] = []
        incoming_edges[edge.target].append(edge.source)
    
    # Find nodes with no incoming edges (start nodes)
    start_nodes = []
    for action in workflow.actions:
        if action.id not in incoming_edges:
            start_nodes.append(action.id)
    
    # Simple execution for hackathon - just execute actions in sequence
    for action in workflow.actions:
        action_result = await execute_action(action.type, action.config, context)
        context.update(action_result)
    
    return context

async def execute_action(action_type: str, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a single action based on its type
    """
    # This is where you'd implement different action types
    # For the hackathon, we'll simulate a few basic actions
    
    if action_type == "extract_text":
        # Simulate text extraction
        return {"extracted_text": "Sample extracted text"}
    
    elif action_type == "classify_document":
        # Simulate document classification
        return {"document_type": "invoice", "confidence": 0.95}
    
    elif action_type == "send_email":
        # Simulate sending email
        return {"email_sent": True, "timestamp": datetime.now().isoformat()}
    
    elif action_type == "http_request":
        # Simulate HTTP request
        return {"response": {"status": 200, "body": "Success"}}
    
    else:
        # Unknown action type
        raise ValueError(f"Unknown action type: {action_type}")

async def get_workflow_execution(execution_id: str) -> Optional[WorkflowExecution]:
    """
    Get a workflow execution by its ID
    """
    execution_dict = await get_execution(execution_id)
    if not execution_dict:
        return None
    return WorkflowExecution(**execution_dict)

async def get_workflow_executions(workflow_id: str, skip: int = 0, limit: int = 20) -> List[WorkflowExecution]:
    """
    Get all executions for a specific workflow
    """
    executions_dict = await get_executions_by_workflow(workflow_id, skip, limit)
    return [WorkflowExecution(**execution) for execution in executions_dict]