from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_user_create(client):
    res=client.post('/users/',json={'email':'hello123@gmail.com', 'password':'password123'})
    new_user=schemas.UserResponse(**res.json())
    assert new_user.email=='hello123@gmail.com'
    assert res.status_code==201

def test_user_login(client,test_user):
    #  test_user ==> dict
    # res ==> dict
    res=client.post('/login',data={'username':test_user['email'],'password':test_user['password']})
    #login_res ==> unpacked json response
    login_res= schemas.Token(**res.json())
    #payload ==> dict
    payload=jwt.decode(login_res.access_token , settings.secret_key, settings.algorithm)

    assert test_user['id'] == payload.get('User_ID')
    assert login_res.token_type=='bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
    ('hello123@gmail.com','wrongpassword',403),
    ('wrongemail@gmail.com','password123',403),
    ('wrongemail@gmail.com','wrongpassword',403),
    (None,'wrongpassword',422),
    ('hello123@gmail.com',None,422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post('/login',data={'username':email, 'password':password})

    assert res.status_code == status_code




