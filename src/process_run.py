import process_data as pd

def test():
    csv = 'raw_data\match_data_01_01_2024.csv'

    process = pd.process_data(csv)
    test = process.do_run()
    return test

test()
