'use strict';

/* Controllers */


function TictactoeCtrl($scope, socket) {
    $scope.status = "not connected";
    $scope.symbol = "x";
    socket.on('connect', function() {$scope.status = "connected";});
}


function footerCtlr($scope, version) {
    $scope.version = version;
}
