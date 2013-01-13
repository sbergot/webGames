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
		  server[name](data);
	      }
	  };
      }
      function get_socket(socket) {
	  return {
	      on: function (eventName, callback) {
		  socket.on(eventName, function () {  
		      var args = arguments;
		      $rootScope.$apply(function () {
			  callback.apply(socket, args);
		      });
		  });
	      },
	      emit: function (eventName, data, callback) {
		  socket.emit(eventName, data, function () {
		      var args = arguments;
		      $rootScope.$apply(function () {
			  if (callback) {
			      callback.apply(socket, args);
			  }
		      });
		  })
	      }
	  };
      };
      return {
	  connect : function(name) {
	      if (sockets[name] === undefined) {
		  sockets[name] = spawn_connection(name);
	      }
	      return get_socket(sockets[name]);
	  },
	  server : server
      }
  });
