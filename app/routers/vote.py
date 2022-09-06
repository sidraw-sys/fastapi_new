from typing import List, Optional
from fastapi import HTTPException,status,Response,Depends,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    post_exist=db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {vote.post_id} does not exist!")
    
    vote_query=db.query(models.Vote).filter(models.Vote.user_id==current_user.id,models.Vote.post_id==vote.post_id)
    vote_exist=vote_query.first()

    if vote.dir==1:
        if vote_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='This post is already liked by you...')
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message":"Successfully added vote!"}
    
    else:
        if vote_exist:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"Successfully deleted vote!"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote not found!")

        



        
