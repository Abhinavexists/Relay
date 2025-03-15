from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from datetime import datetime
from backend.models.workflow import WorkflowModel, WorkflowExecution
from ..services.workflow_service import (
    create_new_workflow,
    get_workflow_by_id,
    get_user_workflows,
    update_existing_workflow,
    delete_workflow_by_id,
    execute_workflow,
    get_workflow_execution,
    get_workflow_executions
)
from ..services.ai_service import generate_workflow_from_description
from .user import get_current_user
from ..models.user import UserModel

router = APIRouter()

@router.post("/", response_model=WorkflowModel, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow: WorkflowModel,
    current_user: UserModel = Depends(get_current_user)
):
    workflow.created_by = current_user.id
    workflow.created_at = datetime.now()
    workflow.updated_at = datetime.now()
    created_workflow = await create_new_workflow(workflow)
    return created_workflow

@router.post("/generate", response_model=WorkflowModel, status_code=status.HTTP_201_CREATED)
async def generate_workflow(
    description: str = Body(..., embed=True),
    current_user: UserModel = Depends(get_current_user)
):
    workflow = await generate_workflow_from_description(description, current_user.id)
    return workflow

@router.get("/", response_model=List[WorkflowModel])
async def get_workflows(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user)
):
    workflows = await get_user_workflows(current_user.id, skip, limit)
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowModel)
async def get_workflow(
    workflow_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    workflow = await get_workflow_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this workflow")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowModel)
async def update_workflow(
    workflow_id: str,
    workflow_data: WorkflowModel,
    current_user: UserModel = Depends(get_current_user)
):
    existing_workflow = await get_workflow_by_id(workflow_id)
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if existing_workflow.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this workflow")
    
    workflow_data.updated_at = datetime.now()
    updated_workflow = await update_existing_workflow(workflow_id, workflow_data)
    return updated_workflow

@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    existing_workflow = await get_workflow_by_id(workflow_id)
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if existing_workflow.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this workflow")
    
    deleted = await delete_workflow_by_id(workflow_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete workflow")
    return None

@router.post("/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow_endpoint(
    workflow_id: str,
    input_data: dict = Body(...),
    current_user: UserModel = Depends(get_current_user)
):
    workflow = await get_workflow_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    execution_result = await execute_workflow(workflow_id, input_data)
    return execution_result

@router.get("/{workflow_id}/executions", response_model=List[WorkflowExecution])
async def get_workflow_executions_endpoint(
    workflow_id: str,
    skip: int = 0,
    limit: int = 20,
    current_user: UserModel = Depends(get_current_user)
):
    workflow = await get_workflow_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this workflow")
    
    executions = await get_workflow_executions(workflow_id, skip, limit)
    return executions

@router.get("/{workflow_id}/executions/{execution_id}", response_model=WorkflowExecution)
async def get_execution_endpoint(
    workflow_id: str,
    execution_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    workflow = await get_workflow_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this workflow")
    
    execution = await get_workflow_execution(execution_id)
    if not execution or execution.workflow_id != workflow_id:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@router.post("/webhook/{webhook_id}")
async def webhook_trigger(
    webhook_id: str,
    payload: dict = Body(...)
):
    # Find workflow with this webhook ID
    # Execute workflow with the payload
    # Return minimal response to avoid information leakage
    return {"status": "received"}