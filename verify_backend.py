import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_backend():
    # 1. Login
    print("Testing Login...")
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/users/login", data=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.status_code} - {response.text}")
            # Try registering if login fails
            print("Attempting registration...")
            register_data = {
                "email": "test@example.com",
                "password": "password123",
                "full_name": "Test User"
            }
            reg_response = requests.post(f"{BASE_URL}/users/register", json=register_data)
            if reg_response.status_code not in [200, 201]:
                 print(f"Registration failed: {reg_response.status_code} - {reg_response.text}")
                 return
            
            # Retry login
            response = requests.post(f"{BASE_URL}/users/login", data=login_data)
            if response.status_code != 200:
                print(f"Login failed after registration: {response.status_code} - {response.text}")
                return

        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"Login successful. Token: {access_token[:10]}...")
        
        headers = {"Authorization": f"Bearer {access_token}"}

        # 2. Get Me
        print("\nTesting /users/me...")
        me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if me_response.status_code == 200:
            print(f"User info: {me_response.json()}")
        else:
            print(f"Get Me failed: {me_response.status_code} - {me_response.text}")

        # 3. Generate Workflow
        print("\nTesting AI Workflow Generation...")
        workflow_desc = "Create a workflow that sends an email when a new user signs up."
        gen_response = requests.post(
            f"{BASE_URL}/workflows/generate", 
            headers=headers,
            json={"description": workflow_desc}
        )
        if gen_response.status_code in [200, 201]:
            print("Workflow generation successful!")
            workflow_data = gen_response.json()
            print(workflow_data)
            workflow_id = workflow_data["id"]
            
            # 4. Execute Workflow
            print("\nTesting Workflow Execution...")
            exec_response = requests.post(
                f"{BASE_URL}/execute/{workflow_id}",
                headers=headers,
                json={"input": "test data"}
            )
            if exec_response.status_code == 200:
                print("Workflow execution triggered successfully!")
                print(exec_response.json())
            else:
                print(f"Workflow execution failed: {exec_response.status_code} - {exec_response.text}")
        else:
            print(f"Workflow generation failed: {gen_response.status_code} - {gen_response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_backend()
