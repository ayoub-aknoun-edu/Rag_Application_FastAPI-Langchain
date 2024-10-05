from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal, ProcessingSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
import aiofiles
import logging
from .schemas.data import ProcessRequest
from models.db_schemas import DataChunk, Asset
from models.enums.AssetTypeEnum import AssetTypeEnum
from bson.objectid import ObjectId


logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)



@router.post("/upload/{project_id}")
async def upload_data(request: Request,project_id: str, file: UploadFile, app_settings:Settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    data_controller = DataController()
    is_valid, resul_signal = data_controller.validate_uploaded_file(file= file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={
                "message": resul_signal
                })
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(original_file_name=file.filename, project_id=project_id)
    try:
        async with aiofiles.open(file_path, 'wb') as buffer:
            chunck_size = app_settings.FILE_DEFAULT_CHUNK_SIZE
            while chunk := await file.read(chunck_size):
                await buffer.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOAD_FAILED.value
                })

    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset = Asset(
         asset_project_id=project.id,
         asset_type=AssetTypeEnum.FILE.value,
         asset_name= file_id,
        asset_size=os.path.getsize(file_path))
    asset_record= await asset_model.create_asset(asset=asset)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
          content={
              "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id":str(asset_record.id)
              })



@router.post("/process/{project_id}")
async def process_data(request:Request, project_id: str, process_request: ProcessRequest):


    
    chunks_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model =await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    project_file_ids = {}
    if process_request.file_id:
        asset_recod = await asset_model.get_asset_record(asset_project_id=project.id, asset_name=process_request.file_id)
        
        if asset_recod is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": ResponseSignal.NO_FILE_WITH_ID.value
                    })
        
        project_file_ids = {asset_recod.id:asset_recod.asset_name }
    else:
        project_files = await asset_model.get_all_project_assets(asset_project_id=project.id, asset_type=AssetTypeEnum.FILE.value)
        project_file_ids = {record.id:record.asset_name for record in project_files}
    
    if len(project_file_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSignal.FILE_NOT_FOUND.value
                })
    
    process_controller = ProcessController(project_id=project_id)
    
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    if do_reset == 1:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    nb_records = 0
    nb_files = 0
    for asset_id,file_id in project_file_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id)
        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunks_size,
            overlap_size=overlap_size
            )
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": ResponseSignal.FILE_PROECSSING_FAILED.value
                    })
        
        file_chunks_records = [
            DataChunk(
                    chunk_text= chunk.page_content,
                    chunk_metadata= chunk.metadata,
                    chunk_order = i+1,
                    chunk_project_id = project.id,
                    chunk_asset_id= asset_id
                    )
                    for i, chunk in enumerate(file_chunks)
        ]

        nb_records+= await chunk_model.insert_many_chunks(file_chunks_records)  
        nb_files+=1
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.FILE_PROECSSING_SUCCESS.value,
            "inserted_chunks": nb_records,
            "processed_files": nb_files
            })


 