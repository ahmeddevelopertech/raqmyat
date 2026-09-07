const disablePage = () => {
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'block';

    setTimeout(() => {
            overlay.style.display = 'none';
            window.location.reload()
        }, 1500
    );
}

export { disablePage };
