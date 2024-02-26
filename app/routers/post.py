from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)


@router.get("/", response_model = List[schemas.Posts])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    

# @router.get("/posts")
# def get_pasts():
#     cursor.execute("""Select * from posts """)
#     posts = cursor.fetchall()
#     return{"data": posts}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Posts)
def create_posts(post:schemas.Post, db : Session = Depends(get_db) ):
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) Returning * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return{'data': new_post}

@router.get("/{id}", response_model = schemas.Posts)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()



    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
        
    return post

# @router.get("/posts/{id}")
# def get_post(id:int, response: Response):
#     cursor.execute("Select * from posts where id = %s", (str(id)))
#     post = cursor.fetchone()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return{"message": f"post for id {id} not found"}
        
#     # print(post)
#     return{"post_details": post}


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    # deleted_posts = db.query(models.Post).filter(models.Post.id == id).first().delete()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("Delete from  posts where id = %s returning * ", (str(id),))
#     deleted_posts = cursor.fetchone()
#     conn.commit()
    
#     if deleted_posts==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int , post:schemas.Post, db: Session = Depends(get_db), response_model = schemas.Posts):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()

    
    return post_query.first()


# @router.put("/posts/{id}")
# def update_post(id:int, post:Post):
#     cursor.execute("Update posts set title = %s, content = %s, published = %s  where id = %s returning *", (post.title, post.content, post.published, str(id)),)
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
#     return {'message': updated_post}
