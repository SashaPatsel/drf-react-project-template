class Timer {
  constructor() {
    this.seconds = 0;
    this.minutes = 0;
    this.time = null;
  }

  start() {
    var timer = this
    this.time = setInterval(() => {
      timer.seconds++
      if (timer.seconds === 60) {
        timer.minutes++
        timer.seconds = 0
      }
    }, 1000);
  }

  stop() {
    clearInterval(this.time)
    console.log(`Query answered in ${this.minutes}: ${this.seconds}`)
  }

  reset() {
    this.seconds = 0
    this.minutes = 0
  }

}

export default Timer