# coding=utf-8
from __future__ import unicode_literals
import xlsxwriter

from email_with_mako import rows_data, col_headers, row_headers

workbook = xlsxwriter.Workbook('core_user_report.xlsx')
worksheet = workbook.add_worksheet('核心用户')

bold = workbook.add_format({'bold': True, 'align': 'center'})

format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
format2 = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})

worksheet.write_row(0, 0, col_headers, bold)
for index, header in enumerate(row_headers, 2):
    col = 'A{}'.format(index)
    worksheet.write(col, header, bold)

for row, row_data in enumerate(rows_data):
    worksheet.write_row(row + 1, 1, row_data)

worksheet.conditional_format('B2:H11', {'type': 'cell',
                                        'criteria': '>=',
                                        'value': 50,
                                        'format': format1})

worksheet.conditional_format('B2:H11', {'type': 'cell',
                                        'criteria': '<',
                                        'value': 50,
                                        'format': format2})
worksheet.set_column('I:I', 20)
for i in range(2, 12):
    worksheet.add_sparkline(
        'I{}'.format(i),
        {'range': '核心用户!B{0}:H{0}'.format(i), 'markers': True,
         'series_color': '#E965E0'})

workbook.close()
