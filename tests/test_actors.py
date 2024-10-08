import json
from unittest.mock import patch

from src import app
import http

from tests.fakes_for_test import FakeActor, FakeFilm


class TestActors:
    @patch('src.services.actor_service.ActorService.fetch_all_actors')
    def test_get_actors_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/actors')

        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_actor_with_mock(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'name': 'Test Name',
                'birthday': '2010-04-01',
                'is_active': 'true'
            }
            resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_actor_with_mock_db(self):
        with patch('src.services.actor_service.ActorService.fetch_actor_by_uuid') as mocked_query, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeActor()
            client = app.test_client()
            url = f'/actors/1'
            data = {
                'name': 'Update Name',
                'birthday': '2010-04-01',
                'is_active': 'true'
            }
            resp = client.patch(url, data=json.dumps(data), content_type='application/json')

            mock_session_commit.assert_called_once()

            assert resp.status_code == http.HTTPStatus.OK

    def test_delete_actor_with_mock(self):
        with patch('src.services.actor_service.ActorService.fetch_actor_by_uuid') as mocked_query, \
                patch('src.db.session.delete', autospec=True) as mock_session_delete, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeActor()
            client = app.test_client()
            url = f'/actors/1'
            resp = client.delete(url)
            assert resp.status_code == http.HTTPStatus.NO_CONTENT

            mocked_query.assert_called_once()
            mock_session_delete.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_actor_filmography(self):
        with patch(
                'src.services.actor_service.ActorService.fetch_actor_by_uuid'
        ) as mocked_query_actor, \
                patch(
                    'src.services.film_service.FilmService.fetch_film_by_uuid'
                ) as mocked_query_film, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query_actor.return_value = FakeActor()
            mocked_query_film.return_value = FakeFilm()
            data = {
                'filmography': ['film-uuid-1']
            }
            client = app.test_client()
            url = f'/actors/1'
            resp = client.patch(url, data=json.dumps(data), content_type='application/json')
            print(f"Response: {resp.json}")

            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.OK
