const scroll = new LocomotiveScroll({
    el: document.querySelector('#main'),
    smooth: true
});

function page4Animation() {
    var elemC = document.querySelector("#elem-container")
    var fixed = document.querySelector("#fixed-image")
    elemC.addEventListener("mouseenter", function () {
        fixed.style.display = "block"
    })
    elemC.addEventListener("mouseleave", function () {
        fixed.style.display = "none"
    })

    var elems = document.querySelectorAll(".elem")
    elems.forEach(function (e) {
        e.addEventListener("mouseenter", function () {
            var image = e.getAttribute("data-image")
            fixed.style.backgroundImage = `url(${image})`
        })
    })
}

function swiperAnimation() {
    var swiper = new Swiper(".mySwiper", {
        slidesPerView: "auto",
        centeredSlides: true,
        spaceBetween: 100,
    });
}
function menuAnimation() {

    var menu = document.querySelector("nav h3")
    var full = document.querySelector("#full-scr")
    var navimg = document.querySelector("nav img")
    var flag = 0
    menu.addEventListener("click", function () {
        if (flag == 0) {
            full.style.top = 0
            navimg.style.opacity = 0
            flag = 1
        } else {
            full.style.top = "-100%"
            navimg.style.opacity = 1
            flag = 0
        }
    })
}

function loaderAnimation() {
    var loader = document.querySelector("#loader")
    setTimeout(function () {
        loader.style.top = "-100%"
    }, 4200)
}
let progress = 0;
let targetProgress = 75; // Change this value for different progress
let progressText = document.getElementById("progress-text");
let circle = document.querySelector(".circle");

function updateLoader() {
    if (progress < targetProgress) {
        progress++;
        progressText.textContent = progress + "%";
        circle.style.background = `conic-gradient( #ddd ${progress}%,#FE320A 0%)`;
        setTimeout(updateLoader, 30); // Adjust speed
    }
}

document.getElementById("send-btn").addEventListener("click", async function () {
    let inputField = document.getElementById("user-input");
    let userMessage = inputField.value.trim();

    if (userMessage) {
        displayMessage(userMessage, "user");

        try {
            let aiResponse = await getOllamaResponse(userMessage);
            displayMessage(aiResponse, "assistant");
        } catch (error) {
            displayMessage("Error: Unable to connect to Ollama AI.", "assistant");
            console.error("Ollama Fetch Error:", error);
        }

        inputField.value = "";
    }
});

async function getOllamaResponse(userMessage) {
    try {
        let response = await fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama2",  // Change to another model if needed
                prompt: userMessage,
                stream: false
            })
        });

        let data = await response.json();
        return data.response;  // Extract AI's response
    } catch (error) {
        console.error("Error fetching AI response:", error);
        return "Sorry, I'm unable to respond at the moment.";
    }
}

function displayMessage(text, sender) {
    let chatBox = document.getElementById("chat-box");

    let messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `<span class="message-text">${text}</span>`;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');


updateLoader();
swiperAnimation()
page4Animation()
menuAnimation()
loaderAnimation()
