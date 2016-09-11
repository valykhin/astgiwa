/*!
 * Additional scripts to work with multiselect
 */

function add_row(elem, main_input_id) {
    var list = document.getElementById('urls_list');
    var li = document.createElement('LI');
    var div = document.createElement('DIV');
    var span = document.createElement('SPAN');
    var button = document.createElement('BUTTON');
    var input = document.createElement('INPUT');
    li.className = 'list-group-item';
    div.className = 'input-group';
    div.innerHTML = elem;
    span.className = 'input-group-btn';
    button.className = 'btn btn-primary';
    button.type = 'button';
    button.innerHTML = 'Удалить';
    button.setAttribute('onclick', 'delete_row(this)');
    alert(main_input_id)
    div.children[0].value = document.getElementById(main_input_id).value;
    list.appendChild(li);
    li.appendChild(div);
    div.appendChild(span);
    span.appendChild(button);
    }
    
function delete_row(elem) {
    var li = elem.parentNode.parentNode.parentNode;
    li.parentNode.removeChild(li);
    }