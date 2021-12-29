from aiohttp import ClientConnectorError
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

import os.path

from googleapiclient.discovery import build
from google.oauth2 import service_account

from tracardi_google_sheets_integrator.model.configuration import Configuration

class GoogleSheetsIntegratorAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = Configuration(**kwargs)

    async def run(self, payload):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = self.config.service_account_key
        SAMPLE_SPREADSHEET_ID = self.config.spreadsheet_id
        SAMPLE_RANGE_NAME = f"{self.config.sheet}!{self.config.range}"

        creds = None
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        try:
            if self.config.read is True and self.config.write is True:
                return ValueError("You can't read and write data ath the same time.")

            if self.config.read is True:
                service = build('sheets', 'v4', credentials=creds)

                sheet = service.spreadsheets()
                read_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range=self.config.range).execute()
                values = read_result.get('values', [])

                if not values:
                    response = 'No data found.'
                else:
                    response = read_result

            elif self.config.write is True:
                if self.config.values is None:
                    raise ValueError("If you want to parse data, set values to parse")

                service = build('sheets', 'v4', credentials=creds)
                sheet = service.spreadsheets()

                write_request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                                    valueInputOption="USER_ENTERED",
                                                    body={"values": self.config.values}).execute()

                response = write_request

            else:
                response = None

        except ClientConnectorError as e:
            return Result(port="response", value=None), Result(port="error", value=str(e))

        return Result(port="payload", value=response)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_google_sheets_integrator.plugin',
            className='GoogleSheetsIntegratorAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1',
            license="MIT",
            author="Marcin Gaca",
            init={
                "service_account_key": None,
                "sample_spreadsheet_id": None,
                "sheet": None,
                "range": None,
                "read": False,
                "write": False,
                "values": None,
            }
        ),
        metadata=MetaData(
            name='tracardi-tracardi-google-sheets-integrator',
            desc='This plugin connects Tracardi to Google Sheets.',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["General"]
        )
    )