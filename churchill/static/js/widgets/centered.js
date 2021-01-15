"use strict"

export class CenteredWidget {
  constructor () {
    let navbar = document.getElementById("navbar"),
      container = document.getElementById("container")

    this.navbar_height = navbar.offsetHeight
    this.container_padding = window.getComputedStyle(container).getPropertyValue("padding-left")
  }

  center(element) {
    element.style.top = ((window.innerHeight - element.offsetHeight) / 2) - this.navbar_height + "px"
    element.style.left = (window.innerWidth - element.offsetWidth) / 2  - this.container_padding + "px"
  }
}