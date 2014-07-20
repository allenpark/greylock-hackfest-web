$('document').ready(function() {
    console.log('Ready!');
});
var map, mapCanvas;

function toggleMap(id, numUsers, latitude, longitude, radius) {
    var mapButton = $('#mapButton' + id);
    var mapContainer = $('#mapContainer' + id);
    if (mapContainer.hasClass('hidden')) {
        mapContainer.removeClass('hidden');
        mapButton.text('Hide');
        if (!mapContainer.hasClass('loaded')) {
            mapContainer.addClass('loaded');
            mapCanvas = $('#mapCanvas' + id)[0];
            var center = new google.maps.LatLng(latitude, longitude);
            var mapOptions = {
                center: center,
                zoom: 8,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(mapCanvas, mapOptions);
            var meters = radius * 1609.344;
            var circleOptions = {
                strokeColor: '#FF0000',
                strokeOpacity: 0.5,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.1,
                map: map,
                center: center,
                radius: meters
            };
            var circle = new google.maps.Circle(circleOptions);
            var markerOptions = {
                position: center,
                draggable: false,
                raiseOnDrag: false,
                map: map,
                labelContent: 'There were ' + numUsers + ' users in this radius.',
                labelAnchor: new google.maps.Point(100, 0),
                labelClass: 'labels', // the CSS class for the label
            };
            var marker = new MarkerWithLabel(markerOptions);
        }
    } else {
        mapContainer.addClass('hidden');
        mapButton.text('Expand');
    }
}
