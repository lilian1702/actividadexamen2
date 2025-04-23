
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-instructor");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const datos = new URLSearchParams(formData);
        try {
            const response = await fetch("/agregarInstructor", {
                method: "POST",
                body: datos
            });
            if (response.redirected) {
                Swal.fire({
                    icon: 'success',
                    title: 'Instructor guardado',
                    text: 'Se ha enviado la contraseña al correo.',
                    timer: 3000,
                    showConfirmButton: false
                });
                form.reset();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al guardar',
                    text: 'Verifica los datos.',
                });
            }
        } catch (error) {
            console.error("Error:", error);
            Swal.fire({
                icon: 'error',
                title: 'Error de conexión',
                text: 'No se pudo contactar con el servidor.',
            });
        }
    });
});

