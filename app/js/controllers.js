'use strict';

/* Controllers */


function TictactoeCtrl($scope, socket) {
    $scope.status = "not connected";
    $scope.symbol = "x";
    $scope.grid = [
	[{coord : "11", value : ""},
	 {coord : "12", value : ""},
	 {coord : "13", value : ""}],
	[{coord : "21", value : ""},
	 {coord : "22", value : ""},
	 {coord : "23", value : ""}],
	[{coord : "31", value : ""},
	 {coord : "32", value : ""},
	 {coord : "33", value : ""}]
    ]
    $scope.play = function(cell) {
	var x = parseInt(cell[0]) - 1;
	var y = parseInt(cell[1]) - 1;
	$scope.grid[x][y].value = $scope.symbol;
	socket.emit("play", {fullGrid : $scope.grid, box : cell});
    }
    socket.on('connect', function() {$scope.status = "connected";});
    socket.on('getsymbol', function(data) {$scope.symbol = data.symbol;});
    socket.on('newturn', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });
    socket.on('replay', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });

}

function MainCtrl($scope) {
    $scope.playerName = "toto";
}

function LobbyCtrl($scope) {
    $scope.games = [
	{ host :"toto"},
	{ host :"tata"}
    ];
}

function footerCtlr($scope, version) {
    $scope.version = version;
}
