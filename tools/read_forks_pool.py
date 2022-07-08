from openpyxl import load_workbook


def read_forks_pool(xlsx_path):
    wb = load_workbook(filename=xlsx_path)
    worksheet1 = wb.active
    stock_list = []
    for cell in worksheet1['A']:
        stock_list.append(cell.value)

    return stock_list[1:]
