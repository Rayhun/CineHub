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

// Password Toggle
function togglePassword(fieldId) {
  const field = document.getElementById(fieldId)
  if (field.type === "password") {
    field.type = "text"
  } else {
    field.type = "password"
  }
}

// Login Form Submission
const loginForm = document.getElementById("loginForm")
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault()
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    console.log("[v0] Login attempt:", { email })
    alert("Login successful! Welcome back.")
    this.reset()
  })
}

// Signup Form Submission
const signupForm = document.getElementById("signupForm")
if (signupForm) {
  signupForm.addEventListener("submit", function (e) {
    e.preventDefault()
    const fullname = document.getElementById("fullname").value
    const email = document.getElementById("signup-email").value
    const password = document.getElementById("signup-password").value
    const confirmPassword = document.getElementById("confirm-password").value

    if (password !== confirmPassword) {
      alert("Passwords do not match!")
      return
    }

    console.log("[v0] Signup attempt:", { fullname, email })
    alert("Account created successfully! Please check your email to verify.")
    this.reset()
  })
}

// Profile Tab Navigation
document.querySelectorAll(".profile-menu-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault()
    const tabId = this.getAttribute("data-tab")

    // Remove active class from all items and tabs
    document.querySelectorAll(".profile-menu-item").forEach((i) => i.classList.remove("active"))
    document.querySelectorAll(".profile-tab").forEach((tab) => tab.classList.remove("active"))

    // Add active class to clicked item and corresponding tab
    this.classList.add("active")
    document.getElementById(tabId).classList.add("active")

    console.log("[v0] Profile tab switched to:", tabId)
  })
})

// Profile Form Submission
const profileForm = document.getElementById("profileForm")
if (profileForm) {
  profileForm.addEventListener("submit", (e) => {
    e.preventDefault()
    console.log("[v0] Profile updated")
    alert("Profile updated successfully!")
  })
}

// Password Change Form
const passwordForm = document.getElementById("passwordForm")
if (passwordForm) {
  passwordForm.addEventListener("submit", function (e) {
    e.preventDefault()
    const newPwd = document.getElementById("new-pwd").value
    const confirmPwd = document.getElementById("confirm-pwd").value

    if (newPwd !== confirmPwd) {
      alert("Passwords do not match!")
      return
    }

    console.log("[v0] Password changed")
    alert("Password changed successfully!")
    this.reset()
  })
}

// Pricing Plan Selection
document.querySelectorAll(".pricing-card .btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const planName = this.closest(".pricing-card").querySelector("h3").textContent
    console.log("[v0] Plan selected:", planName)
    alert("Proceeding to checkout for " + planName + " plan")
  })
})

// Change Avatar
document.querySelectorAll(".change-avatar").forEach((btn) => {
  btn.addEventListener("click", () => {
    console.log("[v0] Avatar change initiated")
    alert("Avatar upload feature coming soon!")
  })
})

// Download Again Button
document.querySelectorAll(".history-action .btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const movieTitle = this.closest(".history-item").querySelector("h5").textContent
    console.log("[v0] Re-download initiated:", movieTitle)
    alert("Download started: " + movieTitle)
  })
})

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  console.log("[v0] CineHub website loaded")
})
