import os

while True:
    try:
        import scrapy
        import selenium
        import gspread
        import pandas
        import scrapy_selenium
        from dotenv import load_dotenv
        from gspread_dataframe import get_as_dataframe, set_with_dataframe
        from gspread_formatting import set_column_width
        # END TEST IMPORTS
        break
    except ModuleNotFoundError as e:
        os.system(f"pip install scrapy")
        os.system(f"pip install selenium")
        os.system(f"pip install gspread")
        os.system(f"pip install pandas")
        os.system(f"pip install python-dotenv")
        os.system(f"pip install gspread_dataframe")
        os.system(f"pip install gspread_formatting")
        os.system(f"pip install scrapy-selenium")
        # os.system(f"pip install git+https://github.com/dylanwalker/better-scrapy-selenium.git")

    
