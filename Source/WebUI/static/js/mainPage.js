var mainColor = "#00CC00";
$(document).ready(function(){
  namespace = '/test';
  var currentGrip = -1;
  var gripToTrain = -1;
  var handLR = "L-";
  const NUM_OF_MOVES = 15
  var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
  // Dialog
  var modal = document.getElementById('trainingDialog');
  // Open Dialog Button
  var btn = document.getElementById("startButton");
  // CLose Dialog Button
  var span = document.getElementsByClassName("close")[0];
  //Next Button
  var nextBut = document.getElementById("next");

  var trainPic = document.getElementById("trainPic");

  var handChoosing = document.getElementById("handSwitch");

  socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
  });
  socket.on('disconnect', function() {
    $('#log').append('<br>Disconnected');
  });
  socket.on('my response', function(msg) {
    $('#response').empty();
    $('#response').append(msg.data);
  });
  socket.on('grip receive', function(msg) {
    var elem = [0];
    for (var i = 0; i < NUM_OF_MOVES; i++) {
      elem[i] = document.getElementById("mvDataBar" + i);
      if (i == msg.data) {
        elem[i].style.background = "#FF4500";
      } else {
        elem[i].style.background = mainColor;
      }
    }
    var predictPic = document.getElementById("predictPic");
    predictPic.src = "media/images/" + handLR + msg.data + ".png"
  });
  socket.on('time elapsed', function(msg) {
    $('#time_elapsed').empty();
    $('#time_elapsed').append('Time Elapsed: ' + msg.data);
  });
  socket.on('train grip', function(msg) {
    currentGrip = msg.data;
    trainPic.src = "media/images/" + handLR + msg.data + ".png"
    $('#response').empty();
    $('#trainButton').empty();
    $('#deleteButton').empty();
    $('#trainButton').append('Train Grip ' + msg.data);
    $('#deleteButton').append('Delete All Data Grip ' + msg.data);
  });
  socket.on('move data', function(msg) {
    var elem = [0];
    var mvData = msg.data.slice(1, -1).split(',');
    for (var i = 0; i < NUM_OF_MOVES; i++) {
      elem[i] = document.getElementById("mvDataBar" + i);
      elem[i].style.width = mvData[i]*0.885 + '%';
      elem[i].innerHTML = mvData[i] * 1 + '%';
    }
  });
  $('#disconnect').click(function(event) {
    socket.emit('disconnect request');
    return false;
  });
  $('#trainButton').click(function(event) {
    socket.emit('button pressed', currentGrip);
    return false;
  });
  $('#deleteButton').click(function(event) {
    socket.emit('button pressed', 'D' + currentGrip);
    return false;
  });
  $('#startButton').click(function(event) {
    currentGrip = -1;
    socket.emit('button pressed', 'start');
    return false;
  });
  $('#next').click(function(event) {
    if (currentGrip < NUM_OF_MOVES - 1) {
      socket.emit('button pressed', -1);
    }
    return false;
  });

  // When the user clicks the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
    $('#next').empty();
    $('#next').append('Next');
  }
  // When the user click the button, move to next grip
  nextBut.onclick = function() {
    if (currentGrip == NUM_OF_MOVES - 2) {
      $('#next').empty();
      $('#next').append('Complete!');
    } else if (currentGrip >= NUM_OF_MOVES - 1) {
      modal.style.display = "none";
    }
  }
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == dialog) {
      modal.style.display = "none";
    }
  }

  $("button").hover(function(){
     $(this).not("button.active").css("background-color", mainColor);
     $(this).not("button.active").css("color", "#FFFFFF");
  });

  $("button").mouseleave(function(){
    $(this).not("button.active").css("background-color", "#f1f1f1");
    $(this).not("button.active").css("color", "#555555");
  });

  handChoosing.onclick = function() {
    if (handLR == "L-") {
      handLR = "R-";
      mainColor = "#2E8DEF"
    } else if (handLR == "R-") {
      handLR = "L-";
      mainColor = "#00CC00"
    }
    $("button.active").css("background-color", mainColor);
    $("#time_elapsed").css("color", mainColor);
  }
});

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  $("button.tablinks").not("button.active").css("background-color", "#f1f1f1");
  $("button.tablinks").not("button.active").css("color", "#555555");
  $("button.active").css("background-color", mainColor);
}
