import pandas as pd


def read_data(filename = 'norm.xlsx'):
    xl_file = pd.ExcelFile(filename)
    dfs = {sheetname: xl_file.parse(sheetname) for sheetname in xl_file.sheet_names}
    dfs['t']=dfs[xl_file.sheet_names[0]].T.columns.values.tolist()
    return dfs
read_data('data/norm.xlsx')