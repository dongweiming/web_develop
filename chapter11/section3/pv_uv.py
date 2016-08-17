# coding=utf-8
from __future__ import unicode_literals

import xlsxwriter

workbook = xlsxwriter.Workbook('pv_uv.xlsx')

worksheet1 = workbook.add_worksheet('pv')
worksheet2 = workbook.add_worksheet('uv')
worksheet3 = workbook.add_worksheet('analysis')

chart1 = workbook.add_chart({'type': 'line'})
chart2 = workbook.add_chart({'type': 'column'})

worksheet1.set_tab_color('#4271ae')
worksheet2.set_tab_color('#c82829')
worksheet3.set_tab_color('green')

bold = workbook.add_format({'bold': 1})

pv_data = [[20233, 27855, 30126, 22737, 23331, 34791, 18075],
           [31001, 34483, 33221, 29448, 27082, 31534, 18035],
           [30771, 34543, 30001, 26257, 30778, 22168, 27469],
           [34605, 31545, 26359, 32073, 29603, 32025, 32674],
           [24035, 32267, 19562, 24721, 19573, 31712, 28171]]

uv_data = [[15509, 13787, 14492, 14093, 14008, 10630, 10363],
           [11727, 15526, 15865, 12235, 14798, 10056, 11561],
           [12699, 13125, 15009, 9606, 9555, 17222, 17231],
           [16110, 13798, 10435, 11363, 11862, 10981, 10113],
           [9306, 17165, 9803, 14932, 13226, 13047, 17671]]


cols = ['专题页{}'.format(i) for i in range(1, 6)]
headings = ['专题页', '周一', '周二', '周三', '周四', '周五', '周六', '周日']

for sheet, data in ((worksheet1, pv_data),
                    (worksheet2, uv_data)):
    sheet.write_row('A1', headings, bold)
    sheet.write_column('A2', cols, bold)
    for index, row in enumerate(data, 2):
        sheet.write_row('B{}'.format(index), row)

for sheet, chart in ((worksheet1, chart1),
                     (worksheet2, chart2)):
    for index in range(1, 6):
        chart.add_series({
            'name': '活动页{}'.format(index),
            'categories': '={}!$B$1:$H$1'.format(sheet.name),
            'values': '={0}!$B${1}:$H${1}'.format(
                sheet.name, index + 1),
        })

chart1.set_title({'name': '上周活动页 PV'})
chart1.set_x_axis({'name': 'PV'})
chart1.set_y_axis({'name': '数量'})
chart1.set_style(10)

worksheet1.insert_chart('A8', chart1, {'x_offset': 25, 'y_offset': 10})


chart2.set_title({'name': '上周活动页 UV'})
chart2.set_x_axis({'name': 'UV'})
chart2.set_y_axis({'name': '数量'})
chart2.set_style(33)
worksheet2.insert_chart('A8', chart2, {'x_offset': 25, 'y_offset': 10})

workbook.close()
