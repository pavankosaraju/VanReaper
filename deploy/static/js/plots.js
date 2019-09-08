$('.tabgroup > div').hide();
$('.tabgroup > div:first-of-type').show();
$('.tabs a').click(function(e){
  e.preventDefault();
    var $this = $(this),
        tabgroup = '#'+$this.parents('.tabs').data('tabgroup'),
        others = $this.closest('li').siblings().children('a'),
        target = $this.attr('href');
    others.removeClass('active');
    $this.addClass('active');
    $(tabgroup).children('div').hide();
    $(target).show();
  
})

var map;
  function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 49.2827, lng: -123.1207},
      zoom: 11
    });
  
  }

$('#property_form').on('submit',function(e){
     
    var area = document.getElementById('area').value;
    var interest = document.getElementById('interest').value;
    var pid = document.getElementById('pid').value;
    
    
    var input = {
        "area" : area,
        "interest" : interest,
        "pid" : pid        
    };
    
    $.ajax({
        url: "/property_predict",
        type: "POST",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(input),
        dataType:"json",
        success: function (response) {
           var space = " "  
           space = space.concat(response.price)
           space = space.concat(" millions")
           document.getElementById("message").innerHTML = space;
           var figure_1 = JSON.parse(response.graph_1); 
           var layout_1 = {
                title:'General Trend: ' + area,
                xaxis: {
                title: 'Year',
                showgrid: false,
                zeroline: false
              },
              yaxis: {
                title: 'Price in million',
                showline: false
              }
           
              };
           Plotly.newPlot('linegraph', figure_1,layout_1);
           if (response.graph_2 !== 'error') {
            var figure_2 = JSON.parse(response.graph_2); 
               var layout_2 = {
                title:'Property Trend: ' + pid,
                xaxis: {
                title: 'Year',
                showgrid: false,
                zeroline: false
              },
              yaxis: {
                title: 'Property price in million',
                showline: false
              }
              };
            Plotly.newPlot('usergraph', figure_2, layout_2);
            }
        }
    });
    e.preventDefault();
   // $('#property_form')[0].reset();

   
})

$('#recommendation_form').on('submit',function(e){
    
    var pid = document.getElementById('p_value').value;
    var bdrm = document.getElementById('bdrm').value;
    var bthrm = document.getElementById('bthrm').value;
    var sqrft = document.getElementById('sqrft').value;
    var fire = document.getElementById('fire').value;
    var features = document.getElementById('features').value;
    
    
    var input = {
        "pid" : pid,
        "bdrm" : bdrm,
        "bthrm" : bthrm,
        "sqrft" : sqrft,
        "fire" : fire,
        "features" : features
    };
    
    $.ajax({
        url: "/get_recommendation",
        type: "POST",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(input),
        dataType:"json",
        success: function (response) {
          var space = "$"  
          space = space.concat(response.price)
          document.getElementById("message_recommend").innerHTML = space;
          var figure_1 = JSON.parse(response.table_1); 
          var layout_1 = {
                title:'Recommended Property Listing',
                responsive: true,
                autosize: true,
                margin : {'l': 0, 'r': 0, 't': 0, 'b': 0},
                xaxis: {'automargin': true},
                yaxis: {'automargin': true}
              };
           Plotly.newPlot('table', figure_1,layout_1);
            
        var locations = response.locations
        var infowindow = new google.maps.InfoWindow();
        var marker, i;
        var bounds = new google.maps.LatLngBounds();
            for (i = 0; i < locations.length; i++) {  
              marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                map: map
              });
             bounds.extend(marker.getPosition());
             

              google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                  infowindow.setContent('Listing id : '+locations[i][0]+', \n'
                                       +'Price : '+locations[i][3]+', \n'
                                       +'Bed : '+locations[i][4]+', \n'
                                       +'Bath : '+locations[i][5]+',\n'
                                       +'Area Sqft : '+locations[i][6]+', \n'
                                       +'fireplaces : '+locations[i][7]+', \n'
                                       );
                  infowindow.open(map, marker);
                }
              })(marker, i));
                
           
            }
           
            
            map.fitBounds(bounds);
            map.panToBounds(bounds);
            }
    });
    e.preventDefault();
    //$('#recommendation_form')[0].reset();
    var $this = $('tab2'),
        tabgroup = '#'+$this.parents('.tabs').data('tabgroup'),
        others = $this.closest('li').siblings().children('a'),
        target = $this.attr('href');
    others.removeClass('active');
    $this.addClass('active');
    $(tabgroup).children('div').hide();
    $(target).show();
})




