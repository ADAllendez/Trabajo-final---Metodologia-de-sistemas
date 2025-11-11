import { useEffect, useState } from "react";
import { crearTurno, actualizarTurno, getTurnos } from "../api/turnos";
import { getPacientes } from "../api/pacientes";
import { getMedicos } from "../api/medicos";
import { getEspecialidades } from "../api/especialidades";
import Layout from "../components/Layout";

function TurnosPage() {
  const [pacientes, setPacientes] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [especialidades, setEspecialidades] = useState([]);
  const [especialidadSeleccionada, setEspecialidadSeleccionada] = useState("");
  const [turnos, setTurnos] = useState([]);

  const [form, setForm] = useState({
    id_turno: null,
    id_paciente: "",
    id_medico: "",
    fecha_turno: "",
    estado: "Programado",
  });
  const [modoEdicion, setModoEdicion] = useState(false);

  async function cargarDatos() {
    const [ps, ms, esps, ts] = await Promise.all([
      getPacientes(),
      getMedicos(),
      getEspecialidades(),
      getTurnos(),
    ]);
    setPacientes(ps);
    setMedicos(ms);
    setEspecialidades(esps);
    setTurnos(ts);
  }

  useEffect(() => {
    cargarDatos();
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      id_paciente: Number(form.id_paciente),
      id_medico: form.id_medico ? Number(form.id_medico) : null,
      fecha_turno: form.fecha_turno,
      estado: form.estado,
    };

    if (modoEdicion && form.id_turno) {
      await actualizarTurno(form.id_turno, payload);
    } else {
      await crearTurno(payload);
    }

    setForm({
      id_turno: null,
      id_paciente: "",
      id_medico: "",
      fecha_turno: "",
      estado: "Programado",
    });
    setModoEdicion(false);
    setEspecialidadSeleccionada("");
    await cargarDatos();
  }

  //Función para cambiar el estado del turno desde los botones
  async function cambiarEstado(id_turno, nuevoEstado) {
    const turno = turnos.find((t) => t.id_turno === id_turno);
    if (!turno) return alert("Turno no encontrado");

    const payload = {
      id_paciente: turno.id_paciente,
      id_medico: turno.id_medico,
      fecha_turno: turno.fecha_turno,
      estado: nuevoEstado,
    };

    await actualizarTurno(id_turno, payload);
    await cargarDatos();
  }

  //Médicos filtrados por especialidad
  const medicosFiltrados =
    especialidadSeleccionada === ""
      ? medicos
      : medicos.filter(
        (m) => m.id_especialidad === Number(especialidadSeleccionada)
      );

  return (
    <Layout current="turnos">
      {/* Encabezado */}
      <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="flex items-center gap-2 text-2xl font-semibold text-slate-800 md:text-3xl">
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white">
              📅
            </span>
            Nuevo Turno
          </h1>
          <p className="text-sm text-slate-500">
            Completá los datos para registrar un nuevo turno.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            setModoEdicion(false);
            setForm({
              id_turno: null,
              id_paciente: "",
              id_medico: "",
              fecha_turno: "",
              estado: "Programado",
            });
            setEspecialidadSeleccionada("");
          }}
          className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50"
        >
          ⬅ Limpiar formulario
        </button>
      </div>

      {/* --- Formulario --- */}
      <div className="mb-6 overflow-hidden rounded-xl bg-white shadow-md">
        <div className="flex items-center gap-2 bg-blue-600 px-5 py-3 text-white">
          <span>✏️</span>
          <h2 className="font-semibold">Datos del Turno</h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 px-5 py-4">
          {/* Paciente / Médico */}
          <div className="grid gap-4 md:grid-cols-2">
            {/* Paciente */}
            <div className="rounded-lg border bg-slate-50 p-4 shadow-sm">
              <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-700">
                👤 Paciente <span className="text-red-500">*</span>
              </h3>
              <select
                name="id_paciente"
                value={form.id_paciente}
                onChange={handleChange}
                required
                className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm"
              >
                <option value="">-- Seleccionar paciente --</option>
                {pacientes.map((p) => (
                  <option key={p.id_paciente} value={p.id_paciente}>
                    {p.nombre} {p.apellido}
                  </option>
                ))}
              </select>
            </div>

            {/* Especialidad + Médico */}
            <div className="rounded-lg border bg-slate-50 p-4 shadow-sm">
              <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-700">
                🩺 Médico <span className="text-red-500">*</span>
              </h3>

              <select
                value={especialidadSeleccionada}
                onChange={(e) => {
                  setEspecialidadSeleccionada(e.target.value);
                  setForm((prev) => ({ ...prev, id_medico: "" }));
                }}
                className="mb-3 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm"
              >
                <option value="">-- Seleccionar especialidad --</option>
                {especialidades.map((esp) => (
                  <option key={esp.id_especialidad} value={esp.id_especialidad}>
                    {esp.nombre}
                  </option>
                ))}
              </select>

              <select
                name="id_medico"
                value={form.id_medico}
                onChange={handleChange}
                required
                disabled={medicosFiltrados.length === 0}
                className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm"
              >
                <option value="">
                  {especialidadSeleccionada === ""
                    ? "-- Primero elija una especialidad --"
                    : medicosFiltrados.length === 0
                      ? "No hay médicos disponibles"
                      : "-- Seleccionar médico --"}
                </option>
                {medicosFiltrados.map((m) => (
                  <option key={m.id_medico} value={m.id_medico}>
                    {m.nombre} {m.apellido}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Fecha / Hora / Estado */}
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <label className="text-xs text-slate-600">Fecha *</label>
              <input
                type="date"
                name="fecha_turno"
                value={form.fecha_turno.split("T")[0] || ""}
                onChange={(e) => {
                  const fecha = e.target.value;
                  const hora = form.fecha_turno.split("T")[1] || "09:00";
                  setForm({ ...form, fecha_turno: `${fecha}T${hora}` });
                }}
                required
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label className="text-xs text-slate-600">Hora *</label>
              <input
                type="time"
                name="hora"
                value={form.fecha_turno ? form.fecha_turno.slice(11, 16) : ""}
                onChange={(e) => {
                  const hora = e.target.value;
                  const fecha =
                    form.fecha_turno.split("T")[0] ||
                    new Date().toISOString().slice(0, 10);
                  setForm({ ...form, fecha_turno: `${fecha}T${hora}` });
                }}
                required
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label className="text-xs text-slate-600">Estado</label>
              <select
                name="estado"
                value={form.estado}
                onChange={handleChange}
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              >
                <option value="Programado">Programado</option>
                <option value="Atendiendo">Atendiendo</option>
                <option value="Finalizado">Finalizado</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-semibold text-white hover:bg-blue-700"
            >
              ✅ {modoEdicion ? "Guardar cambios" : "Crear Turno"}
            </button>
          </div>
        </form>
      </div>

      {/* --- Panel de ayuda --- */}
      <div className="mb-6 rounded-xl bg-white p-4 text-sm text-slate-600 shadow-md">
        <h3 className="mb-2 font-semibold">💡 Ayuda</h3>
        <ul className="list-disc list-inside space-y-1">
          <li>Los campos marcados con * son obligatorios.</li>
          <li>El paciente y el médico deben estar cargados en el sistema.</li>
          <li>Revisá el horario del médico antes de asignar el turno.</li>
        </ul>
      </div>

      {/* --- Tabla de Turnos con botones de estado --- */}
      <div className="overflow-x-auto rounded-xl bg-white p-4 shadow-md">
        <h2 className="mb-3 text-lg font-semibold text-slate-800">
          📋 Turnos Activos
        </h2>
        <table className="w-full border-collapse text-sm">
          <thead className="bg-slate-100 text-left text-slate-600">
            <tr>
              <th className="p-2">Paciente</th>
              <th className="p-2">Médico</th>
              <th className="p-2">Fecha</th>
              <th className="p-2">Estado</th>
              <th className="p-2 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {turnos.map((t) => (
              <tr key={t.id_turno} className="border-b last:border-none">
                <td className="p-2">
                  {t.paciente?.nombre} {t.paciente?.apellido}
                </td>
                <td className="p-2">
                  {t.medico
                    ? `${t.medico.nombre} ${t.medico.apellido}`
                    : "Sin asignar"}
                </td>
                <td className="p-2">
                  {new Date(t.fecha_turno).toLocaleString()}
                </td>
                <td className="p-2 font-medium">{t.estado}</td>
                <td className="p-2 text-center space-x-2">
                  <div className="flex justify-center gap-2">
                    <button
                      onClick={() => cambiarEstado(t.id_turno, "Atendiendo")}
                      className="rounded-md bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700 hover:bg-emerald-200"
                    >
                      🩺 Atendiendo
                    </button>
                    <button
                      onClick={() => cambiarEstado(t.id_turno, "Finalizado")}
                      className="rounded-md bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 hover:bg-slate-200"
                    >
                      ✅ Finalizado
                    </button>
                    <button
                      onClick={() => cambiarEstado(t.id_turno, "Cancelado")}
                      className="rounded-md bg-red-100 px-3 py-1 text-xs font-medium text-red-700 hover:bg-red-200"
                    >
                      ❌ Cancelar
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}

export default TurnosPage;

