// Things to do

// sendField. This will recieve the field that has been used for the trump card
// and then call castFields, castRndWin, also check if the game is over
// (someone has all of the cards, or everyone else has no cards.)

// We need to deal with players who have already run out of cards in games with
// more than 2 players. I imagine removing elements from the list that do not
// meet the requirement of cards could be enough, or simple check if their queue
// is empty before sending the next card.

// Returns an array of Objects with Card Data.
// Usage `getCards();`
// "use strict";
var get = require('./get.js');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var users = {} //socket.id -> groupname
var groups = {} //groupname -> [usernames]
var readies = {}

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

function severityConvert(x){
    var severityMap = {slight : 1, serious : 2, fatal : 3}
    return severityMap[x];
}
function weatherConvert(x){
	var weatherMap = {"Fine no high winds" : 0, "Raining no high winds" : 1, "Fine + high winds" : 2, "Raining + high winds" : 3, "Snowing no high winds" : 4}
    return weatherMap[x];
}
function lightConvert(x){
	var lightMap = {"Daylight" : 0, "Darkness - lights lit" : 1, "Darkness - lighting unknown" : 2, "Darkness - lights unlit" : 3}
	return lightMap[x];
}
function id(x){
	return x
}

var mapMap = {"Accident severity" : severityConvert, "Number of vehicles" :id, "Number of casualties" : id, "Speed limit" : id, "Light conditions" : lightConvert, "Weather conditions" : weatherConvert}

// Map of User Names to Session ID
var userToId = {};
// 
var cards = {};
// Cards that have been played in this game
var turnCards = [];


io.on('connection', function(socket){

  socket.on('join', function (data) {
    users[socket.id] = data;
    userToId[data.user] = socket.id;
    // cards = ANTHONY GIVE ME SOME CARDS!!!!
    // console.log(socket);
    // users.push(socket.id);
    // users.push(data.token);
    socket.join(data.token);
    if (groups[data.token]) groups[data.token].push(data.user);
    else groups[data.token] = [data.user];
    console.log(groups[data.token]);
  });

  //Figure out who won the previous round. The cards can once again be checked
  socket.on('sendField', function (data) {
    io.sockets.in(data.token).emit('castField', data.field);
    var max = 0;
    console.log(turnCards);
    for (var i = 0; i < turnCards.length; i++) {
      var x = mapMap[data.field](turnCards[i].card[data.field]);
      console.log(data.field);
      console.log(turnCards[i].card[data.field], turnCards[i].user);
      if (x >= max) {
        max = x;
        console.log(x);
        var rndWin = turnCards[i].user;
      }
    }
    io.sockets.in(data.token).emit('castCards', {cards:turnCards, rndWinner:rndWin});
    for (var i = 0; i < turnCards.length; i++) {
      cards[rndWin].push(turnCards[i].card);
    }
    turnCards = [];
    var gameWin = true;
    for (var i = 0; i < groups[data.token].length; i++) {
      if (groups[data.token][i] != rndWin) {
        if (cards[groups[data.token][i]].length > 0) {
          gameWin = false;
          console.log("we should be here");
          //break;
        } else {
          console.log("we should not be here");

          if (groups[data.token][i]) {
            io.sockets.in(data.token).emit('chat message', groups[data.token][i] + " is out.");
            groups[data.token][i] = undefined;
          }
        }
      }
    }
    if (gameWin) {
      io.sockets.in(data.token).emit('win', rndWin); //The user that won.
    } else {
      setTimeout(function(){
	if (!turnCards) turnCards = []; //TODO THIS IS A PROBLEM FIX ME NOW
        for (var i = 0; i < groups[data.token].length; i++) {
          if (groups[data.token][i]) {
            console.log(groups[data.token][i] + " casting " + cards[groups[data.token][i]][0]);
            console.log(cards[groups[data.token][i]][0]);
          io.to(userToId[groups[data.token][i]]).emit('castCard', cards[groups[data.token][i]][0]);
          turnCards.push({card:cards[groups[data.token][i]].shift(), user:groups[data.token][i]});
        }
        }
      }, 50);
    }
  });
  //
  // function getCards(i) {
  //   if (i == 0) {
  //     return [{id:'a', field1:5, field2:6}, {id:'a', field1:5, field2:6}]; //Player 1
  //   }
  //   return [{id:'a', field1:4, field2:4}, {id:'a', field1:4, field2:4}]; //Player 2
  // }

  socket.on('ready', function (data) {
    console.log("Called");
    console.log(socket.id);
    if (readies[data.token]) readies[data.token].push(data.user);
    else readies[data.token] = [data.user];
    io.sockets.in(data.token).emit('chat message', data.user + " is now ready.");
    if (readies[data.token].length == groups[data.token].length && groups[data.token].length > 1) {
      io.sockets.in(data.token).emit('gameInit', {numPlayers:groups[data.token].length, first:data.user});
      console.log("Cast");
      for (var i = 0; i < groups[data.token].length; i++) {
        cards[groups[data.token][i]] = get.getCards(10);//getCards(); //Stand in
        console.log("Cast (inner) " + groups[data.token][i]);
        if (!userToId[groups[data.token][i]]) console.log("Yeah well of course this was it...");
        io.to(userToId[groups[data.token][i]]).emit('castCard', cards[groups[data.token][i]][0]);
        turnCards.push({card:cards[groups[data.token][i]].shift(), user:groups[data.token][i]});
      }
      // io.sockets.in(data.token).emit('castCards', groups[data.token].length);
    }
  });

  socket.on('disconnect', function(data) {
    if (users[socket.id]) {
      var index = groups[users[socket.id].token].indexOf(users[socket.id].user);
      userToId[data.user] = undefined;
      groups[users[socket.id].token].splice(index, 1);
      users[socket.id] = undefined;
    }
  });

  socket.on('chat message', function(data){
    io.sockets.in(data.token).emit('chat message', data.user + ": " + data.message);
  });
});

http.listen(8080, function(){
  console.log('listening on *:8080');
});
