var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 17.9841287, lng: 79.5332929},
      zoom: 10
    });
}