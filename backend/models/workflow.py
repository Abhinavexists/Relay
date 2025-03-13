from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid

class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

class WorkflowTriggerType(str, Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT = "event"
    WEBHOOK = "webhook"

class WorkflowAction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str
    config: Dict[str, Any]
    position: Dict[str, int] = {"x": 0, "y": 0}

class WorkflowCondition(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    condition: str
    true_path: str
    false_path: str
    position: Dict[str, int] = {"x": 0, "y": 0}

class WorkflowTrigger(BaseModel):
    type: WorkflowTriggerType
    config: Dict[str, Any]

class WorkflowEdge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    target: str
    label: Optional[str] = None

class WorkflowModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    status: WorkflowStatus = WorkflowStatus.DRAFT
    trigger: WorkflowTrigger
    actions: List[WorkflowAction] = []
    conditions: List[WorkflowCondition] = []
    edges: List[WorkflowEdge] = []
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Document Processing Workflow",
                "description": "Automatically process incoming documents",
                "status": "active",
                "trigger": {
                    "type": "webhook",
                    "config": {
                        "path": "/incoming-document"
                    }
                },
                "actions": [
                    {
                        "name": "Extract Text",
                        "type": "extract_text",
                        "config": {
                            "output_var": "document_text"
                        },
                        "position": {"x": 100, "y": 100}
                    }
                ],
                "conditions": [],
                "edges": [],
                "created_by": "user123"
            }
        }

class WorkflowExecution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    status: str
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    input_data: Dict[str, Any] = {}
    output_data: Dict[str, Any] = {}
    logs: List[Dict[str, Any]] = []
    
    class Config:
        schema_extra = {
            "example": {
                "workflow_id": "12345",
                "status": "completed",
                "started_at": "2023-01-01T12:00:00",
                "completed_at": "2023-01-01T12:01:00",
                "input_data": {"document_url": "https://example.com/doc.pdf"},
                "output_data": {"extracted_text": "Sample text..."},
                "logs": [
                    {"timestamp": "2023-01-01T12:00:30", "action": "extract_text", "message": "Processing completed"}
                ]
            }
        }