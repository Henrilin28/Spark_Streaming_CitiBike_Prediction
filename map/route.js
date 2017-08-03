// var directionsDisplay;
// var directionsService = new google.maps.DirectionsService();
var map;
// var haight = new google.maps.LatLng(37.7699298, -122.4469157);
// var oceanBeach = new google.maps.LatLng(37.7683909618184, -122.51089453697205);


  var markers = [];
  var infowindows = [];
  var start_lat = 40.76727216
  var start_lon = -73.99392888

  function initMap() {
    // var directionsService = new google.maps.DirectionsService;
    // var directionsDisplay = new google.maps.DirectionsRenderer;
    //deleteMarkers();
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: start_lat, lng: start_lon}
    });
    var id = []
    var mylat = [];
    var mylng = [];
    var predict = [];
    var num_bike = [];
    d3.csv('predict_info.csv', function(data) {
        predict = Object.values(data[0]);
        num_bike = Object.values(data[1]);
        mylng = Object.values(data[3]);
        mylat = Object.values(data[4]);

        //set all bike stations!
        for(var i=0; i<mylat.length; i++) {
              if(true) {
                markers[i] = new google.maps.Marker({
                    position: {lat: Number(mylat[i]), lng: Number(mylng[i])},
                    map: map,
                    title:"destinations!"
                });
                markers[i].index = i;

                infowindows[i] = new google.maps.InfoWindow({
                  content: "number_of_bikes: " + num_bike[i] + '<br>'
                         + "prediction of bikes: " + predict[i]
                });
                google.maps.event.addListener(markers[i], 'click', function() {
                    // infowindows[this.index].open(map, markers[this.index]);
                    // map.panTo(markers[this.index].getPosition());
                    //console.log(markers[this.index].getPosition().lat());
                    setDestination(markers[this.index].getPosition().lat(), markers[this.index].getPosition().lng());
                });
                markers[i].setMap(map);
            }
        }
    });

    var onChangeHandler = function() {
      calculateAndDisplayRoute(directionsService, directionsDisplay);
    };

    //document.getElementById('start').addEventListener('change', onChangeHandler);
    //document.getElementById('end').addEventListener('change', onChangeHandler);
  }

  function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

  function clearMarkers() {
    setMapOnAll(null);
  }

  function deleteMarkers() {
    clearMarkers();
    markers = [];
  }

  function setDestination(start_lat, start_lon) {
      console.log("starting position: " + start_lat + ", " + start_lon);
      deleteMarkers();

      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: start_lat, lng: start_lon}
      });

      var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
      //set origin marker
      var marker = new google.maps.Marker({
          position: {lat: start_lat, lng: start_lon},
          map: map,
          title:"origin!",
          icon: image
      });

      var infowindow = new google.maps.InfoWindow({
        content: "starting point!"
      });

      google.maps.event.addListener(marker, 'click', function() {
          infowindow.open(map, marker);
          map.panTo(marker.getPosition());
          if (marker.getAnimation() !== null) {
              marker.setAnimation(null);
          } else {
              marker.setAnimation(google.maps.Animation.BOUNCE);
          }

      });
      console.log(marker);
      marker.setMap(map);
      var id = []
      var mylat = [];
      var mylng = [];
      var predict = [];
      var num_bike = [];
      var capacity = [];
      d3.csv('predict_info.csv', function(data) {
          predict = Object.values(data[0]);
          num_bike = Object.values(data[1]);
          capacity = Object.values(data[2]);
          mylng = Object.values(data[3]);
          mylat = Object.values(data[4]);
          var start_index = 0;
          for(var i=0; i<mylat.length; i++) {
              if(mylat[i] == start_lat) {
                start_index = i;
                break;
            }
          }
          console.log("start_index: " + start_index);
          var for_start = (start_index-50) < 0 ? 0 : (start_index - 50);
          var for_end = (start_index+50) > mylat.length ? mylat.length : (start_index + 50);

          console.log("for_start: " + for_start);

          console.log("for_end: " + for_end);
          //set destination marker
          for(var i=for_start; i<for_end; i++) {
              if(i==start_index) continue;
              if(isReach(start_lat, start_lon, Number(mylat[i]), Number(mylng[i]))) {
                  markers[i] = new google.maps.Marker({
                      position: {lat: Number(mylat[i]), lng: Number(mylng[i])},
                      map: map,
                      title:"destinations!"
                  });
                  markers[i].index = i;

                  infowindows[i] = new google.maps.InfoWindow({
                    content: "number_of_bikes: " + num_bike[i] + '<br>'
                           + "prediction_of_bikes: " + predict[i] + '<br>'
                           + "number_of_docks: " + (capacity[i] - num_bike[i]) + '<br>'
                           + "prediction_of_docks: " + (capacity[i] - predict[i]) + '<br>'
                  });
                  google.maps.event.addListener(markers[i], 'click', function() {
                      infowindows[this.index].open(map, markers[this.index]);
                      map.panTo(markers[this.index].getPosition());
                      if (markers[this.index].getAnimation() !== null) {
                          markers[this.index].setAnimation(null);
                      } else {
                          markers[this.index].setAnimation(google.maps.Animation.BOUNCE);
                      }
                  });
                  markers[i].setMap(map);
              }
          }
      });
  }

  function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
      origin: document.getElementById('start').value,
      destination: document.getElementById('end').value,
      travelMode: 'BICYCLING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
  }

  function isReach(start_lat, start_lon, lat, lon) {
      if(start_lat==lat && start_lon==lon) return false;

      url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start_lat +"," + start_lon + "&destinations=" + lat + "," + lon + "&mode=bicycling&key=AIzaSyB_2tueX2QiPdzrQtmNZPz1LIwwj620gKQ"
      var responseText = JSON.parse(Get(url));
      var elements = responseText.rows[0];
      var time = elements.elements[0].duration.value;
      console.log(time);
       if(time < 900)
         return true;

      return false;
  }

  function Get(whateverUrl) {
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET",whateverUrl,false);
        Httpreq.send(null);
        return Httpreq.responseText;
  }
