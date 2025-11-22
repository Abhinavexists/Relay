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
from .tool_service import tool_service

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
        output_data = await process_workflow(workflow, input_data, execution)
        
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

async def process_workflow(workflow: WorkflowModel, input_data: Dict[str, Any], execution: WorkflowExecution) -> Dict[str, Any]:
    """
    Process a workflow by executing its actions in topological order
    """
    context = {**input_data}  # Start with input data
    
    # Build graph
    adj_list = {}
    in_degree = {}
    action_map = {action.id: action for action in workflow.actions}
    
    # Initialize in-degree for all actions
    for action in workflow.actions:
        in_degree[action.id] = 0
        adj_list[action.id] = []
        
    # Build adjacency list and calculate in-degrees
    for edge in workflow.edges:
        if edge.source in action_map and edge.target in action_map:
            adj_list[edge.source].append(edge.target)
            in_degree[edge.target] += 1
            
    # Find start nodes (in-degree 0)
    queue = [action_id for action_id, degree in in_degree.items() if degree == 0]
    
    execution_order = []
    
    while queue:
        current_id = queue.pop(0)
        execution_order.append(current_id)
        
        for neighbor in adj_list[current_id]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(execution_order) != len(workflow.actions):
        raise ValueError("Cycle detected in workflow graph")
        
    # Execute actions in order
    for action_id in execution_order:
        action = action_map[action_id]
        execution.logs.append({"timestamp": datetime.now().isoformat(), "message": f"Executing action: {action.name} ({action.type})"})
        
        try:
            action_result = await execute_action(action.type, action.config, context)
            context.update(action_result)
            execution.logs.append({"timestamp": datetime.now().isoformat(), "message": f"Action {action.name} completed"})
        except Exception as e:
            execution.logs.append({"timestamp": datetime.now().isoformat(), "message": f"Action {action.name} failed: {str(e)}"})
            raise e
            
    return context

async def execute_action(action_type: str, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a single action based on its type using ToolService
    """
    if action_type == "http_request":
        return await tool_service.execute_http_request(config, context)
    
    elif action_type == "data_transformation":
        return await tool_service.execute_data_transformation(config, context)
    
    elif action_type == "send_email":
        return await tool_service.send_email(config, context)
    
    elif action_type in ["summarize", "extract", "classify", "generate", "ai_task"]:
        # Map generic ai_task or specific types to execute_ai_task
        if action_type != "ai_task":
            config["task_type"] = action_type
        return await tool_service.execute_ai_task(config, context)
    
    else:
        # Fallback for unknown types or simulation
        logger.warning(f"Unknown action type: {action_type}, returning empty result")
        return {}

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