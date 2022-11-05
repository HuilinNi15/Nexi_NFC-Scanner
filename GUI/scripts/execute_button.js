document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById("button")
    const button_text = document.getElementById("button_text")
    const ripple = document.getElementById("ripple")    
    const gif = document.getElementById("gif")    
    var clicked = false
    button.onclick = () => {
        if (!clicked) {
            clicked = true
            button.classList.add("activated")
            button_text.innerHTML = ""
            gif.classList.remove("moved")
            setTimeout(() => {ripple.style.display = 'inline-block'}, 100)


            setTimeout(() => {
                ripple.style.display = 'none'
                button.classList.add("scanned")}
            , 5000);
        }
        
    }

})