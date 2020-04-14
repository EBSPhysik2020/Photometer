var colors
var referenceMeasurements
var measurements

var broadcast

function getColors() {
  return colors
}

function getReferences() {
  return referenceMeasurements
}

function getMeasurements() {
  return measurements
}

function removeMeasurement(index) {
  index = index - 1
  if (measurements[index] == null) {
    return
  }
  console.log('Measurement #' + index + ' deleted.');
  measurements[index] = null
  broadcast('delete', index + 1)
}

function start(callback) {

  broadcast = callback

  var net = require('net')
  var server = net.createServer()

  console.log('Connector started.')

  server.on('connection', function(socket) {

    socket.on('data', function(data) {
      var params = data.split('/')
      var type = params[0]
      var parsedData

      switch (type) {

        case 'colors':
          parsedData = {
            notification: true,
            measurements: []
          }
          measurements = []
          var count = (params.length - 1) / 5
          for (var i = 0; i < count; i++) {
            var offset = (i * 5) + 1
            parsedData.measurements.push({
              r: Number(params[offset + 0]),
              g: Number(params[offset + 1]),
              b: Number(params[offset + 2]),
              waveLength: Number(params[offset + 3]),
              intensity: Number(params[offset + 4])
            })
          }
          colors = parsedData
          break


        case 'measurement-progress':
          parsedData = {
            type: params[1],
            progress: Number(params[2])
          }
          break


        case 'reference':
          measurements = []
          parsedData = {
            notification: true,
            concentration: Number(params[1]),
            measurements: []
          }
          for (var i = 0; i < colors.measurements.length; i++) {
            var offset = (i * 3) + 2
            parsedData.measurements.push({
              intensity: Number(params[offset + 0]),
              extinction: Number(params[offset + 1]),
              coefficient: Number(params[offset + 2])
            })
          }
          referenceMeasurements = parsedData
          break

        case 'measurements':
          parsedData = {
            notification: true,
            measurements: []
          }
          for (var i = 0; i < colors.measurements.length; i++) {
            var offset = (i * 3) + 1
            parsedData.measurements.push({
              intensity: Number(params[offset + 0]),
              extinction: Number(params[offset + 1]),
              concentration: Number(params[offset + 2])
            })
          }
          measurements.push(parsedData)
          break
      }

      broadcast(type, parsedData)

    })
    socket.setEncoding('utf8')
  })

  server.listen(5000)

}

module.exports = {
  start: start,
  removeMeasurement: removeMeasurement,
  getColors: getColors,
  getReferences: getReferences,
  getMeasurements: getMeasurements
}
