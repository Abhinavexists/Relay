from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from ...services.workflow_service import execute_workflow, get_workflow_execution, get_workflow_executions
from ...models.workflow import WorkflowExecution
from ..deps import get_current_user
from ...models.user import UserModel

router = APIRouter()

@router.post("/{workflow_id}", response_model=WorkflowExecution)
async def trigger_workflow(
    workflow_id: str,
    input_data: Dict[str, Any] = {},
    current_user: UserModel = Depends(get_current_user)
):
    """
    Trigger a workflow execution
    """
    try:
        execution = await execute_workflow(workflow_id, input_data)
        return execution
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{execution_id}", response_model=WorkflowExecution)
async def get_execution_status(
    execution_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get the status of a workflow execution
    """
    execution = await get_workflow_execution(execution_id)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    return execution

@router.get("/workflow/{workflow_id}", response_model=List[WorkflowExecution])
async def list_workflow_executions(
    workflow_id: str,
    skip: int = 0,
    limit: int = 20,
    current_user: UserModel = Depends(get_current_user)
):
    """
    List executions for a specific workflow
    """
    return await get_workflow_executions(workflow_id, skip, limit)
