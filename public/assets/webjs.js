window.navbarClick = function() {
	const navbar = document.getElementById('navbarMain');
	const burger = document.querySelectorAll('.navbar-burger')[0];
	burger.classList.toggle("is-active");
	navbar.classList.toggle("is-active");
}