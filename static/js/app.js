function agregarGuia() {
    const url = "/guia/";
    const form = document.getElementById("formGuia");
    const formData = new FormData(form);

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(respuesta => respuesta.json())
    .then(resultado => {
        if (resultado.estado) {
            location.href = "/guia/";
        } else {
            Swal.fire("Agregar guía", resultado.mensaje, "warning");
        }
    })
    .catch(error => {
        console.error("Error al agregar guía:", error);
    });
}


