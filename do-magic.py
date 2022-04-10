import os
import warnings
import openpyxl
from openpyxl.utils import get_column_letter

warnings.simplefilter("ignore")


def set_border(ws, cell_range):
    thin = openpyxl.styles.Side(border_style="thin", color="757171")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = openpyxl.styles.Border(top=thin, left=thin, right=thin, bottom=thin)
            cell.comment = None
            # cell.alignment = Alignment(wrap_text=True)


def set_header(ws, cell_range):
    for row in ws[cell_range]:
        for cell in row:
            cell.fill = openpyxl.styles.PatternFill(start_color="0B5394", fill_type="solid")
            cell.font = cell.font.copy(color="ffffff")
            cell.alignment = openpyxl.styles.Alignment(horizontal='center')


def check_end(ws):
    no_end = True
    i = 8
    while no_end:
        if ws['A{}'.format(i)].value:
            pass
        else:
            no_end = False
            return i
        i += 1


def check_max_col(ws):
    no_end = True
    i = 8
    while no_end:
        if not ws['{}4'.format(get_column_letter(i))].value:
            no_end = False
        i += 1
    return get_column_letter(i - 2)


def check_start_a(ws):
    for i in range(5, 19):
        if ws['a{}'.format(i)].value:
            return (i)


def check_start_f(ws):
    col_range = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    for i, n in enumerate(col_range):
        if ws['{}2'.format(n)].value:
            return col_range[i], col_range[i - 1]

def check_for_hide_colums(n, e, ws):
    to_hide = []
    col_range = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    for i, col in enumerate(col_range):
        if '[Attr' in str(ws['{}{}'.format(col,n)].value):
            to_hide.append(col)
    return(to_hide)


def hide_cols(to_hide, ws):
    for col in to_hide:
        ws.column_dimensions[col.upper()].hidden = True       
    return ws


def check_for_hide_rows(n, m, ws):
    to_hide = []
    for row in range(1, n):
        if '[Attr' in str(ws['{}{}'.format(m, row)].value):
            to_hide.append(row)
    return to_hide


def hide_rows(to_hide, ws):
    for row in to_hide: 
        ws.row_dimensions[row].hidden = True     
    return ws    


if __name__ == '__main__':
    dir_list = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "work", ""))

    for filename in dir_list:
        print("---------" + filename)
        wb = openpyxl.load_workbook(os.path.join(os.path.dirname(os.path.realpath(__file__)), "work", filename))
        for ws_name in wb.sheetnames:
            ws = wb[ws_name]
            for i, row in enumerate(ws.rows):
                ws.column_dimensions[get_column_letter(i + 1)].width = 25
            n = check_start_a(ws) # start of first block
            m, e = check_start_f(ws) # m = start colum of second block; e = end colum of first block; 
            end = check_end(ws) # end of first block
            col = check_max_col(ws) # end colum
            to_hide = check_for_hide_colums(n, e, ws)
            ws = hide_cols(to_hide, ws)
            to_hide = check_for_hide_rows(n, m, ws)
            ws = hide_rows(to_hide, ws)    
            set_border(ws, 'A{}:{}{}'.format(n, e, end))
            set_border(ws, '{}1:{}{}'.format(m, col, end))

            set_header(ws, 'A{}:{}{}'.format(n, e, n))
            set_header(ws, '{}1:{}{}'.format(m, m, n - 1))

        wb.save(os.path.join(os.path.dirname(os.path.realpath(__file__)), "done", filename))