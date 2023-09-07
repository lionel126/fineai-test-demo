from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine
from fineai_test.db.app import UserBaseInfo, UploadImageFile
from .config import settings

Sess = sessionmaker(bind=create_engine(settings.postgresql_uri_sync))

def get_user_info(user_id:int) -> UserBaseInfo | None:
    with Sess() as sess:
        stmt = select(UserBaseInfo).where(UserBaseInfo.id==user_id)
        rs = sess.execute(stmt)
        row = rs.one_or_none()
    if row:
        return row[0]
    
def get_dataset_images(model_id:int) -> list[UploadImageFile]:
    with Sess() as sess:
        stmt = select(UploadImageFile).where(UploadImageFile.user_model_id==model_id)
        rows = sess.execute(stmt).all()
    return [row[0] for row in rows]