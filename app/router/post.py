from fastapi import APIRouter
from fastapi import HTTPException, status, Response, Depends
from sqlmodel import Session, select
from .. import models, oauth2
from ..database import get_session


router = APIRouter(tags=["Posts"], prefix="/posts")

@router.post("/", response_model=models.PostPublic, status_code=status.HTTP_201_CREATED)
def create_Post(post: models.PostCreate, user_credentials = Depends(oauth2.get_current_user), session: Session = Depends(get_session)):
    new_post = models.Posts(user_id=user_credentials.id,**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
    

@router.get("/", response_model=list[models.PostPublic])
def get_posts(session: Session = Depends(get_session)):
    posts = session.exec(select(models.Posts)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no data in the database")
    return posts

@router.get("/{id:int}", response_model=models.PostPublic)
def get_specific_post(id:int, session: Session = Depends(get_session)):
    post = session.get(models.Posts, id)    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no content with an id of {id}")
    return post

@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, user_credentials = Depends(oauth2.get_current_user),session: Session = Depends(get_session)):
    post = session.get(models.Posts, id)    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no content with an id of {id}")
    # if post.user_id != user_credentials.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform this action!")
    
    session.delete(post)
    session.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    

@router.patch("/{id:int}", response_model=models.PostPublic)
def update_post(id:int, posts: models.PostUpdate, session: Session = Depends(get_session), user_credentials = Depends(oauth2.get_current_user)):
    db_post = session.get(models.Posts, id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no content with an id of {id}")
    if db_post.user_id != user_credentials.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform this action!")

    new_post = posts.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(new_post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post
