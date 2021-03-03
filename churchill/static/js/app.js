import { Api } from "./library/api.js"
import { _ } from "./library/translate.js"
import { today, registerHandlebarsHelpers, installServiceWorker } from "./library/utils.js"

import { CenteredWidget } from "./widgets/centered.js"
import { LoaderWidget } from "./widgets/loader.js"

import { daysOfWeek } from "./const.js"

"user strict"

class App {
  constructor (api) {
    this.api = api

    if (localStorage.getItem("profile")) {
      this.profile = localStorage.getItem("profile")
    }
    if (localStorage.getItem("calendar")) {
      this.calendar = localStorage.getItem("calendar")
    }
    if (localStorage.getItem("shotList")) {
      this.shotList = localStorage.getItem("shotList")
    }

    this.container = document.getElementById("container")

    this.loader = new LoaderWidget()
    this.centered = new CenteredWidget()

    this.route()
    this.loader.hide()

    this.checkMessages()
  }

  route() {
    if (this.api.token) {
      if (this.profile) {
        this.renderDashboard()
      } else {
        this.update()
      }
    } else {
      this.renderLogin()
    }
  }

  update() {
    this.api.getProfile((data) => {
      this.profile = data
      this.renderDashboard()
    }, () => {
      this.renderLogin()
    })
  }

  render(template, data) {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById(template).innerHTML,
    )(data)
  }

  renderDashboard() {
    this.render("t-dashboard", { profile: this.profile })

    if (!this.calendar) {
      this.api.getCalendar((data) => {
        this.calendar = data
        this.renderCalendar()
      }, () => {
        console.error("Can't get calendar data")
      })
    } else {
      this.renderCalendar()
    }

    if (!this.shotList) {
      this.api.getShotList((data) => {
        this.shotList = data
        this.renderShotList()
      }, () => {
        console.error("Can't get shot list data")
      })
    } else {
      this.renderShotList()
    }

    document.getElementById("show-add-shot-item-form").onclick = event => {
      this.render("t-add-shot-item", { shots: this.profile.shots })

      document.getElementById("add-shot-item-form").onsubmit = event => {
        event.preventDefault()

        let formData = new FormData(event.currentTarget), data = {}
        formData.forEach((value, key) => data[key] = value)

        this.api.createShotItem(data, () => {
          this.update()
        }, () => {
          alert(_("Can't add new shot, please try again later"))
        })
      }

      document.getElementById("close-add-shot-item-form").onclick = event => {
        event.preventDefault()
        this.renderDashboard()
      }
    }

    this.showSettingsButton()

    document.getElementById("show-settings").onclick = event => {
      this.render("t-settings", { profile: this.profile, options: OPTIONS })

      document.getElementById("update-settings-form").onsubmit = event => {
        event.preventDefault()

        let formData = new FormData(event.currentTarget), data = {}
        formData.forEach((value, key) => data[key] = value)

        this.api.updateSettings(data, () => {
          this.update()
        }, () => {
          alert(_("Can't update your settings, please try again later"))
        })
      }

      document.getElementById("close-update-settings-form").onclick = event => {
        event.preventDefault()
        this.renderDashboard()
      }
    }
  }

  showSettingsButton() {
    document.getElementById("show-settings").classList.remove("hidden")
  }

  renderCalendar() {
    document.getElementById("calendar-container").innerHTML = Handlebars.compile(
      document.getElementById("t-calendar").innerHTML,
    )({ calendar: this.calendar, today: today(), daysOfWeek: daysOfWeek })
  }

  renderShotList() {
    let shotList = [], check = null,
      curr_created_at, check_created_at

    for (let i = 0; i < this.shotList.length; i++) {
      if (i > 0) {
        if (check === null) {
          check = this.shotList[i - 1]
          check["count"] = 1
        }

        curr_created_at = new Date(Date.parse(this.shotList[i]["created_at"]))
        check_created_at = new Date(Date.parse(check["created_at"]))
        if (
          curr_created_at.getDate() === check_created_at.getDate() &&
          curr_created_at.getMonth() === check_created_at.getMonth() &&
          this.shotList[i]["shot"]["id"] === check["shot"]["id"]
        ) {
          check["count"]++
        } else {
          shotList.push(check)
          check = null
        }
      }
    }

    document.getElementById("shot-list-container").innerHTML = Handlebars.compile(
      document.getElementById("t-shot-list").innerHTML,
    )({ shotList: shotList.slice(0, 12) })
  }

  renderLogin() {
    this.render("t-login")

    document.getElementById("show-registration-form").onclick = event => {
      this.renderRegistration()
    }

    this.centered.center(
      document.getElementById("login-form")
    )

    document.getElementById("login").onclick = event => {
      event.preventDefault()

      let data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      }

      this.api.login(data, () => {
        this.update()
      }, () => {
        alert(_("Can't login with provided email and password, please try again with different credentials"))
      })
    }
  }

  renderRegistration() {
    this.render("t-register")

    document.getElementById("show-login-form").onclick = event => {
      this.renderLogin()
    }

    document.getElementById("register").onclick = event => {
      event.preventDefault()

      let data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      }

      this.api.register(data, () => {
        alert(_("Account created successfully, please check you email for verification link."))
        this.renderLogin()
      }, () => {
        alert(_("Can't register with provided email and password, please try again with different credentials"))
      })
    }

    this.centered.center(
      document.getElementById("register-form")
    )
  }

  checkMessages() {
    if (MESSAGES.length) {
      let result = ""

      for (let i = 0; i < MESSAGES.length; i++) {
        result += MESSAGES[i]["message"] + "\n"
      }

      alert(result)
    }
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  registerHandlebarsHelpers()

  let api = new Api(),
    app = new App(api)

  document.getElementById("show-dashboard").onclick = event => {
    event.preventDefault()
    app.route()
  }
})
