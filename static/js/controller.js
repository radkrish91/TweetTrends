
angular.module('twitApp').controller('homeController', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog) {
		
		var links = new google.maps.Data();
		
		console.log("hello");
		var MAP_CENTER = new google.maps.LatLng(11.770570, -2.988281); //position that the main map centers on
		var MINIMUM_ZOOM = 2; //The minimum zoom level a user can zoom out
		var mapOptions = {
			  center: MAP_CENTER,
			  zoom: MINIMUM_ZOOM,
			  mapTypeId: google.maps.MapTypeId.ROADMAP,
			  disableDefaultUI:true,
			  mapTypeControl: true,
			  mapTypeControlOptions: {
				  style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
				  position: google.maps.ControlPosition.TOP_CENTER
			  },
			  streetViewControl: false,
			  streetViewControlOptions: {
				  position: google.maps.ControlPosition.TOP_CENTER
			  }
			};
		$scope.map_canvas = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
		
		$scope.availableOptions= [{id: '1', name: 'hillary'}, {id: '2', name: 'trump'}, {id: '3', name: 'patriots'}, {id: '4', name: 'clinton'}, {id: '5', name: 'giants'}, {id: '6', name: 'jets'}, {id: '7', name: 'football'}, {id: '8', name: 'mufc'}, {id: '9', name: 'voice'}, {id: '10', name: 'coyg'}];

		$scope.items = [
		{
			'image1' : '/static/img/twitter-neutral.png',
			'name1' : 'neutral',
			'image2' : '/static/img/twitter-negative.png',
			'name2' : 'negative',
			'image3' : '/static/img/twitter.png',
			'name3' : 'positive'
		}
		];

		 $scope.hasChanged = function() {
			 var search_key = {"search_key" : $scope.selectedKeyword};
			 map_damage = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
			 document.getElementById("map_canvas").style.display = "inline-block";
			 links.setMap(null);
			 links =  new google.maps.Data({map:map_damage});
			 console.log(search_key);
			 $.ajax({
	            url: '/search',
	            data: search_key,
	            type: 'GET',
			 	success : function(data) {
				 	var latitudes = JSON.parse(JSON.stringify(data.latitude));
					var longitudes = JSON.parse(JSON.stringify(data.longitude));
					var text = JSON.parse(JSON.stringify(data.text));
					var name = JSON.parse(JSON.stringify(data.name));
					var sentiment = JSON.parse(JSON.stringify(data.sentiment));

					for(i=0; i<latitudes.length; i++) {
							var position = new google.maps.LatLng(latitudes[i], longitudes[i]);
							var image = null
							switch(sentiment[i]) {
								case 'neutral':
									image = '/static/img/twitter-neutral.png';
									break;
								case 'negative':
									image = '/static/img/twitter-negative.png';
									break;
								case 'positive':
									image = '/static/img/twitter.png';
									break;
								default:
									image = '/static/img/twitter.png';
									break;
							}

							var image = new google.maps.MarkerImage(
								image,
								null,
								null,
								null,
								new google.maps.Size(21, 21));
							
							marker = new google.maps.Marker({
								position: position,
								map: map_damage,
								title: "Tweet"
							});

							marker.setIcon(image);
							
							var contentString = '<div id = "content">' +
							'<div id="siteNotice">'+
							  '</div>'+
							  '<h4 id="firstHeading" class="firstHeading">' + name[i] + '</h4>'+
							  '<div id="bodyContent">'+
							  '<p><b>Tweet : </b>' + text[i] + '</p>'+
							  '</div>'+
							  '</div>';

							var infowindow =  new google.maps.InfoWindow({
								content: ''
							});
							bindInfoWindow(marker, map_damage, infowindow, contentString);
						}
						function bindInfoWindow(marker, map, infowindow, html) { 
							google.maps.event.addListener(marker, 'mouseover', function() { 
								infowindow.setContent(html); 
								infowindow.open(map, marker); 
							});
							google.maps.event.addListener(marker, 'mouseout', function() { 
								infowindow.close(); 
							});
						}
				 },
			 	 error : function(data) {
			 		console.log("error");
		 			console.log(data);
		 		 }

			});
		}
   }]);
