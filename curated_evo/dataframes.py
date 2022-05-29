
import pandas as pd

import gspread
from gspread.exceptions import WorksheetNotFound
from gspread_formatting import set_column_width
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from scrapy.utils.project import get_project_settings

from .env_vars import ENV
from .decorators import decorate

scrapy_settings = get_project_settings()

df_columns_list = scrapy_settings["GSHEET_COLUMNS"]

class Gsheet:

    worksheets = {}
    dataframes = {}

    error_columns_list = [
                        "Time",
                        'Spider',
                        'Process',
                        "URL",
                        "Error",
                        "Traceback"
                    ]

    @decorate.connection_retry()
    def reorder_sheets(self,new_order=[]):
        order = []
        list_of_worksheets = self.spreadsheet.worksheets()
        if new_order:
            for worksheet_name in new_order:
                for worksheet in list_of_worksheets:
                    if worksheet.title == worksheet_name:
                        order.append(worksheet)
            self.spreadsheet.reorder_worksheets(order)

    @decorate.connection_retry()
    def authenticate_gspread(self):
        # Start Gspread
        self.gc = gspread.service_account_from_dict(ENV.GOOGLE_API_KEY)
        # Access Spreadsheet via ID
        self.spreadsheet = self.gc.open_by_key(ENV.SPREADSHEET_ID)

    def __init__(self,columns_list=[]):
        # Start Google API connection
        self.authenticate_gspread()
        # Create Dataframe
        self.base_df = pd.DataFrame(columns=columns_list)
        self.errors_df = pd.DataFrame(columns=self.error_columns_list)
        self.read_worksheet('ERRORS')
    
    @decorate.connection_retry()
    def read_worksheet(self,name='DefaultSheetName'):
        try:
            worksheet = self.spreadsheet.worksheet(name)
            print(f"Getting worksheet |{name}|")
            self.worksheets.update({name:worksheet})
            sheet_df = get_as_dataframe(self.worksheets[name])
        except WorksheetNotFound as e:
            print(f"Worksheet not found --> |{name}|. {e}")
            print(f"Creating new worksheet")
            sheet_df = self.create_new_sheet(name=name)

        # REMOVE EMPTY ROWS
        sheet_df.dropna(how='all',inplace=True)
        
        self.dataframes.update({name:sheet_df})
    
    @decorate.connection_retry()
    def write_worksheet(self,name='DefaultSheetName'):
        time_name = self.get_time_name(name)
        # Sort Items on DataFrame Descending
        self.dataframes[name][time_name] = self.dataframes[name][time_name].astype('datetime64[ns]')
        # Sort Items on DataFrame Descending
        self.dataframes[name].sort_values(by=time_name, ascending = False, inplace=True)
        # Remove Duplicate Items
        if name != 'ERRORS':
            self.dataframes[name].drop_duplicates(subset=['Type','Name','Brand'],keep='first',inplace=True)
        # Write DataFrame to Sheet
        set_with_dataframe(self.worksheets[name], self.dataframes[name])

    @decorate.connection_retry()
    def add_row_to_sheet(self,data,name='DefaultSheetName'):
        # self.read_worksheet(name=name)
        time_name = self.get_time_name(name)
        
        data[time_name] = data[time_name].strftime(("%m-%d-%Y %H:%M:%S"))
        self.add_row_to_dataframe(data,name)
        self.worksheets[name].append_row(list(data.values()))
        # self.worksheets[name].sort((1, 'des'))

    @decorate.conditional_function(scrapy_settings['SAVE_TO_DATAFRAME'])
    def add_row_to_dataframe(self,data,name='DefaultSheetName'):
        row_index = self.dataframes[name].shape[0]
        self.dataframes[name].loc[row_index] = data


    @decorate.connection_retry()
    def create_new_sheet(self,name='DefaultSheetName'):

        if name != 'ERRORS':
            df_to_set = self.base_df
        else:
            df_to_set = self.errors_df
        number_of_cols = df_to_set.shape[1]

        last_column = chr(number_of_cols + 64)
        column_range = f'A:{last_column}'
        column_range_row = f'A1:{last_column}1'

        # Create worksheet
        worksheet = self.spreadsheet.add_worksheet(title=name, rows="2", cols=number_of_cols)

        # Format worksheet
        worksheet.format(column_range,{"wrapStrategy":"WRAP"})
        worksheet.format(column_range_row, {
                                                    "backgroundColor": {
                                                                          "red": 0.0,
                                                                          "green": 0.0,
                                                                          "blue": 0.0
                                                                        },
                                                    "horizontalAlignment": "CENTER",
                                                    'textFormat': {
                                                                    "foregroundColor": {
                                                                                            "red": 1.0,
                                                                                            "green": 1.0,
                                                                                            "blue": 1.0
                                                                                          },
                                                                    'bold': True
                                                                    }
                                                })
        worksheet.freeze(rows=1)
        self.resize_worksheet(worksheet)
        if name != 'ERRORS':
            self.reorder_sheets([name,'||'])

        # Set Dataframe to Blank worksheet
        set_with_dataframe(worksheet,df_to_set)

        self.worksheets.update({name:worksheet})
        self.dataframes.update({name:df_to_set})

        return self.dataframes[name]
    
    def resize_worksheet(self,worksheet):
        if worksheet.title != 'ERRORS':
            set_column_width(worksheet, 'D', 300)
            set_column_width(worksheet, 'F', 450)
        else:
            set_column_width(worksheet, 'D', 300)
            set_column_width(worksheet, 'E', 450)
            set_column_width(worksheet, 'F', 700)
    
    def get_time_name(self,name='DefaultSheetName'):
        if name != 'ERRORS':
            time_name = self.base_df.columns[0]
        else:
            time_name = self.errors_df.columns[0]
        return time_name


gsheet = Gsheet(df_columns_list)