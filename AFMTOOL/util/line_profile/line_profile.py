from openpyxl import Workbook
from datetime import datetime
import openpyxl
import pytz
from openpyxl.utils import get_column_letter

tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")


def plot_line_profile():
    