window.addEventListener('load', function(){
    const btn = document.getElementById('del')

    btn.addEventListener('onmouseover', function(){
        btn.classList.add('visible')
        btn.classList.remove('invisible')
    });

});