from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


SPREADSHEET_PROPERTIES = {
    'properties': {'locale': 'ru_RU'},
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {'rowCount': 100, 'columnCount': 11}
            }
        }
    ]
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}'},
        **SPREADSHEET_PROPERTIES
    }
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheet_id']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for proj in projects:
        new_row = [proj['name'], proj['closed_data'], proj['description']]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(  # noqa
        service.spreadsheets.values.update(
            spreadsheet_id=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
