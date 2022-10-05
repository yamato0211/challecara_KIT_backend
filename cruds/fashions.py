from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from db.model import Fashion, Fashion_Clothes
from schemas.fashions import Fashion as FashionSchema
from db.model import Clothe

def create_fashion(db: Session, user_id: str, clothe_ids: list[str], name:str) -> FashionSchema:
    fashion_orm = Fashion(
        user_id=user_id,
        name=name
    )
    db.add(fashion_orm)
    db.commit()
    db.refresh(fashion_orm)
    for clothe_id in clothe_ids:
        clothe = db.query(Clothe).filter(Clothe.clothe_id == clothe_id).first()
        if clothe is None:
            raise HTTPException(status_code=404, detail=f"{clothe_id} clothe not found")
        fashion = Fashion_Clothes(
            fashion_id=fashion_orm.fashion_id,
            clothe_id=clothe_id
        )
        db.add(fashion)
        db.commit()
    fashion = FashionSchema.from_orm(fashion_orm)
    return fashion
    