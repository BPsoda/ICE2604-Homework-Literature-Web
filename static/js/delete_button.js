// 添加按钮
let btn=[]
for(i = 0; i < 10; i++) {
    btn[i] = document.createElement('button')
    btn[i].textContent = 'Delete';
    document.getElementsByClassName('operation')[i].appendChild(btn[i]);
    btn[i].addEventListener('click', 
    function() {
        this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode)
    });
}
