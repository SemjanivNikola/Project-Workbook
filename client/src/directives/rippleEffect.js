
export default {
	bind (el) {
		console.log('el: ', el);

		function materializeEffect(event){
			console.log('here');
			const circle = document.createElement('div');
			const x = event.layerX;
			const y = event.layerY;
			circle.classList.add('btn-fade-circle');
			circle.style.left = `${x}px`;
			circle.style.top = `${y}px`;
			el.appendChild(circle);
		}

		el.addEventListener('click', materializeEffect);
	}
}
