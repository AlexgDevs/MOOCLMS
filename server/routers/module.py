from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import db_manager, Module
from ..schemas import (
    CreateModule, 
    DetailModuleResponse, 
    ModuleResponse
)

from ..utils import CustomExeptions

module_app = APIRouter(prefix='/modules', tags=['Modules'])


@module_app.get('/',
                response_model=List[ModuleResponse],
                summary='get all modules info',
                description='endpoint for getting all info modules')
async def all_modules_info(
    session = Depends(db_manager.db_session)
    ):

    modules = await session.scalars(
        select(Module)
    )

    return modules


@module_app.get('/detail/{module_id}',
                response_model=DetailModuleResponse,
                summary='get detail module info',
                description='endpoint for getting detail info by module')
async def detail_module_info(
    module_id: int,
    session = Depends(db_manager.db_session)
    ):

    module = await session.scalar(
        select(Module)
        .options(
            selectinload(Module.lessons)
            )
    )

    if not module:
        await CustomExeptions.module_not_found()

    return module


@module_app.post('',
                status_code=status.HTTP_201_CREATED,
                summary='create module',
                description='endpoint for creating module for course')
async def create_module(
    module_data: CreateModule, 
    session = Depends(db_manager.db_session_begin)):

    session.add(Module(**module_data.model_dump(exclude_unset=True)))
    return {'status': 'module created'}


@module_app.delete('/{module_id}',
                summary='delete module',
                description='endpoint for deleting module')
async def delete_module(
    module_id: int,
    session = Depends(db_manager.db_session_begin)
    ):

    module = await session.scalar(
        select(Module)
        .where(Module.id == module_id)
    )

    if not module:
        await CustomExeptions.module_not_found()

    await session.delete(module)
    return {'status': 'module deleted'}