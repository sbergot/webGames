'use strict';

/* Controllers */


function TictactoeCtrl($scope) {
    $scope.status = "not connected";
    $scope.symbol = "x";
}


function footerCtlr($scope, version) {
    $scope.version = version;
}
