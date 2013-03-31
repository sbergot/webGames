'use strict';

/* Controllers */

function ConnectionConfig($scope, conn, session_id) {
    conn.on('connect', function() {
        $scope.status = "connected";
    });
    conn.on('get-symbol', function(data) {
        $scope.symbol = data.symbol;
    });
    conn.on('get-player-list', function(data) {
        $scope.players = data.players;
    });
    conn.emit('checkin', {
        player_name : $scope.player_name,
        player_id : $scope.player_id,
        session_id : session_id
    });
}

function TictactoeCtrl($scope, socket, $routeParams, $location) {
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
    ConnectionConfig($scope, conn, $routeParams.sessionId);
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
    $scope.quit = function() {
	conn.emit("quit");
	$location.path("/lobby");
    };
    conn.on('play', function(data) {
        $scope.status = data.status;
        $scope.grid = data.grid;
    });
}

function MainCtrl($scope, $cookies, socket, guid) {
    function new_name() {
	return "toto du " + Math.floor(Math.random()*101);
    }
    if (!$cookies.player_id) {
	$cookies.player_id = guid();
    }
    if ($cookies.player_name) {
	$scope.player_name = $cookies.player_name;
    } else {
	$scope.player_name = new_name();
    }
    $scope.save_name = function() {
	$cookies.player_name = $scope.player_name;
    };
    $scope.player_id = $cookies.player_id;
    $scope.new_id = function new_id() {$scope.player_id = guid();};
    $scope.games = ["tictactoe"];
}

function LobbyCtrl($scope, $location, socket) {
    var conn = socket.connect('lobby');
    conn.on('get_sessions', function(data) {$scope.sessions = data.sessions;});
    conn.on('get-session-access', function(data) {
        $location.path('/' + data.name + '/session/' + data.id);
    });
    $scope.join_game = function(session_id) {
        conn.emit('join_game', {
            player_id : $scope.player_id,
            session_id : session_id,
	    player_name : $scope.player_name
        });
    };
    $scope.create_game = function(game_name) {
        conn.emit('create_game', {
            player_id : $scope.player_id,
            game_name : game_name,
	    player_name : $scope.player_name
        });
    };
}

function footerCtlr($scope, version) {
    $scope.version = version;
}
