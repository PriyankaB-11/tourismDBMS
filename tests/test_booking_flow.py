import mysql.connector
import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


def test_admin_confirm_booking_insufficient_slots(app, monkeypatch):
    # Simulate query_db raising a MySQL error from trigger
    def fake_query_db(*args, **kwargs):
        raise mysql.connector.Error("Not enough available slots to confirm booking")

    monkeypatch.setattr('routes.booking.query_db', fake_query_db)

    client = app.test_client()
    # Set admin session
    with client.session_transaction() as sess:
        sess['admin_id'] = 1

    resp = client.post('/admin/bookings/1/status', data={'status': 'Confirmed'}, follow_redirects=True)
    assert b'Cannot confirm booking' in resp.data


def test_admin_update_booking_success(app, monkeypatch):
    # Simulate successful update
    def fake_query_db(*args, **kwargs):
        return None

    monkeypatch.setattr('routes.booking.query_db', fake_query_db)

    client = app.test_client()
    with client.session_transaction() as sess:
        sess['admin_id'] = 1

    resp = client.post('/admin/bookings/1/status', data={'status': 'Cancelled'}, follow_redirects=True)
    assert b'Booking status updated' in resp.data
