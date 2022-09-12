from .barcode.routes import router as barcode_router
from .counterparty.routes import router as counterpartycheck_router
from fastapi import APIRouter

router = APIRouter(prefix='/api')
router.include_router(barcode_router)
router.include_router(counterpartycheck_router)


@router.get('/')
async def root():
    return {'message': 'BarCodeProcesser service online!'}
