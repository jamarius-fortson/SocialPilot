from fastapi import FastAPI, HTTPException, BackgroundTasks, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional
import uuid
import logging

from app.schemas.state import BrandProfile, SocialState
from app.graphs.orchestrator import create_social_pilot_graph

# Setup advanced logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("OmniViral")

app = FastAPI(
    title="OmniViral AI: Autonomous Social Media API",
    description="Enterprise-grade autonomous system for social media marketing orchestration.",
    version="2.0.0"
)

# Advanced Security Implementation
API_KEY_NAME = "X-OmniViral-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In a real FAANG application, this would use a secure Key Management Service
SECRET_API_KEY = "ov_live_sk_example_123" # Example static key for demo purposes

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return api_key_header

# In-memory stores (in production, use Redis/PostgreSQL)
BRAND_DB = {}
PENDING_APPROVALS = {}
TASKS_STATUS = {}

class CampaignRequest(BaseModel):
    client_id: str
    task_type: str = "campaign"

def run_graph_background(initial_values: dict, task_id: str):
    logger.info(f"Starting background graph execution for task {task_id}")
    try:
        graph = create_social_pilot_graph()
        result = graph.invoke(initial_values)
        
        if result.get("requires_human_approval"):
            approval_id = str(uuid.uuid4())
            PENDING_APPROVALS[approval_id] = result
            TASKS_STATUS[task_id] = {
                "status": "awaiting_approval",
                "approval_id": approval_id,
                "reason": result.get("escalation_reason")
            }
            logger.warning(f"Task {task_id} paused awaiting human approval")
        else:
            TASKS_STATUS[task_id] = {"status": "completed", "result": result}
            logger.info(f"Task {task_id} completed successfully")
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}")
        TASKS_STATUS[task_id] = {"status": "failed", "error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "online", "system": "OmniViral AI", "version": "2.0.0"}

@app.post("/client/profile", dependencies=[Depends(get_api_key)])
async def create_profile(profile: BrandProfile, client_id: str):
    BRAND_DB[client_id] = profile
    logger.info(f"Created/Updated profile for client: {client_id}")
    return {"message": "Profile created successfully", "client_id": client_id}

@app.post("/run", dependencies=[Depends(get_api_key)])
async def run_automation(request: CampaignRequest, background_tasks: BackgroundTasks):
    if request.client_id not in BRAND_DB:
        raise HTTPException(status_code=404, detail="Client profile not found. Please sync profile first.")
    
    brand = BRAND_DB[request.client_id]
    
    initial_values = {
        "client_id": request.client_id,
        "brand_profile": brand,
        "task_type": request.task_type,
        "messages": [],
        "requires_human_approval": False
    }
    
    task_id = str(uuid.uuid4())
    TASKS_STATUS[task_id] = {"status": "processing"}
    
    # Delegating to a BackgroundTask for non-blocking I/O
    background_tasks.add_task(run_graph_background, initial_values, task_id)
    logger.info(f"Enqueued automation for client {request.client_id} with task ID: {task_id}")
    
    return {"status": "processing", "task_id": task_id, "message": "Automation cycle triggered globally."}

@app.get("/task/{task_id}", dependencies=[Depends(get_api_key)])
async def get_task_status(task_id: str):
    if task_id not in TASKS_STATUS:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS_STATUS[task_id]

@app.post("/approve/{approval_id}", dependencies=[Depends(get_api_key)])
async def approve_content(approval_id: str, background_tasks: BackgroundTasks):
    if approval_id not in PENDING_APPROVALS:
        raise HTTPException(status_code=404, detail="Approval request not found")
        
    state = PENDING_APPROVALS.pop(approval_id)
    state["requires_human_approval"] = False
    state["task_type"] = "scheduling" # Set task to scheduling to skip previous steps
    
    task_id = str(uuid.uuid4())
    TASKS_STATUS[task_id] = {"status": "processing approval"}
    background_tasks.add_task(run_graph_background, state, task_id)
    
    logger.info(f"Human intervention completed: Content approved for {approval_id}")
    return {"message": "Content approved and processing resumed", "task_id": task_id}

@app.post("/reject/{approval_id}", dependencies=[Depends(get_api_key)])
async def reject_content(approval_id: str, feedback: str = "Rejected by human operations constraint"):
    if approval_id not in PENDING_APPROVALS:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    PENDING_APPROVALS.pop(approval_id)
    logger.info(f"Content rejected for approval id {approval_id}. Feedback: {feedback}")
    return {"message": "Content rejected", "feedback": feedback}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
