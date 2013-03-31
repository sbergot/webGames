'use strict';

/* Controllers */

function ConnectionConfig($scope, conn, session_id) {
    conn.on('connect', function() {
        $scope.status = "connected";
    });
    conn.on('get-symbol', function(data) {
        $scope.symbol = data.symbol;
    });
    conn.emit('checkin', {
        player_name : $scope.player_name,
        player_id : $scope.player_id,
        session_id : session_id
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
            session_id : session_id
        });
    };
    $scope.create_game = function(game_name) {
        conn.emit('create_game', {
            player_id : $scope.player_id,
            game_name : game_name
        });
    };
}

function footerCtlr($scope, version) {
    $scope.version = version;
}
