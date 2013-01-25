'use strict';

angular.module('webGames', ['socket', 'infos', 'ngCookies']).
  config(['$routeProvider', function($routeProvider) {
      function guid() {
	  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
		  /[xy]/g,
	      function(c) {
		  var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
		  return v.toString(16);
	      }
	  );
      }
    $routeProvider.when(
	'/lobby',
	{
	    templateUrl: 'partials/lobby.html',
	    controller: LobbyCtrl
	}
    );
    $routeProvider.when(
	'/tictactoe',
	{
	    redirectTo: '/tictactoe/' + guid()
	}
    );
    $routeProvider.when(
	'/tictactoe/:id',
	{
	    templateUrl: 'partials/tictactoe.html',
	    controller: TictactoeCtrl
	}
    );
    $routeProvider.otherwise({redirectTo: '/lobby'});
  }]);
