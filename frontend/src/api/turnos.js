import api from "./client";

export async function getTurnos() {
  const res = await api.get("/turnos/");
  return res.data;
}

export async function crearTurno(data) {
  const res = await api.post("/turnos/", data);
  return res.data;
}

export async function actualizarTurno(id, data) {
  const res = await api.put(`/turnos/${id}`, data);
  return res.data;
}

export async function eliminarTurno(id) {
  const res = await api.delete(`/turnos/${id}`);
  return res.data;
}
export async function descargarComprobante(id, formato = "pdf") {
  const response = await api.get(`/turnos/${id}/reporte?formato=${formato}`, {
    responseType: "blob", // para manejar archivos
  });

  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `turno_${id}.${formato}`);
  document.body.appendChild(link);
  link.click();
}