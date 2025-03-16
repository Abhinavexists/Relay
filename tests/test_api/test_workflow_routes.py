"""
Tests for workflow API routes.
"""

import pytest
from fastapi import status

def test_create_workflow(test_app, mock_db):
    """
    Test workflow creation endpoint.
    """
    response = test_app.post(
        "/api/workflows/",
        json={
            "name": "Test Workflow",
            "description": "A test workflow",
            "steps": [
                {
                    "type": "email",
                    "config": {
                        "to": "test@example.com",
                        "subject": "Test",
                        "body": "Test email"
                    }
                }
            ]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Workflow"
    assert "id" in data

def test_list_workflows(test_app, mock_db):
    """
    Test workflow listing endpoint.
    """
    response = test_app.get("/api/workflows/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_workflow(test_app, mock_db):
    """
    Test getting a specific workflow.
    """
    # First create a workflow
    create_response = test_app.post(
        "/api/workflows/",
        json={
            "name": "Test Workflow",
            "description": "A test workflow",
            "steps": []
        }
    )
    workflow_id = create_response.json()["id"]

    # Then get it
    response = test_app.get(f"/api/workflows/{workflow_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == workflow_id 