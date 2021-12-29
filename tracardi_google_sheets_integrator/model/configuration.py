from pydantic import BaseModel
from typing import Optional


class Configuration(BaseModel):
    service_account_key: str
    spreadsheet_id: str
    sheet: str
    range: str
    read: bool
    write: bool
    values: Optional[list]
