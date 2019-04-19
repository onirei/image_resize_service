/**
 * Created by Onirei on 19.04.2019.
 */

function queryset_filter(form) {
    for (var i=0;i<form.elements.length;i++) {
        if (form.elements[i].value.length === 0) {
            form.elements[i].setAttribute('disabled', 'true');
        }
    }
}

function validate_upload(form) {
    if (form.elements.image_from_file.value.length === 0 && form.elements.image_from_url.value.length === 0) {
        document.error.innerHTML = 'Заполните хотя бы одно поле!';
        return false;
    }
    if (form.elements.image_from_file.value.length !== 0 && form.elements.image_from_url.value.length !== 0) {
        document.error.innerHTML = 'Заполните только одно поле!';
        return false;
    }
}
