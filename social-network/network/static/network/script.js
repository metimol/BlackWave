const themeToggler = document.getElementById('theme-toggler')

// Initialize theme
if (localStorage.getItem("theme") === null) {
    localStorage.setItem("theme", "auto")
}

setTheme()

if (themeToggler) {
    themeToggler.value = localStorage.getItem("theme")
    themeToggler.addEventListener("change", () => {
        localStorage.setItem("theme", themeToggler.value)
        setTheme()
    })
}

// Event Listeners
document.querySelectorAll("button.connect").forEach(btn => {
    btn.addEventListener("click", (e) => {
        connect(e.target.dataset.username)
    })
})

document.querySelectorAll("button.like").forEach(btn => {
    btn.addEventListener("click", () => {
        react(btn)
    })
})

document.querySelectorAll("button.bookmark").forEach(btn => {
    btn.addEventListener("click", () => {
        bookmark(btn)
    })
})

document.querySelectorAll("button.edit").forEach(btn => {
    btn.addEventListener("click", () => {
        const postId = btn.dataset.postid;
        const postEl = document.querySelector(`div.post[data-postid="${postId}"]`)
        const postContent = postEl.querySelector(".post-content")
        const postEditForm = postEl.querySelector(".post-edit-form")

        if (postContent.style.display === "none") {
            postContent.style.display = "block"
            postEditForm.style.display = "none"
        }
        else {
            postContent.style.display = "none"
            postEditForm.style.display = "block"
        }
    })
})

document.querySelectorAll(".post-edit-form").forEach(form => {
    form.addEventListener("submit", (e) => {
        e.preventDefault()
        editPost(form)
    })
})

document.querySelectorAll("button.delete").forEach(btn => {
    btn.addEventListener("click", () => {
        deletePost(btn)
    })
})

document.querySelectorAll("button.pin").forEach(btn => {
    btn.addEventListener("click", () => {
        pinPost(btn)
    })
})

document.querySelectorAll("button.edit-comment").forEach(btn => {
    btn.addEventListener("click", () => {
        const commentId = btn.dataset.commentid;
        const commentEl = document.querySelector(`div.comment[data-commentid="${commentId}"]`)
        const commentContent = commentEl.querySelector(".comment-content")
        const commentEditForm = commentEl.querySelector(".comment-edit-form")
        if (commentContent.style.display === "none") {
            commentContent.style.display = "block"
            commentEditForm.style.display = "none"
        } else {
            commentContent.style.display = "none"
            commentEditForm.style.display = "block"
        }
    })
})

document.querySelectorAll(".comment-edit-form").forEach(form => {
    form.addEventListener("submit", (e) => {
        e.preventDefault()
        editComment(form)
    })
})

document.querySelectorAll("button.delete-comment").forEach(btn => {
    btn.addEventListener("click", () => {
        deleteComment(btn)
    })
})

// Functions
function setTheme() {
    if (localStorage.getItem("theme") === "light") {
        document.body.dataset.bsTheme = "light"
    }
    else if (localStorage.getItem("theme") === "dark") {
        document.body.dataset.bsTheme = "dark"
    }
    else {
        document.body.dataset.bsTheme = window.matchMedia('(prefers-color-scheme: light)').matches ? "light" : "dark"
    }
}

function connect(username) {
    fetch(`/profile/${username}/connect`, { method: 'POST' })
        .then(res => res.json())
        .then(res => {
            if (res.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (res.status === "404") {
                alert(res.response)
            }
            else {
                location.reload()
            }
        })
}

function react(el) {
    const postId = parseInt(el.dataset.postid)
    fetch(`/posts/${postId}/react`, { method: 'POST' })
        .then(res => res.json())
        .then(res => {
            if (res.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (res.status === "404") {
                alert(res.response)
            }
            else {
                if (res.action == "Liked") {
                    el.innerHTML = `<i class="fas fa-heart"></i> <span class="ml-1">${res.postReactionsCount}</span>`
                }
                else {
                    el.innerHTML = `<i class="far fa-heart"></i> <span class="ml-1">${res.postReactionsCount}</span>`
                }
            }
        })
}

function bookmark(el) {
    const postId = parseInt(el.dataset.postid)
    fetch(`/posts/${postId}/bookmark`, { method: 'POST' })
        .then(res => res.json())
        .then(res => {
            if (res.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (res.status === "404") {
                alert(res.response)
            }
            else {
                if (res.action == "Bookmarked") {
                    el.innerHTML = `<i class="fas fa-bookmark"></i>`
                }
                else {
                    el.innerHTML = `<i class="far fa-bookmark"></i>`
                }
            }
        })
}

function editPost(form) {
    const postId = form.dataset.postid
    const postEl = form.parentElement
    const content = form.querySelector("textarea").value

    fetch(`/posts/${postId}/edit`, {
        method: "POST",
        body: JSON.stringify({
            content: content
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (data.status == "201") {
                postEl.querySelector(".post-content").innerHTML = data.postContent.replace(/\n/g, '<br>')
            }
            else {
                alert(data.response)
            }
        })
    form.style.display = "none"
    postEl.querySelector(".post-content").style.display = "block"
}

function deletePost(btn) {
    const postId = btn.dataset.postid
    fetch(`/posts/${postId}/delete`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (data.status == "201") {
                if (window.location.pathname.startsWith("/posts/")) {
                    window.location.href = window.location.origin
                }
                else {
                    const postDiv = document.querySelector(`div.post[data-postid='${postId}']`)
                    if (postDiv) postDiv.remove()
                }
            }
            else {
                alert(data.response)
            }
        })
}

function pinPost(btn) {
    const postId = btn.dataset.postid
    fetch(`/posts/${postId}/pin`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.status === "401") {
                window.location.href = window.location.origin + "/login"
            }
            else if (data.status == "201") {
                window.location.href = window.location.origin + "/profile/" + data.username
            }
            else {
                alert(data.response)
            }
        })
}

function editComment(form) {
    const commentId = form.dataset.commentid
    const commentEl = form.parentElement
    const content = form.querySelector("textarea").value
    fetch(`/comments/${commentId}/edit`, {
        method: "POST",
        body: JSON.stringify({ content: content })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === "401") {
                window.location.href = window.location.origin + "/login"
            } else if (data.status == "201") {
                commentEl.querySelector(".comment-content").innerHTML = data.commentContent.replace(/\n/g, '<br>')
            } else {
                alert(data.response)
            }
        })
    form.style.display = "none"
    commentEl.querySelector(".comment-content").style.display = "block"
}

function deleteComment(btn) {
    const commentId = btn.dataset.commentid
    fetch(`/comments/${commentId}/delete`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.status === "401") {
                window.location.href = window.location.origin + "/login"
            } else if (data.status == "201") {
                const commentDiv = document.querySelector(`div.comment[data-commentid='${commentId}']`)
                if (commentDiv) commentDiv.remove()
            } else {
                alert(data.response)
            }
        })
}