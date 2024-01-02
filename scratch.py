import process_data as pd

def test():
    csv = 'match_data_01_01_2024.csv'

    process = pd.process_data(csv)
    test = process.do_process()
    return test

test()
