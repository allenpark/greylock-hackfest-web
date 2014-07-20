$(document).ready(function() {
    $('.message-input').bind('input', function(e) {
        var text = $('.message-input').val();
        if (text === '') {
            text = '&nbsp;';
        }
        $('#preview').html(text);
    });
    map_initialize();
    $('#setAddress').bind('click', setAddress);
    $('#address').bind('keyup', function(e) {
        if (e.which === 13) {
            setAddress();
        }
    });
    $('#radius').bind('keyup', function(e) {
        if (e.which === 13) {
            setAddress();
        }
    });
    if (navigator.geolocation) {
        $('#useCurrentLocation').bind('click', useCurrentLocation);
    } else {
        $('#useCurrentLocation').hide();
    }
});

var geocoder;
var map;
var marker;
var circle;
function map_initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var map_canvas = $('.map')[0];
    var map_options = {
        center: latlng,
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(map_canvas, map_options);
}
//google.maps.event.addDomListener(window, 'load', map_initialize);

function setAddress() {
    var address = $('#address').val();
    if (address === null || address === '') {
        useCurrentLocation();
        return;
    }
    showLoading();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            onLocationChange(results[0].geometry.location);
        } else {
            onMapsError('That location could not be found. Please try again.');
        }
    });
}

function useCurrentLocation() {
    if (navigator.geolocation) {
        showLoading();
        navigator.geolocation.getCurrentPosition(function(position) {
            var latlng = new google.maps.LatLng(position.coords.latitude,
                                                position.coords.longitude);
            onLocationChange(latlng);
        });
    } else {
        onMapsError('We cannot find your current location.');
    }
}

function showLoading() {
    var loading = $('#loading');
    if (loading.hasClass('hidden')) {
        loading.removeClass('hidden');
    }
}

function hideLoading() {
    var loading = $('#loading');
    if (!loading.hasClass('hidden')) {
        loading.addClass('hidden');
    }
}

function onLocationChange(location) {
    hideLoading();
    map.setCenter(location);
    var miles = parseInt($('#radius').val());
    miles = isNaN(miles) ? 1 : miles;
    var meters = miles * 1609.344; // 1609.344 meters in a mile
    var circleOptions = {
        strokeColor: '#FF0000',
        strokeOpacity: 0.5,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.1,
        map: map,
        center: location,
        radius: meters
    };
    if (circle) {
        circle.setOptions(circleOptions);
    } else {
        circle = new google.maps.Circle(circleOptions);
    }
    map.setZoom(radiusToZoom(meters));

    var channel = $('#channel').val();
    var numUsers = getNumUsersOnChannelInRadius(location, channel, miles, function(data, status, xhr) {
        handleJson(data, status, xhr, location);
    });
    // var markerOptions = {
    //     position: location,
    //     draggable: false,
    //     raiseOnDrag: false,
    //     map: map,
    //     labelContent: 'There are ' + numUsers + ' users in this radius.',
    //     labelAnchor: new google.maps.Point(100, 0),
    //     labelClass: 'labels', // the CSS class for the label
    // };
    // if (marker) {
    //     marker.setOptions(markerOptions);
    // } else {
    //     marker = new MarkerWithLabel(markerOptions);
    // }
}

function getNumUsersOnChannelInRadius(location, channel, miles, callback) {
    url = "api/getNumUsersOnChannelInRadius/"+channel+"/"+location.lat()+"/"+location.lng()+"/"+miles;
    console.log(url);
    $.getJSON(url, callback);
}
function handleJson (data, status, xhr, location){
    var markerOptions = {
        position: location,
        draggable: false,
        raiseOnDrag: false,
        map: map,
        labelContent: 'There are ' + data["num_users"] + ' users in this radius.',
        labelAnchor: new google.maps.Point(100, 0),
        labelClass: 'labels', // the CSS class for the label
    };
    if (marker) {
        marker.setOptions(markerOptions);
    } else {
        marker = new MarkerWithLabel(markerOptions);
    }
}

function onMapsError(error) {
    $('#mapsError').text(error);
}

function radiusToZoom( r ){
    var w = $('#map_canvas').width();
    var d = r * 2;
    var zooms = [,21282,16355,10064,5540,2909,1485,752,378,190,95,48,24,12,6,3,1.48,0.74,0.37,0.19];
    var z = 20;
    var m;
    while( zooms[--z] ){
        m = zooms[z] * w;
        if( d < m ){
            break;
        }
    }
    return z;
}
