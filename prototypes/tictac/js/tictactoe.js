$(function() {
    
var s = new io.connect('http://' + window.location.hostname + ':8001', {
            rememberTransport: false
        });

s.on('connect', function() {set_status("connected")});
s.on('getsymbol', function(data) {$("#symbol").html(data.symbol)});
s.on('newturn', function(data) {
    $('#response').html(data.status);
    set_grid(data.grid);
});
s.on('replay', function(data) {
    $('#response').html(data.status);
    set_grid(data.grid);
});



function set_status(status) {
    $('#response').html("status: " + status);
}

function set_grid(grid) {
    for (var box in ttt.grid)
    {
	ttt.grid[box].innerHTML = grid[box];
    }
}

function getJSONGrid() {
    var res = {};
    for (var i in ttt.grid)
    {
	res[i] = ttt.grid[i].innerHTML;
    }
    return res;
}

var ttt = {
    grid : (function() {
    var res = {};
    var boxes = document.getElementsByTagName("td");
    for (var i = 0; i < 9; i++)
    {
        var box = boxes[i];
        var id = box.id;
        res[id] = box;
    }
    return res
    })()
}

function reset() {
    $('.box').html('');
    set_status('start');
}

function initEvents() {
    for (var i in ttt.grid)
    {
	var box = ttt.grid[i];
	$(box).click((function() {
            var id = box.id;
            return function() {
		var data = {fullGrid : getJSONGrid(), box : id};
		s.emit('play', data);
            };
	})());
    }
    $("#reset").click(function() {s.emit('resetGrid', {name : 'toto'});});
    $("#symbol").html("no symbol");
    //$("#symbol").click(function() {s.emit});
    $("#response").html("no status");
}

initEvents();
});
