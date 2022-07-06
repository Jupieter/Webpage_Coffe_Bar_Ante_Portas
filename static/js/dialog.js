var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerList) {
  return new bootstrap.Popover(popoverTriggerList)
})

function closeModal() {
  var container = document.getElementById("modals-here")
  var backdrop = document.getElementById("modal-backdrop")
  var modal = document.getElementById("modalMessenger")

  modal.classList.remove("show")
  backdrop.classList.remove("show")


  setTimeout(function() {
    container.removeChild(modal)
    container.removeChild(backdrop)
  }, 200)
}

;(function () {
  const modal = new bootstrap.Modal(document.getElementById("modalForm"))

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
      modal.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })
})()

//based:
// https://blog.benoitblanchon.fr/django-htmx-modal-form/
// https://www.bugbytes.io/posts/django-bokeh-and-htmx-data-driven-bar-charts/  YT video in it.

