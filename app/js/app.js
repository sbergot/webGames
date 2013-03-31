'use strict';

angular.module('webGames', ['socket', 'infos', 'ngCookies']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when(
	'/lobby',
	{
	    templateUrl: 'partials/lobby.html',
	    controller: LobbyCtrl
	}
    );
    $routeProvider.when(
	'/tictactoe/session/:sessionId',
	{
	    templateUrl: 'partials/tictactoe.html',
	    controller: TictactoeCtrl
	}
    );
    $routeProvider.otherwise({redirectTo: '/lobby'});
  }]);
