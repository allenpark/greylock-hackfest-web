$(document).ready(function() {
    $('.message').bind('input', function(e) {
        var text = $('.message').val();
        if (text === '') {
            text = '&nbsp;';
        }
        $('#preview').html(text);
    });
    map_initialize();
    // $('#setAddress').bind('click', function() {setAddress(onLocationChange);});
    $('#address').bind('keyup', function(e) {
        if (e.which === 13) {
            setAddress(onLocationChange);
        }
    });
    $('#radius').bind('keyup', function(e) {
        if (e.which === 13) {
            setAddress(onLocationChange);
        }
    });
    if (navigator.geolocation) {
        $('#useCurrentLocation').bind('click', function() {useCurrentLocation(onLocationChange);});
    } else {
        $('#useCurrentLocation').hide();
    }
    $('#timeSend').mask('99/99/9999 99:99');
    $('#dateSend').mask('99/99/9999');
    $('#form').bind('keyup keypress', function(e) {
        var code = e.keyCode || e.which;
        if (code  == 13) {
            e.preventDefault();
            return false;
        }
    });
});

var geocoder;
var map;
var marker;
var circle;
function map_initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(40.7127, -74.0059);
    var map_canvas = $('.map')[0];
    var map_options = {
        center: latlng,
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(map_canvas, map_options);
}
//google.maps.event.addDomListener(window, 'load', map_initialize);

function setAddress(callback) {
    if (callback === undefined) {
        callback = onLocationChange;
    }
    var address = $('#address').val();
    if (address === null || address === '') {
        useCurrentLocation(callback);
        return;
    }
    showLoading();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            callback(results[0].geometry.location);
        } else {
            onMapsError('That location could not be found. Please try again.');
        }
    });
}

function useCurrentLocation(callback) {
    if (navigator.geolocation) {
        showLoading();
        navigator.geolocation.getCurrentPosition(function(position) {
            var latlng = new google.maps.LatLng(position.coords.latitude,
                                                position.coords.longitude);
            if (!callback) {
                callback = onLocationChange;
            }
            callback(latlng);
        });
    } else {
        onMapsError('We cannot find your current location.');
    }
}

function showLoading() {
    var loading = $('#loading');
    if (loading.hasClass('invisible')) {
        loading.removeClass('invisible');
    }
}

function hideLoading() {
    var loading = $('#loading');
    if (!loading.hasClass('invisible')) {
        loading.addClass('invisible');
    }
}

function onLocationChange(location) {
    hideLoading();
    var channel = $('#selectedChannel').text();
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

    var url = "api/getNumUsersOnChannelInRadius/" + channel + "/" + location.lat() + "/" + location.lng() + "/" + miles;
    $.getJSON(url, function(data, status, xhr) {
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
    });
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

function changeChannel(channel, objectId) {
    $('#selectedChannel').text(channel);
    document.getElementById("channel").value = objectId;
}

function submitForm() {
    var datetime = $('#timeSend').val();
    document.getElementById("datetime").value = datetime;

    if ($('#radius').text() === "") {
        $('#radius').val(1);
    }

    setAddress(function(position) {
        var latitude = position.lat();
        var longitude = position.lng();
        document.getElementById("latitude").value = latitude;
        document.getElementById("longitude").value = longitude;
        $('#form').submit();
    });
}
