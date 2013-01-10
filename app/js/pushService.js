'use strict';

angular.module('socket', []).
  factory('socket', function ($rootScope) {
      function spawn_connection(name) {
	  return new io.connect(
	      'http://' + window.location.hostname + ':8001/' + name,
	      {rememberTransport: false}
	  );
      }
      var sockets = {};
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
	  }
      }
  });
