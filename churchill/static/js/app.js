import { _ } from "./library/translate.js"

import { CenteredWidget } from "./widgets/centered.js"
import { LoaderWidget } from "./widgets/loader.js"

"user strict"

class App {
  constructor () {
    this.container = document.getElementById("container")

    this.loader = new LoaderWidget()
    this.centered = new CenteredWidget()

    this.update()
    this.checkMessages()
  }

  update() {
    fetch("/api/v1/profile/").then((response) => {
      this.loader.hide()
      if (response.status === 200) {
        this.profile = response.data
        this.renderDashboard()
        return
      }
      if (response.status === 403) {
        this.renderLogin()
        return
      }
      console.error("Error loading profile data")
    })
  }

  renderDashboard() {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById("t-dashboard").innerHTML,
      { data: { profile: this.profile }}
    )()


    document.getElementById("show-add-shot-item-form").onclick = (event) => {
      this.container.innerHTML = Handlebars.compile(
        document.getElementById("t-add-shot-item").innerHTML
      )()

      document.getElementById("add-shot").onclick = (event) => {
        event.preventDefault()

        let data = { id: document.getElementById("shot-id").value }

        fetch("/api/v1/shot/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
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
    }
  }

  renderLogin() {
    this.container.innerHTML = Handlebars.compile(
      document.getElementById("t-login").innerHTML
    )()

    document.getElementById("show-registration-form").onclick = () => {
      this.renderRegistration()
    }

    this.centered.center(
      document.getElementById("login-form")
    )

    document.getElementById("login").onclick = (event) => {
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
      }).then((response) => {
        if (response.status === 201) {
          this.update()
          this.renderProfile()
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

    document.getElementById("show-login-form").onclick = () => {
      this.renderLogin()
    }

    document.getElementById("register").onclick = (event) => {
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
      }).then((response) => {
        if (response.status === 201) {
          alert("Account created successfully, please check you email for verification link.")
          this.renderLogin()
          return
        }
        alert("Can't register with provided email and password, please try again with different credentials")
      })
    }

    this.centered.center(
      document.getElementById("registration-form")
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

  new App()
})