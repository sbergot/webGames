'use strict';

angular.module('TestSocket', []).
  factory('socket', function ($rootScope) {
      var sockets = {};
      var server = {};
      function spawn_connection() {
	  var events = {};
	  return {
	      on : function(name, callback) {
		  events[name] = callback;
	      },
	      emit : function(name, data) {
		  if (server[name]) {
		      server[name](data);
		  }
	      },
	      events : events
	  };
      }
      return {
	  connect : function(name) {
	      if (sockets[name] === undefined) {
		  sockets[name] = spawn_connection(name);
	      }
	      return sockets[name];
	  },
	  server : server,
	  sockets : sockets,
	  server_emit : function(connection, event, data) {
	      //if (sockets[connection] && sockets[connection][event]) {
		  sockets[connection].events[event](data);
	      //}
	  },
	  server_on : function(event, callback) {
	      server[event] = callback;
	  }
      }
  });
