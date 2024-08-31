from fastapi import APIRouter, HTTPException, Query, Body, Path
from app.models.table1 import test_table
from app.schemas.parameter_schema import ParameterModel



router = APIRouter(prefix="/api/v1/parameter", tags=["parameter"])

@router.post("/test/{id}")
async def parameterTest(request: ParameterModel, id: int, version: int = 1, tested: bool = True):
    return {
        "data": request,
        "id": id,
        "version": version
        }

# meta data

@router.post('/new/{id}/comment')
async def MetaData(request: ParameterModel, id: int, 
                   comment_id:  int = Query(None,
                   title='Id of the comment', 
                   description='Description of the comment', 
                   alias="commentId"),
                   content: str = Body(..., min_length=10, max_length=20)
                   ):
    return {
        'data': request,
        "id": id,
        "comment_id": comment_id,
        "content": content
    }

