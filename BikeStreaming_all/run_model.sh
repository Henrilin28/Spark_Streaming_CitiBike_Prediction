virtualenv -p python3 ml_bike
#pip3 install pandas scikit-learn click

real_time_dir=$(ls -t file/ | head -1)

#echo $real_time_dir
python3 pyscript/etl.py file/$real_time_dir/part-00000
#python3 pyscript/load_model.py model/rf_model.sav sample/test.csv sample/test_output.csv sample/target2_id.csv
python3 pyscript/load_model.py model/rf_model3.sav sample/merge_id_value.csv sample/merge_id.csv sample/merge_id.csv
python3 pyscript/result.py 
#watch -n 5 ./run_model.sh
