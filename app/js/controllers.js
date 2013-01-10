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
    
    var conn = socket.connect('tictactoe');
    $scope.play = function(cell) {
	var x = parseInt(cell[0]) - 1;
	var y = parseInt(cell[1]) - 1;
	$scope.grid[x][y].value = $scope.symbol;
	conn.emit("play", {fullGrid : $scope.grid, box : cell});
    }
    conn.on('connect', function() {$scope.status = "connected";});
    conn.on('getsymbol', function(data) {$scope.symbol = data.symbol;});
    conn.on('newturn', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });
    conn.on('replay', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });

}

function MainCtrl($scope, $cookies, socket, guid) {
    
    if ($cookies.player_id === undefined) {
	$cookies.player_id = guid();
    }
    $scope.playerName = "toto";
    $scope.player_id = $cookies.player_id;
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
