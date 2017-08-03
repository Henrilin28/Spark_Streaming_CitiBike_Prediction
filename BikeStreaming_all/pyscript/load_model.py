# load the model from disk
import click
import pandas as pd
from sklearn.externals import joblib

@click.command()
@click.argument('model_path', type=click.Path(exists=True))
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_station', type=click.Path(exists=True))
@click.argument('target_dict', type=click.Path(exists=True))
def main(input_file, output_station, model_path, target_dict):
    """ main function"""

    output_stations = []
    with open(output_station) as f:
        for line in f:
            output_stations.extend([str(n).strip()
            for n in line.strip().split(',')])

    targets_name = []
    with open(target_dict) as f:
        for line in f:
            targets_name.extend([n.replace('_nxt15', '')
                                for n in line.strip().split(',')])

    features = pd.read_csv(input_file)
    loaded_model = joblib.load(model_path)
    result = pd.DataFrame(loaded_model.predict(features))
    result.columns = targets_name

    #result[output_stations].to_csv(
    #    "./result/{}.csv".format('_'.join(output_stations)))
    result[output_stations].to_csv(
        "./result/predict.csv")
        
    print('predict!!!!!!!')
if __name__ == '__main__':
    main()
