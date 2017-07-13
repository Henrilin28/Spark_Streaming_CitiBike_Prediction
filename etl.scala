
import org.apache.spark._
import org.apache.spark.streaming._

val df = sqlContext.read.json("https://gbfs.citibikenyc.com/gbfs/en/station_status.json")

/*
val conf = new SparkConf().setAppName(appName).setMaster(master)
val ssc = new StreamingContext(conf, Seconds(1))
*/
/*
https://gbfs.citibikenyc.com/gbfs/gbfs.json

{"last_updated":1499912486,"ttl":10,"data":{"en":{"feeds":[{"name":"system_information","url":"https://gbfs.citibikenyc.com/gbfs/en/system_information.json"},{"name":"station_status","url":"https://gbfs.citibikenyc.com/gbfs/en/station_status.json"},{"name":"system_alerts","url":"https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json"},{"name":"system_regions","url":"https://gbfs.citibikenyc.com/gbfs/en/system_regions.json"},{"name":"station_information","url":"https://gbfs.citibikenyc.com/gbfs/en/station_information.json"}]}}}
*/
