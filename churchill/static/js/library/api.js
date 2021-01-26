"user strict"

export class Api {
  constructor () {
    if (localStorage.getItem("token")) {
      this.token = localStorage.getItem("token")
    }
  }

  getProfile(on_success, on_error) {
    fetch("/api/v1/profile/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + this.token
      },
      async: true,
    }).then(response => {
      if (response.status === 200) {
        response.json().then(data => {
          on_success(data)
        })
        return
      }
      if (response.status === 401) {
        on_error()
        return
      }
      console.error("Error loading profile data")
    })
  }

  getCalendar(on_success, on_error) {
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
          on_success(data.results)
        })
        return
      }
      on_error()
    })
  }

  createShotItem(data, on_success, on_error) {
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
        on_success()
        return
      }
      on_error()
    })
  }

  login(data, on_success, on_error) {
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
          on_success()
        })
        return
      }
      on_error()
    })
  }

  register(data, on_success, on_error) {
    fetch("/api/v1/user/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
      async: true,
    }).then(response => {
      if (response.status === 201) {
        on_success()
        return
      }
      on_error()
    })
  }
}
