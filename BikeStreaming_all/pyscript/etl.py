import pandas as pd
import sys
import re

def main():
    #clean real_time data
    real_time = pd.read_csv(sys.argv[1])
    real_time.replace(r"List\(", "", regex=True, inplace=True)
    real_time.replace(r"\)", "", regex=True, inplace=True)
    real_time.columns = real_time.columns.str.replace(r"List\(", "")
    real_time.columns = real_time.columns.str.replace(r"\)", "")
    real_time.columns = real_time.columns.str.replace(r" ", "")
    real_time.to_csv("sample/real_time_clean.csv", index=False)

    #left join id for model
    merge_id = pd.read_csv("sample/merge_id.csv")
    id_value = pd.read_csv("sample/real_time_clean.csv")
    merge_id_value = pd.concat([merge_id, id_value], axis=0, join='inner')
    merge_id_value.to_csv("sample/merge_id_value.csv", index=False)


if __name__ == '__main__':
    main()
