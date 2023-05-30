/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
const menu = document.querySelector("#dropdown-content");

function toggleMenu() {
    console.log(menu);
    menu.classList.toggle("hide");
}