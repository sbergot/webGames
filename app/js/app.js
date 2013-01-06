'use strict';

angular.module('webGames', ['socket']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when(
	'/tictactoe',
	{templateUrl: 'partials/tictactoe.html', controller: MyCtrl1}
    );
    $routeProvider.otherwise({redirectTo: '/tictactoe'});
  }]);
