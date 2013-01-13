'use strict';

describe('TictactoeCtrl', function(){
    var tic;
    var scope;
    var socket;

    beforeEach(module('TestSocket'));
    beforeEach(inject(function($rootScope, socket){
	scope = $rootScope.$new();
	socket.server.play = function() {};
	tic = new TictactoeCtrl(scope, socket);
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
	scope.play("11");
	expect(scope.grid[0][0].value).toEqual("x");
	scope.play("23");
	expect(scope.grid[1][2].value).toEqual("x");
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
    var lobby, scope;

    beforeEach(function(){
	scope = {};
	lobby = new LobbyCtrl(scope);
    });

    it('should fetch the list of games', function(){
	expect(scope.games).toEqual([
	    { host :"toto"},
	    { host :"tata"}
	]);
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
