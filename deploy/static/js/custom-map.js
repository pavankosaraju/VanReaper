var clickmap = null;
    var clickmap_markers = [];
    var clickmap_rectangles = [];
    var clickmap_circles = [];
    var clickmap_polygons = [];
    var clickmap_polylines = [];
    var prev_infowindow_clickmap = null;

    function initialize_clickmap() {
        document.getElementById('clickmap').style.display = 'block';
        clickmap = new google.maps.Map(
        document.getElementById('clickmap'), {
            center: new google.maps.LatLng(37.4419, -122.1419),
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoomControl: true,
            mapTypeControl: true,
            scaleControl: true,
            streetViewControl: true,
            rotateControl: true,
            scrollwheel: true,
            fullscreenControl: true
        });

        //center map location on user location
        

        // add gmap markers
        var raw_markers = [{"lat": 37.45, "lng": -122.135}, {"lat": 37.44, "lng": -122.135}, {"lat": 37.43, "lng": -122.135}, {"lat": 36.42, "lng": -122.135}, {"lat": 36.41, "lng": -121.135}];
        for(i=0; i<5;i++) {
            clickmap_markers[i] = new google.maps.Marker({
                position: new google.maps.LatLng(raw_markers[i].lat, raw_markers[i].lng),
                map: clickmap,
                icon: raw_markers[i].icon,
                title: raw_markers[i].title ? raw_markers[i].title : null
            });

           if(raw_markers[i].infobox)
           {
                google.maps.event.addListener(
                        clickmap_markers[i],
                        'click',
                        getInfoCallback(clickmap, raw_markers[i].infobox)
                );
           }
        }

        
        google.maps.event.addListener(
        	clickmap,
            'click',
			function(event) { clickposCallback('/clickpost/', event.latLng) }
        );
                

        

        // add rectangles
        var raw_rectangles = [];
        for(i = 0; i < 0; i++) {
            clickmap_rectangles[i] = new google.maps.Rectangle({
                strokeColor: raw_rectangles[i].stroke_color,
                strokeOpacity: raw_rectangles[i].stroke_opacity,
                strokeWeight: raw_rectangles[i].stroke_weight,
                fillColor: raw_rectangles[i].fill_color,
                fillOpacity: raw_rectangles[i].fill_opacity,
                map: clickmap,
                bounds: {
                    north: raw_rectangles[i].bounds.north,
                    east: raw_rectangles[i].bounds.east,
                    south: raw_rectangles[i].bounds.south,
                    west: raw_rectangles[i].bounds.west },
            });

           if(raw_rectangles[i].infobox)
           {
                google.maps.event.addListener(
                        clickmap_rectangles[i],
                        'click',
                        getInfoCallback(clickmap, raw_rectangles[i].infobox)
                );
           }
        }

        // add circles
        var raw_circles = [];
        for(i = 0; i < 0; i++) {
            clickmap_circles[i] = new google.maps.Circle({
                strokeColor: raw_circles[i].stroke_color,
                strokeOpacity: raw_circles[i].stroke_opacity,
                strokeWeight: raw_circles[i].stroke_weight,
                fillColor: raw_circles[i].fill_color,
                fillOpacity: raw_circles[i].fill_opacity,
                map: clickmap,
                center: {
                    lat: raw_circles[i].center.lat,
                    lng: raw_circles[i].center.lng,
                },
                radius: raw_circles[i].radius
            });

           if(raw_circles[i].infobox)
           {
                google.maps.event.addListener(
                        clickmap_circles[i],
                        'click',
                        getInfoCallback(clickmap, raw_circles[i].infobox)
                );
           }
        }

        // add polygons
        var raw_polygons = [];
        for(i = 0; i < 0; i++) {
            clickmap_polygons[i] = new google.maps.Polygon({
                strokeColor: raw_polygons[i].stroke_color,
                strokeOpacity: raw_polygons[i].stroke_opacity,
                strokeWeight: raw_polygons[i].stroke_weight,
                fillOpacity: raw_polygons[i].fill_opacity,
                fillColor: raw_polygons[i].fill_color,
                path: raw_polygons[i].path,
                map: clickmap,
                geodesic: true
            });

           if(raw_polygons[i].infobox)
           {
                google.maps.event.addListener(
                        clickmap_polygons[i],
                        'click',
                        getInfoCallback(clickmap, raw_polygons[i].infobox)
                );
           }
        }

        // add polylines
        var raw_polylines = [];
        for(i = 0; i < 0; i++) {
            clickmap_polylines[i] = new google.maps.Polyline({
                strokeColor: raw_polylines[i].stroke_color,
                strokeOpacity: raw_polylines[i].stroke_opacity,
                strokeWeight: raw_polylines[i].stroke_weight,
                path: raw_polylines[i].path,
                map: clickmap,
                geodesic: true
            });

           if(raw_polylines[i].infobox)
           {
                google.maps.event.addListener(
                        clickmap_polylines[i],
                        'click',
                        getInfoCallback(clickmap, raw_polylines[i].infobox)
                );
           }
        }

        
    }

    function getInfoCallback(map, content) {
        var infowindow = new google.maps.InfoWindow({content: content});
        return function(ev) {
            if( prev_infowindow_clickmap ) {
                prev_infowindow_clickmap.close();
            }
            prev_infowindow_clickmap = infowindow;
            infowindow.setPosition(ev.latLng);
            infowindow.setContent(content);
            infowindow.open(map, this);
        };
    }
    
    function clickposCallback(uri, latLng) {
    	xhttp = new XMLHttpRequest();
    	xhttp.open("POST", uri);
    	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("lat=" + latLng.lat() + "&lng="  + latLng.lng());
    }

    
        google.maps.event.addDomListener(window, 'load', initialize_clickmap);
    