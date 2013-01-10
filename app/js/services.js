'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('infos', []).
  value('version', '0.1').
    factory('guid', function() {
	function guid() {
	    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
		    /[xy]/g,
		function(c) {
		    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
		    return v.toString(16);
		}
	    );
	}
	return guid; 
    });
