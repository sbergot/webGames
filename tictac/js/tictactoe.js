$(function() {
    
var s = new io.connect('http://' + window.location.hostname + ':8001', {
            rememberTransport: false
        });

s.on('connect', function() {set_status("connected")})



function set_status(status) {
    $('#response').html =  "status: " + status;
}

function set_grid(grid) {
    var response = JSON.parse(req.responseText);
    set_status(response.status)
    for (var box in ttt.grid)
    {
	ttt.grid[box].innerHTML = response.grid[box];
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
    $('.box').html = '';
    set_status('start')
}

function initEvents() {
    for (var i in ttt.grid)
    {
    var box = ttt.grid[i];
    box.onclick = (function() {
        var id = box.id;
        return function() {
            var data = {grid : getJSONGrid(), box : id};
            s.emit('play', data, set_grid)
        };
    })();
    }
    document.getElementById("reset").onclick = s.emit('reset', {}, reset)
}

initEvents();
});
