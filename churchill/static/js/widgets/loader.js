"use strict"

export class LoaderWidget {
  constructor () {
    this.ctl = document.getElementById("loader")
  }

  show() {
    this.ctl.classList.remove("hidden")
  }

  hide() {
    this.ctl.classList.add("hidden")
  }
}
