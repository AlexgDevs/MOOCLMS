from fastapi import APIRouter, Depends, status

from ..db import db_manager, Module
from ..schemas import CreateModule


module_app = APIRouter(prefix='/modules', tags=['Modules'])


@module_app.post('/',
                status_code=status.HTTP_201_CREATED,
                summary='create module',
                description='endpoint for creating module for course')
async def create_module(
    module_data: CreateModule, 
    session = Depends(db_manager.db_session_begin)):

    session.add(Module(**module_data.model_dump(exclude_unset=True)))
    return {'status': 'module created'}