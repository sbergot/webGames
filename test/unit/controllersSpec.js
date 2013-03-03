'use strict';

beforeEach(module('TestSocket'));
describe('TictactoeCtrl', function(){
    var tic;
    var scope;
    var socket_mock;


    beforeEach(inject(function($rootScope, socket){
	scope = $rootScope.$new();
	socket.server_on('play', function() {});
	tic = new TictactoeCtrl(scope, socket, {id : "toto"});
	socket_mock = socket;
    }));

    it('should set the grid', function() {
	expect(scope.grid).toEqual([
	    [{coord : "11", value : ""},
	     {coord : "12", value : ""},
	     {coord : "13", value : ""}],
	    [{coord : "21", value : ""},
	     {coord : "22", value : ""},
	     {coord : "23", value : ""}],
	    [{coord : "31", value : ""},
	     {coord : "32", value : ""},
	     {coord : "33", value : ""}]
	]);
    });

    it('should provide a play function', function() {
	scope.symbol = "x";
	scope.play("11");
	expect(scope.grid[0][0].value).toEqual("x");
	scope.play("23");
	expect(scope.grid[1][2].value).toEqual("x");
    });

    it('should connect to tictactoe', function() {
	expect(socket_mock.sockets.tictactoe).toBeTruthy();
    });

    it('should accept a symbol', function() {
	socket_mock.server_emit('tictactoe',
				'get-symbol',
				{symbol : 'toto'});
	expect(scope.symbol).toEqual("toto");
    });
});


describe('MainCtrl', function(){
    var main, scope, cookies;
    var socket = {
	connect : function(name) {
	return {
	    on : function() {},
	    emit : function() {}
	};
	}
    };
    var guid = function() {return "myid";};


    beforeEach(function(){
	scope = {};
	cookies = {};
	main = new MainCtrl(scope, cookies, socket, guid);
    });


    it('should set a player id', function() {
	expect(scope.player_id, "myid");
    });

    it('should set a player name', function() {
	expect(scope.player_name, "toto");
    });

});

describe('LobbyCtrl', function(){
    var lobby, scope, socket_mock;


    beforeEach(inject(function($rootScope, socket){
	scope = $rootScope.$new();
	socket_mock = socket;
	lobby = new LobbyCtrl(scope, socket);
    }));

    
    it('should accept the game session list', function() {
	var sessions = [{game : 'tictactoe', id : 'toto'}];
	socket_mock.server_emit('lobby',
				'get_sessions',
				{sessions : sessions});
	expect(scope.sessions).toEqual(sessions);
    });
});

describe('footerCtlr', function(){
    var footer, scope, version;
    
    beforeEach(function(){
	scope = {};
	version = 'myversion'
	footer = new footerCtlr(scope, version);
    });

    it('should set the version variable', function(){
	expect(scope.version).toEqual('myversion');
    });
});
