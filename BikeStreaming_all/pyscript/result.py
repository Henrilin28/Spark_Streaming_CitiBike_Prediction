import pandas as pd
import sys


def main():
    #left join id for model
    predict = pd.read_csv("result/predict.csv")
    info = pd.read_csv("sample/info.csv")
    status = pd.read_csv("sample/real_time_clean.csv")
    predict_info = pd.concat([predict, status, info], axis=0, join='inner')
    #predict_value, real_time_value, capacity, lat, lng
    predict_info.to_csv("result/predict_info.csv", index=False)
    predict_info.to_csv("../BDAD_Project/map/predict_info.csv", index=False)
    print("info complete")
if __name__ == '__main__':
    main()
