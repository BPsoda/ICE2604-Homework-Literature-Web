// 添加按钮
let btn=[]
for(i = 0; i < 10; i++) {
    btn[i] = document.createElement('button')
    btn[i].textContent = 'Deletee';
    document.getElementsByClassName('operation')[i].appendChild(btn[i]);
    restButton.addEventListener('click', 
    function() {
        this.parentNode.parentNode.removeChild()
    });
}
