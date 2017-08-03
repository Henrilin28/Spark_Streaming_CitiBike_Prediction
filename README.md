# BikeStreaming
Get CitiBike real-time data using Spark Streaming

### To run the project: sbt run

myReceiver.scala: define custom receiver class for Spark Streaming

Parsing.scala: define functions parsing JSON formats

bikeJob.scala: main funciton to run Spark Streaming job and compute the time duration
               between the starting point and every station.

### In BikeStreaming_all folder:

  To loop machine learning model: watch -n 20 ./run_model.sh

  files in pyscript folder are for etl code and build machine learning models
  
### In Map folder:
  
  just open index.html and it's our web application.
