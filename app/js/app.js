'use strict';

angular.module('webGames', ['socket', 'infos']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when(
	'/tictactoe',
	{
	    templateUrl: 'partials/tictactoe.html',
	    controller: TictactoeCtrl
	}
    );
    $routeProvider.otherwise({redirectTo: '/tictactoe'});
  }]);
