import { _ } from "./library/translate.js"

import { CenteredWidget } from "./widgets/centered.js"
import { LoaderWidget } from "./widgets/loader.js"

"user strict"

class App {
  constructor () {
    if (localStorage.getItem("token")) {
      this.token = localStorage.getItem("token")
    }
    if (localStorage.getItem("calendar")) {
      this.calendar = localStorage.getItem("calendar")
    }

    this.container = document.getElementById("container")

    this.loader = new LoaderWidget()
    this.centered = new CenteredWidget()

    this.update()
    this.checkMessages()
  }

  update() {
    fetch("/api/v1/profile/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + this.token
      },
      async: true,
    }).then(response => {
      this.loader.hide()
      if (response.status === 200) {
        response.json().then(data => {
          this.profile = data
          this.renderDashboard()
        })
        return
      }
      if (response.status === 401) {
        this.renderLogin()
        return
      }
      console.error("Error loading profile data")
    })
  }

  renderDashboard() {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById("t-dashboard").innerHTML,
    )({ profile: this.profile })

    if (!this.calendar) {
      fetch("/api/v1/shots/calendar/", {
        method: "get",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Token " + this.token
        },
        async: true,
      }).then((response) => {
        if (response.status === 200) {
          response.json().then(data => {
            this.calendar = data.results
            document.getElementById("calendar-container").innerHTML = Handlebars.compile(
              document.getElementById("t-calendar").innerHTML,
            )({ calendar: this.calendar })
          })
        }
      })
    }

    document.getElementById("show-add-shot-item-form").onclick = event => {
      this.container.innerHTML = Handlebars.compile(
        document.getElementById("t-add-shot-item").innerHTML
      )({ shots: this.profile.shots })

      document.getElementById("add-shot-item-form").onsubmit = event => {
        event.preventDefault()

        let formData = new FormData(event.currentTarget), data = {}

        formData.forEach((value, key) => data[key] = value)

        fetch("/api/v1/shots/item/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + this.token
          },
          body: JSON.stringify(data),
          async: true,
        }).then((response) => {
          if (response.status === 201) {
            this.update()
            return
          }
          alert("Can't add new shot, please try again later")
        })
      }

      document.getElementById("close-add-shot-item-form").onclick = event => {
        event.preventDefault()
        this.renderDashboard()
      }
    }
  }

  renderLogin() {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById("t-login").innerHTML
    )()

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

      fetch("/api/v1/user/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        async: true,
      }).then(response => {
        if (response.status === 201) {
          response.json().then(data => {
            localStorage.setItem("token", data["token"])
            this.token = data["token"]
            this.update()
          })
          return
        }
        alert("Can't login with provided email and password, please try again with different credentials")
      })
    }
  }

  renderRegistration() {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById("t-register").innerHTML
    )()

    document.getElementById("show-login-form").onclick = event => {
      this.renderLogin()
    }

    document.getElementById("register").onclick = event => {
      event.preventDefault()

      let data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      }

      fetch("/api/v1/user/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        async: true,
      }).then(response => {
        if (response.status === 201) {
          alert("Account created successfully, please check you email for verification link.")
          this.renderLogin()
          return
        }
        alert("Can't register with provided email and password, please try again with different credentials")
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
  Handlebars.registerHelper("translate", (string) => {
    return _(string)
  })

  let app = new App()

  document.getElementById("show-dashboard").onclick = event => {
    event.preventDefault()
    app.renderDashboard()
  }
})