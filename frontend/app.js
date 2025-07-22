document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const addBookForm = document.getElementById("add-book-form");
    const authSection = document.getElementById("auth-section");
    const librarySection = document.getElementById("library-section");
    const booksList = document.getElementById("books-list");

    let token = null;

    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("register-name").value;
        const email = document.getElementById("register-email").value;
        const password = document.getElementById("register-password").value;
        const role = document.getElementById("register-role").value;

        const response = await fetch("/users/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role }),
        });

        if (response.ok) {
            alert("Registration successful! Please login.");
        } else {
            alert("Registration failed.");
        }
    });

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const response = await fetch("/token", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `username=${email}&password=${password}`,
        });

        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            authSection.style.display = "none";
            librarySection.style.display = "block";
            fetchBooks();
        } else {
            alert("Login failed.");
        }
    });

    addBookForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("book-title").value;
        const author = document.getElementById("book-author").value;
        const genre = document.getElementById("book-genre").value;

        const response = await fetch("/books/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ title, author, genre }),
        });

        if (response.ok) {
            fetchBooks();
        } else {
            alert("Failed to add book.");
        }
    });

    async function fetchBooks() {
        const response = await fetch("/books/");
        const books = await response.json();
        booksList.innerHTML = "";
        books.forEach(book => {
            const bookItem = document.createElement("div");
            bookItem.className = "book-item";
            bookItem.textContent = `${book.title} by ${book.author} - ${book.available ? 'Available' : 'Borrowed'}`;
            booksList.appendChild(bookItem);
        });
    }
});
