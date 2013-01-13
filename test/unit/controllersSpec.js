'use strict';

/* jasmine specs for controllers go here */

describe('TictactoeCtrl', function(){
    var tic;
    var scope = {};
    var socket = {
	connect : function(name) {
	return {
	    on : function() {},
	    emit : function() {}
	};
	}
    };

    beforeEach(function(){
	tic = new TictactoeCtrl(scope, socket);
    });


    it('should ....', function() {
	//spec body
    });
});


describe('MainCtrl', function(){
    var main;
    var scope = {};
    var socket = {
	connect : function(name) {
	return {
	    on : function() {},
	    emit : function() {}
	};
	}
    };
    var cookies = {};
    var guid = function() {return "toto";};


    beforeEach(function(){
	main = new MainCtrl(scope, cookies, socket, guid);
    });


    it('should ....', function() {
	//spec body
    });
});
