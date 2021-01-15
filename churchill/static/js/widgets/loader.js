"use strict"

export class LoaderWidget {
  constructor () {
    this.ctl = document.getElementById("loader")
  }

  show() {
    this.ctl.classList.remove("d-none")
  }

  hide() {
    this.ctl.classList.add("d-none")
  }
}
