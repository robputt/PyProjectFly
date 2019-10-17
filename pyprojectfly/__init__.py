import requests
import pyprojectfly.exceptions


PROJECTFLY_BASE_URL = 'https://app.projectfly.co.uk/api/v3'


class Client(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None

    def _get_token(self):
        if not self.token:
            url = '%s/login' % PROJECTFLY_BASE_URL
            payload = {'username': self.email,
                       'password': self.password}
            login_resp = requests.post(url, json=payload)

            if login_resp.status_code == 200:
                data = login_resp.json().get('data')
                token = data.get('token')
                self.token = token
                return token
            else:
                raise pyprojectfly.exceptions.NotAuthorised()
        else:
            return self.token

    def _get_headers(self):
        return {'Authorization': 'Bearer %s' % self._get_token()}

    def list_bookings(self):
        url = '%s/bookings' % PROJECTFLY_BASE_URL
        bookings_resp = requests.get(url, headers=self._get_headers())

        if bookings_resp.status_code == 200:
            return bookings_resp.json().get('data')
        else:
            raise pyprojectfly.exceptions.BackendError()

    def get_booking_by_id(self, id):
        url = '%s/bookings/%s/details' % (PROJECTFLY_BASE_URL, id)
        booking_resp = requests.get(url, headers=self._get_headers())

        if booking_resp.status_code == 200:
            return booking_resp.json().get('data')
        elif booking_resp.status_code == 403:
            raise pyprojectfly.exceptions.NotAuthorised()
        else:
            raise pyprojectfly.exceptions.BackendError()

    def list_aircraft(self):
        url = '%s/fleet/registrations' % PROJECTFLY_BASE_URL
        fleet_resp = requests.get(url, headers=self._get_headers())

        if fleet_resp.status_code == 200:
            return fleet_resp.json().get('data')
        else:
            raise pyprojectfly.exceptions.BackendError()

    def get_aircraft_by_id(self, id):
        url = '%s/fleet/registrations/%s' % (PROJECTFLY_BASE_URL, id)
        fleet_resp = requests.get(url, headers=self._get_headers())

        if fleet_resp.status_code == 200:
            return fleet_resp.json().get('data')
        else:
            raise pyprojectfly.exceptions.BackendError()

    def list_logbook(self):
        got_all_entries = False
        logbook_url = '%s/bookings/logbook' % PROJECTFLY_BASE_URL

        current_page = 0
        ret_data = []
        while not got_all_entries:
            url = '%s?page=%s' % (logbook_url, current_page)
            logbook_resp = requests.get(url, headers=self._get_headers())
            if logbook_resp.status_code == 200:
                data = logbook_resp.json().get('data')
                ret_data.extend(data)
                if len(data) < 1:
                    got_all_entries = True
            else:
                raise pyprojectfly.exceptions.BackendError()
            current_page += 1
        return ret_data
