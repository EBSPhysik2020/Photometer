
var express = require('express')
var socket = require('socket.io')
var connector = require('./photometerConnector.js')

var callback = function(type, data) {
  io.sockets.emit(type, data)
}

//app setup
var app = express()
var server = app.listen(52525, function(socket) {
    console.log('Listening for requests on port 52525.')
    connector.start(callback)
})

//static files
app.use(express.static('public'))

//socket setup
var io = socket(server)

io.on('connection', function(socket) {
  console.log('[Clients] new client connected. ' + socket.id)
  socket.on('disconnect', function() {
    console.log('[Clients] client disconnected. ' + socket.id);
  })

  socket.on('delete', function(index) {
    connector.removeMeasurement(index)
  })

  var colors = connector.getColors()
  if (colors != null) {
    colors.notification = false
    socket.emit('colors', colors)
  }
  var references = connector.getReferences()
  if (references != null) {
    references.notification = false
    socket.emit('reference', references)
  }

  var measurements = connector.getMeasurements()
  if (measurements != null) {
    measurements.forEach((measurement, i) => {
      if (measurement != null) {
        measurement.notification = false
      }
      socket.emit('measurements', measurement)
    });
  }
})
