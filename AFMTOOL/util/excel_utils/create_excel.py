from openpyxl import Workbook
from datetime import datetime
from openpyxl import styles
from openpyxl.styles import Color, PatternFill, Font, Border, Alignment, Side
from openpyxl.cell import Cell
import openpyxl
import pytz

workbook = Workbook()
sheet = workbook.active

tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")

def create_xl_template():
    """ 
    Creates empty template Excel sheet to be filled in 
    Return path to created Excel sheet
    """
    
    sheet["A1"] = "Lot ID: "
    sheet["A3"] = "File Name:"
    sheet["A5"] = "Top View"
    sheet["A6"] = "3D View"
    sheet["A7"] = "Cu Roughness(nm) 1umX1um"
    sheet["A8"] = "Po roughness (nm) 2umX2um"

    sheet["A9"] = "Step height (nm) Protusion : + Dishing:-"
    
    sheet["B1"] = "Slot ID: "
    
    sheet["C1"] = "CMP recipe: "
    sheet["H1"] = "Process: "
    sheet["I1"] = "Measurement: "
    
    sheet["G2"] = "Step height with example: "
    
    
    blueFill = PatternFill(start_color='000066CC',
                   end_color='000066CC',
                   fill_type='solid')

    sheet["A5"].fill = blueFill
    sheet["A6"].fill = blueFill
    sheet["A7"].fill = blueFill
    sheet["A8"].fill = blueFill
    sheet["A9"].fill = blueFill
    
    double = Side(border_style="medium", color="000000")
    
    #Align texts
    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment= Alignment(wrap_text=True, vertical='center', horizontal = 'center')
            cell.border = Border(top=double, left=double, right=double, bottom=double)
            
    sheet.column_dimensions['A'].width = 25

    target_path = "../results/xlSheets/"+ format_timestring+ "_AFMResults.xlsx"
    workbook.save(target_path)
    
    return target_path

def insert_xl(img_path_2d, img_path_3d):
    
    img_path = img_path[3:]
    
    img = openpyxl.drawing.image.Image("images/2d_height_plot.png")
    img.height = 100
    img.width = 100
    sheet.add_image(img, 'A1')
    

    workbook.save("../results/xlSheets/"+ format_timestring+ "_AFMResults.xlsx")