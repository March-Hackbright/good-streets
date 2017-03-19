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
var my_location = {lat: 37.7572439, lng: -122.4388962};

var endpoints = [];

function initMap() {
  
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  // var geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    center: my_location,
    zoom: 15,
    mapTypeId: 'roadmap'
  });
  directionsDisplay.setMap(map);
  document.getElementById('submit').addEventListener('click', function() {

    endpoints = [];
    clearMarkers();
    markers = [];
    calculateAndDisplayRoute(directionsService, directionsDisplay);
  });
  
}

function clearMarkers() {
        for (var i = 0; i < markers.length; i++ ){
            markers[i].setMap(null);
        }
      }


function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
      origin: document.getElementById('start').value,
      destination: document.getElementById('end').value,
      travelMode: 'WALKING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
    console.log(endpoints);
    codeAddress('start');
    codeAddress('end');

}

function codeAddress(loc) {
    var geocoder = new google.maps.Geocoder();
    address = document.getElementById(loc).value;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        // map.setCenter(results[0].geometry.location);
        // var marker = new google.maps.Marker({
        //     map: map,
        //     position: results[0].geometry.location
        // });
        var lat = results[0].geometry.location.lat();
        var lng = results[0].geometry.location.lng();
        var my_latlon = {'lat': lat, 'lng': lng};
        endpoints.push(my_latlon);
        pushEndpoints();
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }

function pushEndpoints() {
    if(endpoints.length===2) {
    console.log(endpoints);
    var dataInput = {'first': JSON.stringify(endpoints[0]),
                     'second': JSON.stringify(endpoints[1])};
    console.log(dataInput);
    // post data to route, returns data with show markers
    $.post('/markers.json', dataInput, showMarkers);
    $.post('/green-markers.json', dataInput, showgreenMarkers);
    }
}

function showMarkers(data) {
    var image = {
          url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

    if (data) {
        data = JSON.parse(data);
        // console.log(data);
        for (var geo in data) {

            var myLatLng = {lat: data[geo].lat, lng: data[geo].lng};
            var marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
              icon: image,
              dragable: true});
        
            markers.push(marker);
                }
            }
    }


function showgreenMarkers(data) {
    var marker;

          var policeMarker = {
          url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

        var greenMarker = {
          url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

    if (data) {
        // data = JSON.parse(data);
        // console.log(data);
        for (var geo in data) {
            console.log(data[geo].lat);
            var myLatLng = {lat: data[geo].lat, lng: data[geo].lng};
            var description = data[geo].category;
            if (description === 'police department') {
                marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                icon: policeMarker,
                dragable: true});
        

            } else {
              marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
              icon: greenMarker,
              dragable: true});
            }
        
            markers.push(marker);
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