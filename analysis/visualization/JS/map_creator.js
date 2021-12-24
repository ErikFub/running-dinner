let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: { lat: 38.71022591158496, lng: -9.143924874381959},
  });
  map.data.addGeoJson(all_turfs);

  map.data.setStyle({strokeWeight: 1.5, strokeOpacity: 0.9});
  map.data.addListener('mouseover', function(event) {
    map.data.overrideStyle(event.feature, {fillColor: 'red'});
 });
 map.data.addListener('mouseout', function(event) {
  map.data.revertStyle();
});
}