package bikeJob

import receiver.citiBikeReceiver
import org.apache.spark.streaming.receiver.Receiver
import org.apache.spark.examples.streaming.StreamingExamples
import org.apache.spark.SparkConf
import org.apache.spark.streaming.StreamingContext
import org.apache.spark.streaming.Seconds
import scala.io.Source
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD
import java.net.URL
import scala.io.Source
import org.json4s._
import org.json4s.native.JsonMethods._
//import org.apache.spark._

object BikeJob {
  def main(args: Array[String]) {

    import util.Parsing._

    StreamingExamples.setStreamingLogLevels()

    //streaming setup
    val sparkConf = new SparkConf()
        .setAppName("BikeJob")
        .setMaster("local[4]")

    val ssc = new StreamingContext(sparkConf, Seconds(20))

    val station_status = ssc.receiverStream(new citiBikeReceiver("https://gbfs.citibikenyc.com/gbfs/en/station_status.json")).flatMap(parseStatus)
    val station_info = ssc.receiverStream(new citiBikeReceiver("https://gbfs.citibikenyc.com/gbfs/en/station_information.json")).flatMap(parseInfo)

    println("start streaming")

    //processing data
    val status_pair = station_status.map{case(num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, station_id) => (station_id, (num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled))}
    val info_pair = station_info.map{case(capacity, lon, lat, station_id) => (station_id, (capacity, lon, lat))}
    val station_pair = status_pair.join(info_pair).map{case(station_id, (status, info)) => (station_id, status._1,status._2,status._3,status._4,info._1,info._2,info._3)}

    val stations = station_pair.map{case(station_id ,a,b,c,d,e,f,g) => station_id.zip(a.zip(b.zip(c.zip(d.zip(e.zip(f.zip(g))))))).map{case(id, (aa, (bb, (cc, (dd, (ee, (ff, gg))))))) => (id, (aa,bb,cc,dd,ee,ff,gg))}}

    // station schema
    // (id, (num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, capacity, lon, lat))
    val station_list = stations.flatMap(list => list)
    val id_status = station_list.map{
        case(id, data) =>
        (id, (data._3))
    }

    //get stations within 45 mins
    // val result = station_list.map {
    //     case(id, data) =>
    //     val docks = data._3
    //     val lat = data._7
    //     val lon = data._6
    //     val num_bikes_available = data._1
    //     val url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start_lat +"," + start_lon + "&destinations=" + lat + "," + lon + "&mode=bicycling&key=AIzaSyB_2tueX2QiPdzrQtmNZPz1LIwwj620gKQ"
    //     val conn = (new URL(url)).openConnection()
    //     conn.setConnectTimeout(1000)
    //     conn.setReadTimeout(1000)
    //     val stream = conn.getInputStream()
    //     var src = (scala.util.control.Exception.catching(classOf[Throwable]) opt Source.fromInputStream(stream).mkString) match {
    //       case Some(s: String) => s
    //       case _ => ""
    //     }
    //     val json = parse(src)
    //     val rows = (json \ "rows") \ "elements" \ "duration"
    //     val time = (rows \ "value").extract[Int]
    //     //val time = 500
    //     (id, num_bikes_available, time, docks)
    // }.filter{case(id, num_bikes_available, docks, time) => time < 2700}
    // .map{case(id, num_bikes_available, time, docks) => id}  //under 45 mins
    //
    // //result.print()
    // result.repartition(1).saveAsTextFiles("file/id_result")

    //result.map{case(id, num_bikes_available, time, docks) => id +","+num_bikes_available+","+time+","+docks}.repartition(1).saveAsTextFiles("file/id_bike")

    // val status_csv = station_status.map{case(num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, station_id) => station_id + "\n" + num_bikes_available+"\n"+ num_bikes_disabled+"\n"+ num_docks_available+"\n"+num_docks_disabled}
    // status_csv.repartition(1).saveAsTextFiles("file/id_status")

    val id_value = station_status.map{case(num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, station_id) => station_id + "\n" + num_bikes_available}
    id_value.repartition(1).saveAsTextFiles("file/id_status")
    // val info_csv = station_info.map{case(capacity, lon, lat, station_id) => station_id + "\n" +capacity+ "\n" +lon+ "\n"+lat}
    // info_csv.repartition(1).saveAsTextFiles("file/id_info")

    ssc.start()
    ssc.awaitTermination()
  }
}
