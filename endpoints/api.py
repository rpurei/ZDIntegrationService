from .barcode.routes import router as barcode_router
from fastapi import APIRouter

router = APIRouter(prefix='/api')
router.include_router(barcode_router)


@router.get('/')
async def root():
    return {'message': 'BarCodeProcesser service online!'}
