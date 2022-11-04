const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function updateClock() {
    let element = document.getElementById('clock');
    
    let date = new Date();
    let year = (date.getUTCFullYear() + 1286).toString();
    let month = MONTH_NAMES[date.getUTCMonth()];
    let day = date.getUTCDate().toString().padStart(2, '0');
    let hour = date.getUTCHours().toString().padStart(2, '0');
    let minute = date.getUTCMinutes().toString().padStart(2, '0');
    let seconds = date.getUTCSeconds().toString().padStart(2, '0');
    
    let string = day + ' ' + month + ' ' + year + ' ' + hour + ':' + minute + ':' + seconds;
    element.innerHTML = string;
    
    setTimeout(updateClock, 1000);
}

window.addEventListener('load', (event) => {
    updateClock();
});
