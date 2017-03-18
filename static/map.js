// This script links to trip_detail.html and updates/loads maps, markers, routes
// The interactive tables are inputed here

// *****************************************************************************
// JS for Google Maps
// The function initializes the map with origin on San Francisco

var map;
var uniqueId = 0;
var markers = [];
var timeout;
var chart;
var elSvc;
// var path = new Array();
var my_location = {lat: 37.7572439, lng: -122.4388962}

function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    center: my_location,
    zoom: 15,
    mapTypeId: 'roadmap'
   
  });

  $.get('/add_marker.json/'+tripCode, showMarkers);
}


function showMarkers(data) {
    if (data) {
    for (var key in data) {
      (function () {
        var myLatLng = {lat: data[key].lat, lng: data[key].lng};
        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          dragable: true});
        map.panTo(myLatLng);
        marker.id = uniqueId;
        marker.description = data[key].description;
        uniqueId ++;
        markers.push(marker);
            }); );
        }
    }
}


//Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    console.log(markers[i]);
    markers[i].setMap(map);
  }
}