// Category Filter
document.querySelectorAll(".category-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    document.querySelectorAll(".category-btn").forEach((b) => b.classList.remove("active"))
    this.classList.add("active")
  })
})

// Search Functionality
const searchInput = document.getElementById("searchInput")
if (searchInput) {
  searchInput.addEventListener("keyup", function () {
    const query = this.value.toLowerCase()
    console.log("[v0] Search query:", query)
  })
}

// Search Button
const searchBtn = document.querySelector(".search-btn")
if (searchBtn) {
  searchBtn.addEventListener("click", () => {
    const query = searchInput.value
    if (query.trim()) {
      console.log("[v0] Searching for:", query)
    }
  })
}

// Download Buttons
document.querySelectorAll(".download-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const quality = this.textContent.trim()
    console.log("[v0] Download initiated:", quality)
    alert("Download started: " + quality)
  })
})

// Server Selection
document.querySelectorAll(".server-card button").forEach((btn) => {
  btn.addEventListener("click", function () {
    const serverName = this.closest(".server-card").querySelector("h5").textContent
    console.log("[v0] Server selected:", serverName)
    alert("Server selected: " + serverName)
  })
})

// Filter Reset
const resetFilters = document.getElementById("resetFilters")
if (resetFilters) {
  resetFilters.addEventListener("click", () => {
    document.querySelectorAll(".form-check-input").forEach((input) => {
      input.checked = false
    })
    document.querySelectorAll("select").forEach((select) => {
      select.value = ""
    })
    console.log("[v0] Filters reset")
  })
}

// Sort Functionality
const sortFilter = document.getElementById("sortFilter")
if (sortFilter) {
  sortFilter.addEventListener("change", function () {
    console.log("[v0] Sort by:", this.value)
  })
}

// Year Filter
const yearFilter = document.getElementById("yearFilter")
if (yearFilter) {
  yearFilter.addEventListener("change", function () {
    console.log("[v0] Year filter:", this.value)
  })
}

// Comment Form Submission
const commentForm = document.querySelector(".comment-form form")
if (commentForm) {
  commentForm.addEventListener("submit", function (e) {
    e.preventDefault()
    const name = this.querySelector('input[type="text"]').value
    const comment = this.querySelector("textarea").value
    console.log("[v0] Comment submitted:", { name, comment })
    alert("Comment posted successfully!")
    this.reset()
  })
}

// Favorite Button
document.querySelectorAll(".btn-outline-danger").forEach((btn) => {
  if (btn.textContent.includes("Favorites")) {
    btn.addEventListener("click", function () {
      this.classList.toggle("btn-danger")
      this.classList.toggle("btn-outline-danger")
      const isFavorited = this.classList.contains("btn-danger")
      console.log("[v0] Favorite toggled:", isFavorited)
    })
  }
})

// Share Button
document.querySelectorAll(".btn-outline-danger").forEach((btn) => {
  if (btn.textContent.includes("Share")) {
    btn.addEventListener("click", () => {
      const movieTitle = document.querySelector(".movie-title")?.textContent || "Movie"
      console.log("[v0] Share clicked for:", movieTitle)
      alert("Share functionality - Movie: " + movieTitle)
    })
  }
})

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const href = this.getAttribute("href")
    if (href !== "#") {
      e.preventDefault()
      const target = document.querySelector(href)
      if (target) {
        target.scrollIntoView({ behavior: "smooth" })
      }
    }
  })
})

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  console.log("[v0] CineHub website loaded")
})
