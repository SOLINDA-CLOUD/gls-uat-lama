# -*- coding: utf-8 -*-
# from numpy import False_
from odoo import fields, models, api
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

import base64
import pytz
import xlwt
import datetime
from dateutil import relativedelta
import time
# from dateutil.relativedelta import relativedelta
from datetime import datetime
import datetime
import calendar
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging



class ReportListTenderExcel(models.AbstractModel):
    _name = 'report.sol_report_tender.report_list_tender_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Report')

        # xlwt
        format_header = workbook.add_format({'font_name': 'Times', 'bold': True, 'align': 'center', 'size': 16, 'valign': 'vcenter', })
        format_header_2 = workbook.add_format({'font_name': 'Times', 'bold': True, 'align': 'center', 'size': 11, 'valign': 'vcenter', })
        format_header_table = workbook.add_format({'font_name': 'Times', 'bold': True, 'align': 'center', 'size': 11, 'valign': 'vcenter', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1})
        format_table_nomor = workbook.add_format({'font_name': 'Times', 'align': 'center', 'size': 11, 'valign': 'vcenter', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1})
        format_table_nomor_non_border_right = workbook.add_format({'font_name': 'Times', 'align': 'center', 'size': 11, 'valign': 'vcenter', 'left': 1, 'bottom': 1, 'top': 1, 'bg_color': 'white'})
        format_table_nomor_non_border_left = workbook.add_format({'font_name': 'Times', 'align': 'right', 'size': 11, 'valign': 'vcenter', 'right': 1, 'bottom': 1, 'top': 1, 'bg_color': 'white'})
        format_table = workbook.add_format({'font_name': 'Times', 'align': 'left', 'size': 11, 'valign': 'vcenter', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1})
        format_table_angka = workbook.add_format({'font_name': 'Times', 'align': 'right', 'size': 11, 'valign': 'vcenter', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'num_format': '"Rp." #,###0.00',})

        sheet.set_column(0, 0, 5)     
        sheet.set_column(1, 1, 5)     
        sheet.set_column(2, 2, 25)     
        sheet.set_column(3, 3, 5)     
        sheet.set_column(4, 4, 7)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)      
        sheet.set_column(8, 8, 20)      
        sheet.set_column(9, 9, 20)      
        sheet.set_column(10, 10, 20)    
        sheet.set_column(11, 11, 20)    
        sheet.set_column(13, 13, 20)    
        sheet.set_column(14, 14, 20)    
        sheet.set_column(15, 15, 20)    
        sheet.set_column(16, 16, 20)    
        sheet.set_column(17, 17, 20)    
        sheet.set_column(18, 18, 20)    
        sheet.set_column(19, 19, 20)    
        sheet.set_column(20, 20, 20)    

        column = ['F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
        banyak_po = len(obj.purchase_order_ids)

        # Judul
        sheet.merge_range('A2:' + column[(banyak_po * 2)] + '2', 'MATRIKS PERBANDINGAN HARGA ', format_header)
        sheet.merge_range('A3:' + column[(banyak_po * 2)] + '3', 'Membrane : ' , format_header_2)

        # Header table
        sheet.write('B4', 'Project :')
        sheet.write('B5', str(parse(str(obj.create_date)).strftime("%d %B %Y")))

        sheet.merge_range('B6:B8', 'No.', format_header_table)
        sheet.merge_range('C6:C8', 'Spesifikasi', format_header_table)
        sheet.merge_range('D6:D8', 'Qty', format_header_table)
        sheet.merge_range('E6:E8', 'Sat', format_header_table)
        sheet.merge_range('F6:'+ column[(banyak_po * 2) - 1] +'6', 'Penawaran', format_header_table)

        sheet.write('B9', '', format_header_table)
        sheet.write('C9', '', format_header_table)
        sheet.write('D9', '', format_header_table)
        sheet.write('E9', '', format_header_table)

        for x in range((banyak_po * 2)):
            sheet.write(column[x] + '9', '', format_header_table)
        
        data_product = []
        data_prod = []
        nomor = 1
        column1 = 0
        column2 = 1

        index = 10
        subtotal1 =[]
        for rec in obj.purchase_order_ids:
            sheet.merge_range(column[column1] + '7:'+ column[column2] + '7', rec.partner_id.name, format_header_table)
            sheet.write(column[column1] + '8', 'Harga', format_header_table)
            sheet.write(column[column2] + '8', 'Total', format_header_table)


            subtotal1.append({
                'total_price_unit': sum([datas.price_unit for datas in rec.order_line]),
                'total_price_subtotal': sum([datas.price_subtotal for datas in rec.order_line]),
                'total_price_subtotal_tax': sum([datas.price_tax for datas in rec.order_line]),
            })
            for datas in rec.order_line:
                sheet.write(str(int(column[column1])+index) + str(index), str(datas.price_unit), format_table_angka)
                sheet.write(str(int(column[column2])+index) + str(index), str(datas.price_subtotal), format_table_angka)
                index += 1

                if datas.product_id.name not in data_prod:
                    data_prod.append(datas.product_id.name)
                    data_product.append({
                        'nomor': nomor,
                        'nama_product': datas.product_id.name,
                        'qty': datas.product_qty,
                        'uom': datas.product_uom.name,
                    })

                    nomor += 1
            index = 10
                
            column1 += 2
            column2 += 2
        
        ind = 10
        for rec in data_product:
            sheet.write('B'+ str(ind), rec['nomor'], format_table_nomor)
            sheet.write('C'+ str(ind), rec['nama_product'], format_table)
            sheet.write('D'+ str(ind), rec['qty'], format_table_nomor)
            sheet.write('E'+ str(ind), rec['uom'], format_table_nomor)

            ind += 1

        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), '', format_header_table)
        sheet.write('D' + str(ind), '', format_header_table)
        sheet.write('E' + str(ind), '', format_header_table)

        for x in range((banyak_po * 2)):
            sheet.write(column[x] + str(ind), '', format_header_table)
        
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Sub Total 1', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in subtotal1:
            sheet.write(column[column1] + str(ind), str(rec['total_price_unit']), format_table_angka)
            sheet.write(column[column2] + str(ind), str(rec['total_price_subtotal']), format_table_angka)
            # sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str(rec['total_price_subtotal']), format_table_angka)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'VAT', format_table_angka)
        if obj.tax_id:
            sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), str(obj.tax_id.amount) + '%', format_table_nomor)
        else:
            sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '0%', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in subtotal1:
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str((rec['total_price_subtotal'] * obj.tax_id.amount) / 100), format_table_angka)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'customs', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), str(obj.customs) + '%', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in subtotal1:
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str((rec['total_price_subtotal'] * obj.customs) / 100), format_table_angka)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Sub Total 2', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in subtotal1:
            # sheet.write(column[column1] + str(ind), str(rec['total_price_unit']), format_table_angka)
            # sheet.write(column[column2] + str(ind), str(rec['total_price_subtotal_tax']), format_table_angka)
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str((rec['total_price_subtotal']) + ((rec['total_price_subtotal'] * obj.tax_id.amount) / 100)), format_table_angka)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Sewa CDD', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '', format_table_nomor)
        column1 = 0
        column2 = 1
        nom = 0
        for rec in obj.purchase_order_ids:
            if rec.sewa_cdd_ket:
                sheet.write(column[column1] + str(ind), str(rec.sewa_cdd_ket), format_table_nomor_non_border_right)
            else:
                sheet.write(column[column1] + str(ind), '', format_table_nomor_non_border_right)
            sheet.write(column[column2] + str(ind), str(rec.sewa_cdd_harga), format_table_nomor_non_border_left)
            subtotal1[nom]['sewa_cdd_ket'] = rec.sewa_cdd_harga
            nom += 1
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Grand total', format_header_table)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in subtotal1:
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str((rec['total_price_subtotal']) + ((rec['total_price_subtotal'] * obj.tax_id.amount) / 100) + ((rec['total_price_subtotal'] * obj.customs) / 100) + ((rec['total_price_subtotal']) + ((rec['total_price_subtotal'] * obj.tax_id.amount) / 100)) + (rec['sewa_cdd_ket'])), format_table_angka)
            column1 += 2
            column2 += 2

        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), '', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), '', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_angka)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Terms of Payment', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), 'a', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            if rec.payment_term_id:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str(rec.payment_term_id.name), format_table_nomor)
            else:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_nomor)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Delivery Time', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), 'b', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            if rec.delivery_time:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str(rec.delivery_time), format_table_nomor)
            else:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_nomor)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Price', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind), 'c', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            if rec.price:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str(rec.price), format_table_nomor)
            else:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_nomor)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), 'Notes', format_table_angka)
        sheet.merge_range('D' + str(ind) + ':' + 'E' + str(ind+1), '', format_table_nomor)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            if rec.price:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), str(rec.notes), format_table_nomor)
            else:
                sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_nomor)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.write('B' + str(ind), '', format_header_table)
        sheet.write('C' + str(ind), '', format_table_angka)
        column1 = 0
        column2 = 1
        for rec in obj.purchase_order_ids:
            sheet.merge_range(column[column1] + str(ind) + ':' + column[column2] + str(ind), '', format_table_nomor)
            column1 += 2
            column2 += 2
        ind += 1
        sheet.merge_range('B' + str(ind) +':' + column[(banyak_po * 2) - 3] + str(ind),'Vendor Terpilih', format_header_table)
        sheet.merge_range(column[(banyak_po * 2) - 2] + str(ind) + ':' + column[(banyak_po * 2) - 1] + str(ind),'', format_header_table)
        ind += 1
        sheet.merge_range('B' + str(ind) +':' + column[(banyak_po * 2) - 3] + str(ind),'TTD Persetujuan', format_header_table)
        sheet.merge_range(column[(banyak_po * 2) - 2] + str(ind) + ':' + column[(banyak_po * 2) - 1] + str(ind),'', format_header_table)


# ------------------------------------------------------------------------------------------------------------------