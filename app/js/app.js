'use strict';

angular.module('webGames', ['socket', 'infos']).
  config(['$routeProvider', function($routeProvider) {
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
	    templateUrl: 'partials/tictactoe.html',
	    controller: TictactoeCtrl
	}
    );
    $routeProvider.otherwise({redirectTo: '/lobby'});
  }]);
