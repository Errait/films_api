import json
from unittest.mock import patch

from src import app
import http

from tests.fakes_for_test import FakeStuntman


class TestStuntmen:
    @patch('src.services.stuntman_service.StuntmanService.fetch_all_stuntmen')
    def test_get_stuntmen_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/stuntmen')

        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_stuntman_with_mock(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'name': 'Test Name',
                'is_active': True,
                'actor_id': 2
            }
            resp = client.post('/stuntmen', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_stuntman_with_mock(self):
        with patch(
                'src.services.stuntman_service.StuntmanService.fetch_stuntman_by_uuid'
        ) as mocked_query, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeStuntman()
            client = app.test_client()
            url = '/stuntmen/some-valid-uuid'
            data = {
                'name': 'Update Name',
                'is_active': False,
                'actor_id': 2
            }
            resp = client.patch(url, data=json.dumps(data), content_type='application/json')

            mock_session_commit.assert_called_once()

            assert resp.status_code == http.HTTPStatus.OK

    def test_delete_film_with_mock(self):
        with patch(
                'src.services.stuntman_service.StuntmanService.fetch_stuntman_by_uuid'
        ) as mocked_query, \
                patch('src.db.session.delete', autospec=True) as mock_session_delete, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeStuntman()
            client = app.test_client()
            url = '/stuntmen/some-valid-uuid'
            resp = client.delete(url)
            assert resp.status_code == http.HTTPStatus.NO_CONTENT

            mocked_query.assert_called_once()
            mock_session_delete.assert_called_once()
            mock_session_commit.assert_called_once()

    # def test_put_stuntman_with_mock(self):
    #     with patch(
    #             'src.services.stuntman_service.StuntmanService.fetch_stuntman_by_uuid'
    #     ) as mocked_query, \
    #             patch('src.db.session.commit', autospec=True) as mock_session_commit:
    #         mocked_query.return_value = FakeStuntman()
    #         client = app.test_client()
    #         url = '/stuntmen/some-valid-uuid'
    #         data = {
    #             'name': 'New Update Name',
    #             'is_active': True,
    #             'actor_id': 1
    #         }
    #         resp = client.put(url, data=json.dumps(data), content_type='application/json')
    #
    #         mock_session_commit.assert_called_once()
    #
    #         assert resp.status_code == http.HTTPStatus.OK
