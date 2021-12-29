from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_google_sheets_integrator.plugin import GoogleSheetsIntegratorAction

import asyncio

async def main():
    init = {
        "service_account_key": "example.json",
        "spreadsheet_id": "example",
        "sheet": "Arkusz1",
        "range": "A2:C4",
        "read": True,
        "write": False,
        "values": [['1', '2'], ['1', '2']],
    }
    plugin = GoogleSheetsIntegratorAction(**init)

    payload = {}

    results = await plugin.run(payload)
    print(results)


asyncio.run(main())
# payload = {}
# profile = Profile(id="profile-id")
# event = Event(id="event-id",
#               type="event-type",
#               profile=profile,
#               session=Session(id="session-id"),
#               source=Entity(id="source-id"),
#               context=Context())
# result = run_plugin(GoogleSheetsIntegratorAction, init, payload,
#                     profile)
#
# print("OUTPUT:", result.output)
# print("PROFILE:", result.profile)