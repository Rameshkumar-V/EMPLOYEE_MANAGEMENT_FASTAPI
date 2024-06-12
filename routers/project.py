from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session



# database
from databases.database import *

# model
from models import *

#schema
from schemas import *

#security
from security import VerifyRoute



project_router = APIRouter(
    prefix="/api",
    tags=["Project"],
    route_class=VerifyRoute
)

@project_router.delete("/project/{project_id}")
def delete_project(project_id : int,db : Session = Depends(get_db)):
    # Delete Project
    
    try:
        project = db.query(m_project.Project).filter(m_project.Project.id == project_id).first()
        
        if project:
            project.delete()
            project.commit()
            
            return {
                'status' : 'success',
                'msg' :'Successfully Deleted',
                'data': project
            }
        else:
            return {
                'status' : 'failed',
                'msg': 'project Not Found'
            }
    except Exception as e:
        return {
            'status' : 'Error',
            'error' : f'{e}'
        }


@project_router.get("/project")
def show_projects(db : Session = Depends(get_db)):
    
    
    try:
        projects = db.query(m_project.Project).all()
        
        
        return {
            'status' : 'success',
            'msg' : 'Projects are Getted success',
            'datas' : projects
        }
    except Exception as e:
        return {
            'status' : 'error',
            'error' : f"{e}" 
        }


@project_router.post("/project")
def creating_prject(request : s_project.Project,db : Session = Depends(get_db)):
    
    try:
        project = m_project.Project(**request.dict())
        
        db.add(project)
        db.commit()
        
        
        return {
            'status' : 'success',
            'msg' : 'Project data added',
            'data' : project
        }
    except Exception as e:
        
        return {
            'status' : 'error',
            'error' : f'{e}'
        }
        
        