import pytest
from app.jwt_handler import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    verify_token
)

def test_hash_password():
    password = "test_password_123"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 0

def test_verify_password():
    password = "test_password_123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_create_access_token():
    data = {"sub": "user123"}
    token = create_access_token(data)
    assert token is not None
    assert len(token) > 0

def test_decode_token():
    data = {"sub": "user123", "email": "user@example.com"}
    token = create_access_token(data)
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["email"] == "user@example.com"

def test_decode_invalid_token():
    decoded = decode_token("invalid_token_xyz")
    assert decoded is None

def test_verify_token():
    data = {"sub": "user123"}
    token = create_access_token(data)
    assert verify_token(token)
    assert not verify_token("invalid_token")
