
from fastapi import FastAPI, Depends
from my_service.dependencies import get_token
from my_service.utils.logger import setup_logger
from my_service.config.config import settings
from my_service.models.models import ApplicationStatusResponse, ProjectListResponse
from fastapi import APIRouter, HTTPException
from typing import List, Dict
import requests


router = APIRouter(
    prefix="/argocd",
    tags=["argocd"],
)


logger = setup_logger()


app = FastAPI()



@router.get("/application_status", response_model=ApplicationStatusResponse)
async def application_status(token: str = Depends(get_token)):
    """Fetches all ArgoCD applications statuses

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).

    Returns:
        applications_data_concise: concise application metadata json structure
    """
    try:
        logger.info("Getting ArgoCD applications statuses")
        
        response = requests.get(
            f"https://{settings.ARGOCD_SERVER}/api/v1/applications",
            headers={"Authorization": f"Bearer {token}"},
            verify=False
        )

        response.raise_for_status()

        applications = response.json().get("items") or []

        return {
                "applications": [
                    {
                        "application_name": app["metadata"]["name"],
                        "status": app["status"]["sync"]["status"]
                    } for app in applications
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications and statuses: {str(e)}")




@router.get("/list_projects", response_model=ProjectListResponse)
async def list_projects(token: str = Depends(get_token)):
    """Fetches all argocd projects names and namespaces to which they are configured

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).
    Returns:
        projects_data_concise: concise argocd projects metadata json structure
    """
    try: 
        logger.info("Getting ArgoCD projects list")

        response = requests.get(
            f"https://{settings.ARGOCD_SERVER}/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            verify=False
        )
        response.raise_for_status()

        projects = response.json().get("items") or []

        return {
                "projects": [
                    {
                        "project_name": project["metadata"]["name"],
                        "namespace": "argocd"
                    } for project in projects
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")