import pytest

SIGNUP_URL = "/auth/signup"
LOGIN_URL = "/auth/login"
PING_URL = "/auth/ping"
FORGOT_URL = "/auth/forgot-password"


# ── ping ────────────────────────────────────────────────────────────────────

def test_ping(client):
    res = client.get(PING_URL)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Auth blueprint working"


# ── signup ──────────────────────────────────────────────────────────────────

def test_signup_success(client, clean_db):
    res = client.post(SIGNUP_URL, json={
        "email": "admin@test.com",
        "password": "password123",
        "org_name": "TestOrg"
    })
    data = res.get_json()
    assert res.status_code == 201
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["role"] == "ADMIN"


def test_signup_first_user_is_admin(client, clean_db):
    res = client.post(SIGNUP_URL, json={
        "email": "first@test.com",
        "password": "password123",
        "org_name": "OrgA"
    })
    assert res.get_json()["role"] == "ADMIN"


def test_signup_second_user_is_user_role(client, clean_db):
    client.post(SIGNUP_URL, json={
        "email": "admin@org.com",
        "password": "password123",
        "org_name": "OrgB"
    })
    res = client.post(SIGNUP_URL, json={
        "email": "member@org.com",
        "password": "password123",
        "org_name": "OrgB"
    })
    assert res.get_json()["role"] == "USER"


def test_signup_missing_fields(client, clean_db):
    res = client.post(SIGNUP_URL, json={
        "email": "missing@test.com"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_signup_duplicate_email(client, clean_db):
    payload = {
        "email": "dup@test.com",
        "password": "password123",
        "org_name": "DupOrg"
    }
    client.post(SIGNUP_URL, json=payload)
    res = client.post(SIGNUP_URL, json=payload)
    assert res.status_code == 409


# ── login ───────────────────────────────────────────────────────────────────

def test_login_success(client, clean_db):
    client.post(SIGNUP_URL, json={
        "email": "login@test.com",
        "password": "password123",
        "org_name": "LoginOrg"
    })
    res = client.post(LOGIN_URL, json={
        "email": "login@test.com",
        "password": "password123"
    })
    data = res.get_json()
    assert res.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(client, clean_db):
    client.post(SIGNUP_URL, json={
        "email": "wrongpw@test.com",
        "password": "correct",
        "org_name": "WrongOrg"
    })
    res = client.post(LOGIN_URL, json={
        "email": "wrongpw@test.com",
        "password": "incorrect"
    })
    assert res.status_code == 401


def test_login_missing_credentials(client, clean_db):
    res = client.post(LOGIN_URL, json={})
    assert res.status_code == 400


def test_login_nonexistent_user(client, clean_db):
    res = client.post(LOGIN_URL, json={
        "email": "ghost@test.com",
        "password": "password123"
    })
    assert res.status_code == 401


# ── forgot password ─────────────────────────────────────────────────────────

def test_forgot_password_existing_user(client, clean_db):
    client.post(SIGNUP_URL, json={
        "email": "forgot@test.com",
        "password": "password123",
        "org_name": "ForgotOrg"
    })
    res = client.post(FORGOT_URL, json={"email": "forgot@test.com"})
    assert res.status_code == 200


def test_forgot_password_nonexistent_user(client, clean_db):
    res = client.post(FORGOT_URL, json={"email": "nobody@test.com"})
    # Should still return 200 — security best practice, don't leak emails
    assert res.status_code == 200


def test_forgot_password_missing_email(client, clean_db):
    res = client.post(FORGOT_URL, json={})
    assert res.status_code == 400
