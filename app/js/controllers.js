'use strict';

/* Controllers */

function ConnectionConfig($scope, conn) {
    conn.on('connect', function() {
	$scope.status = "connected";
    });
    conn.on('get-symbol', function(data) {
	$scope.symbol = data.symbol;
    });
    conn.on('get-session-id', function(data) {
	$scope.session_id = data.id;
    });
    conn.emit('register', {
	player_name : $scope.player_name,
	player_id : $scope.player_id,
	session_id : $scope.session_id
    });
}

function TictactoeCtrl($scope, socket, $routeParams) {
    $scope.status = "not connected";
    $scope.symbol = "unknown";
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
    ];
    var conn = socket.connect('tictactoe');
    ConnectionConfig($scope, conn);
    $scope.play = function(cell) {
	var x = parseInt(cell[0]) - 1;
	var y = parseInt(cell[1]) - 1;
	$scope.grid[x][y].value = $scope.symbol;
	conn.emit("play", {
	    box : cell,
	    symbol : $scope.symbol,
	    fullGrid : $scope.grid
	});
    };
    conn.on('play', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });
}

function MainCtrl($scope, $cookies, socket, guid) {
    if ($cookies.player_id === undefined) {
	$cookies.player_id = guid();
    }
    $scope.player_name = "toto";
    $scope.player_id = $cookies.player_id;
    $scope.new_id = function new_id() {$scope.player_id = guid();};
}

function LobbyCtrl($scope, socket) {
    var conn = socket.connect('lobby');
    conn.on('get_sessions', function(data) {$scope.sessions = data.sessions;});
    $scope.join = function(session_id) {
	conn.emit('join', {
	    player : $scope.player_id,
	    session_id : session_id
	});
    };
}

function footerCtlr($scope, version) {
    $scope.version = version;
}
