class MeasurementChart {

  constructor(element) {
    Chart.defaults.global.defaultFontFamily = 'Raleway'
    this.chart = new Chart(element.getContext('2d'), {
        type: 'scatter',
        data: {
            datasets: []
        },
        options: {
            scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: true
                  },
                  scaleLabel: {
                    display: true,
                    labelString: 'Extinktion',
                    padding: 0
                  }
                }],
                xAxes: [{
                    ticks: {
                      beginAtZero: true
                    },
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                      display: true,
                      labelString: 'Konzentration (g/l)'
                    }
                }]
            }
        }
    })
  }

  addColor(color) {
    var colorString = color.r + ', ' + color.g + ', ' + color.b
    this.chart.data.datasets.push({
      label: color.waveLength + ' nm',
      borderColor: 'rgb(' + colorString + ')',
      backgroundColor: 'rgba(0, 0, 0, 0)',
      borderWidth: 1,
      showLine: true,
      cubicInterpolationMode: "monotone",
      spanGaps: true,
      data: []
    })
    this.chart.update()
  }

  addMeasurement(color, measurement) {
    if (measurement == null) {
      return
    }
    var dataPoint = {x: measurement.concentration, y: measurement.extinction}
    var dataArray = this.chart.data.datasets[color].data
    var inserted = false
    for (var i = 0; i < dataArray.length; i++) {
      if (dataArray[i] == null) {
        continue
      }
      if (dataArray[i].x > dataPoint.x) {
        dataArray.splice(i, 0, dataPoint)
        inserted = true
        break
      }
    }
    if (!inserted) {
      dataArray.push(dataPoint)
    }
    this.chart.update()
  }

  hideMeasurement(color, concentration) {
    this.chart.data.datasets[color].data.forEach((measurement, index) => {
      if (measurement != null && measurement.x == concentration) {
        this.chart.data.datasets[color].data[index] = null
      }
    })
    this.chart.update()
  }

  removeMeasurements() {
    for (var color = 0; color < this.chart.data.datasets.length; color++) {
      this.chart.data.datasets[color].data = []
    }
    this.chart.update()
  }

  reset() {
    this.chart.data.datasets = []
    this.chart.update()
  }

}
