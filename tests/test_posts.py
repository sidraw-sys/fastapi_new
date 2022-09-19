from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json()) 

    assert len(res.json())==len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client,test_posts):
    res=client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client,test_posts):
    res=client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client):
    res=authorized_client.get('/posts/88888')
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res=authorized_client.get(f'/posts/{test_posts[0].id}')
    post=schemas.PostOut(**res.json())
    
    assert res.status_code == 200
    assert post.Post.title == test_posts[0].title
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content



@pytest.mark.parametrize("title,content,published",[
    ('new title 1','awesome content',True),
    ('pizzas','I love my pizza',False),
    ('tallest buildings','i love skyscrapers',True),
])
def test_create_post(authorized_client,title,content,published,test_user):
    res=authorized_client.post('/posts/',json={'title':title, 'content':content, 'published':published})
    post=schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert post.title ==  title
    assert post.content ==  content
    assert post.published ==  published
    assert post.owner_id == test_user['id']

def test_default_published_value(authorized_client,test_user):
    res=authorized_client.post('/posts/',json={'title':'Test Title', 'content':'Test Content'})
    post=schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert post.title ==  'Test Title'
    assert post.content ==  'Test Content'
    assert post.published ==  True
    assert post.owner_id == test_user['id']
    

def test_unauthorized_user_create_post(client):
    res=client.post('/posts/',json={'title':'Test Title', 'content':'Test Content','published':True})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_posts):
    res=client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post_not_exist(authorized_client,test_posts):
    res=authorized_client.delete(f'/posts/88888')
    assert res.status_code == 404

def test_authorized_user_delete_valid_post(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_user_deleteing_post_not_theirs(authorized_client,test_posts):
    res=authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 401

def test_update_post(authorized_client,test_posts):
    res=authorized_client.put(f"/posts/{test_posts[0].id}",json={'title':'Updated Title', 'content':'Updated Content'})
    updated_post=schemas.Post(**res.json())
    assert res.status_code == 200
    assert test_posts[0].title == updated_post.title
    assert test_posts[0].content == updated_post.content

def test_update_other_user_post(authorized_client,test_posts):
    res=authorized_client.put(f"/posts/{test_posts[3].id}",json={'title':'Updated Title', 'content':'Updated Content'})    
    assert res.status_code == 401

def test_unauthorized_user_update_post(client,test_posts):
    res=client.put(f"/posts/{test_posts[0].id}",json={'title':'Updated Title', 'content':'Updated Content'})    
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client,test_posts):
    res=authorized_client.put(f"/posts/88888",json={'title':'Updated Title', 'content':'Updated Content'})    
    assert res.status_code == 404