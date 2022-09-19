import pytest
from app import models


@pytest.fixture
def test_vote(session,test_posts,test_user):
    new_vote=models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client,test_posts):
    res=authorized_client.post("/vote/",json={'post_id':test_posts[3].id, 'dir':1})
    assert res.status_code == 201
    assert res.json().get('message') == "Successfully added vote!"

def test_vote_twice_check(authorized_client,test_posts,test_vote):
    res=authorized_client.post("/vote/",json={'post_id':test_posts[0].id, 'dir':1})
    assert res.status_code == 409
    assert res.json().get('detail') == 'This post is already liked by you...'

def test_undo_non_exist_vote(authorized_client,test_posts):
    res=authorized_client.post("/vote/",json={'post_id':test_posts[3].id, 'dir':0})
    assert res.status_code == 404
    assert res.json().get('detail') == "Vote not found!"

def test_vote_on_non_exist_post(authorized_client,test_posts):
    res=authorized_client.post("/vote/",json={'post_id':8888, 'dir':0})
    assert res.status_code == 404
    assert res.json().get('detail') == f"Post with ID 8888 does not exist!"

def test_successful_vote_delete(authorized_client,test_posts,test_vote):
    res=authorized_client.post("/vote/",json={'post_id':test_posts[0].id, 'dir':0})
    assert res.json().get('message') == "Successfully deleted vote!"
    assert res.status_code == 201

def test_unauthorised_person_vote_on_post(client,test_posts):
    res=client.post("/vote/",json={'post_id':test_posts[3].id, 'dir':1})
    assert res.status_code == 401