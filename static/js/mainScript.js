var twitApp = angular.module('twitApp', ['ui.router', 'ngMaterial', 'ngMessages', 'ngRoute', 'ngSanitize', 'ngMdIcons']);
   
twitApp.config(function($stateProvider, $urlRouterProvider) {
        
		$urlRouterProvider.otherwise('/home');
		
		$stateProvider
        
        // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/home',
            views: {
			'main@': {
			  templateUrl: './static/pages/home.html',
			  controller: 'homeController'
			}
			},
			data: {
                displayName: 'Home'
            }
        })
    });
	
	

	
	
	
