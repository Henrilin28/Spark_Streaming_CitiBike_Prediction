# BikeStreaming
Get CitiBike real-time data using Spark Streaming

## BikeStreaming_all folder:

To run the project: sbt run

myReceiver.scala: define custom receiver class for Spark Streaming

Parsing.scala: define functions parsing JSON formats

bikeJob.scala: main funciton to run Spark Streaming job every 20s

## In BikeStreaming_all/pyscript folder:

  To loop machine learning model: watch -n 20 ./run_model.sh

  files in pyscript folder are for etl code and build machine learning models
  
## In Map folder:
  
  just open index.html and it's our web application.
