import os
import freshdesk.config.local_vars as conf
import requests
from datetime import datetime


class FreshdeskApiRequest:
    """Client to Connect to the Freshdesk API
    Documentation can be found here: https://developers.freshdesk.com/v2/docs/data-api/"""

    def __init__(self):

        self.__credentials = {
            'api_key': conf.FRESHDESK_API_KEY,
            'url': conf.FRESHDESK_URL,
            'passkey': conf.FRESHDESK_PASSWORD
        }
        self.__validate_credentials()
        self.__api_key = self.__credentials['api_key']
        self.__url = self.__credentials['url']
        self.__passkey = self.__credentials['passkey']
        self.__filename = 'tickets_data_{date}.csv'
        self.__output_path = conf.DATA_FOLDER

    def __validate_credentials(self):
        """ Validates Freshdesk API credentials available in configuration file """
        for key, value in self.__credentials.items():
            if not value:
                raise Exception(
                    f'Freshdesk API credentials are not complete. Please make sure that `{key}` has a valid value')

    def request_report(self):
        """Request the report from the Freshdesk API and returns the response code"""
        redirect_uri = self.__url + "/tickets"

        try:
            response = requests.get(redirect_uri, auth=(self.__api_key, self.__passkey))

            if response.status_code in [200, 202]:
                return response.content

        # raise exceptions in case of failures from the API
        except Exception as err:
            raise Exception(err)

    def get_output_file(self):
        """Gets the output file name with path that will be written per day"""

        report_date = datetime.today().strftime('%Y%m%d')
        output_file_name = self.__filename.format(date=report_date)
        # Generate the complete file path
        output_file_with_path = os.path.join(self.__output_path, output_file_name)

        return output_file_with_path
