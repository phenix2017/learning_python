# Search all the files in a folder

# import os
# path = os.getcwd()
# os.walk(path) 

from win32com import client 

app =  client.Dispath("Excel.Application")
app.Visible = False

input_file = "input_file_path_name"
output_file = "output_file_path_name"

ws_index_list = [1, 2] # worksheet index 

workbook = app.Workbooks.Open(input_file)

workbook.WorkSheets(ws_index_list).Select()

print_area = 'A1:E40'

# Set the page to be print
for index in ws_index_list:
    worksheet = workbook.Worksheets[index-1] # 
    worksheet.PageSetup.Zoom = False
    worksheet.PageSetup.FitToPagesTall = 1
    worksheet.PageSetup.FitToPagesWidth = 1
    worksheet.PaggeSetup.PrintArea = print_area

workbook.AvtiveSheet.ExportAsFixedFormat(0, output_file)
