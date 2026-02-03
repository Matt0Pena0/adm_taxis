<script setup>
import { ref, onMounted, computed } from 'vue';
import { apiFetch } from '@/services/api';
import { formatCurrency, formatDate } from '@/utils/recaudacionFormato.js';
import BaseButton from '@/components/BaseButton.vue';
import ModalFromRecaudacion from '@/components/modals/ModalFromRecaudacion.vue';


const recaudaciones = ref([]);
const error = ref(null);
const isLoading = ref(true);
const isModalOpen = ref(false);

// Datos para selectores (Necesitamos pasarlos al modal)
const choferes = ref([]);
const coches = ref([]);
const opcionesTurno = ref([]);

// Estado para manejo de errores del formulario
const errors = ref({});


const formatearMensajeError = (msg) => {
  // Limpia el prefijo del ValueError técnico de Pydantic
  const cleanMsg = msg.replace("Value error, ", "");
  
  // Mapea los errores de "campo obligatorio"
  if (cleanMsg === "Field required" || cleanMsg.includes("valid string")) {
    return "Este campo es obligatorio.";
  }
  
  return cleanMsg; 
};


const fetchRecaudaciones = async () => {
  try {
    isLoading.value = true;
    recaudaciones.value = await apiFetch('/recaudaciones'); 
  } catch (e) {
    error.value = "Error conectando con el servidor."
  } finally {
    isLoading.value = false;
  }
};


const handleSaveRecaudacion = async (recaudacionData) => {
  isLoading.value = true;
  errors.value = {}; // Limpiamos errores previos
  console.log("Valores crudos del formulario:", recaudacionData);
  const formValues = {
    ...recaudacionData,
    // IDs (Selects devuelven strings, los forzamos a Int)
    chofer_id: Number(recaudacionData.chofer_id), 
    coche_id: Number(recaudacionData.coche_id),
    
    // Montos (Inputs numéricos a veces vienen como strings)
    // Usamos un ternario: Si está vacío (''), ponemos 0. Si hay dato, convertimos a Number.
    km_entrada: recaudacionData.km_entrada === '' ? 0 : Number(recaudacionData.km_entrada),
    km_salida: recaudacionData.km_salida === '' ? 0 : Number(recaudacionData.km_salida),
    total_recaudado: recaudacionData.total_recaudado === '' ? 0 : Number(recaudacionData.total_recaudado),
    combustible: recaudacionData.combustible === '' ? 0 : Number(recaudacionData.combustible),
    otros_gastos: recaudacionData.otros_gastos === '' ? 0 : Number(recaudacionData.otros_gastos),
    h13: recaudacionData.h13 === '' ? 0 : Number(recaudacionData.h13),
    credito: recaudacionData.credito === '' ? 0 : Number(recaudacionData.credito),
  };

  const cleanedData = Object.fromEntries(
    Object.entries(formValues).filter(([_, v]) => v !== '' && v !== null && v !== undefined)
  );

  console.log("Payload limpio a enviar:", cleanedData); // <--- Revisa esto en consola
  // const cleanedData = Object.fromEntries(
  //   Object.entries(recaudacionData).filter(([_, v]) => v !== '' && v !== null && v !== undefined)
  // );

  try {
    const isEditing = !!recaudacionSeleccionada.value?.id;
    const url = isEditing ? `/recaudaciones/${recaudacionSeleccionada.value.id}` : '/recaudaciones';
    const method = isEditing ? 'PATCH' : 'POST';

    await apiFetch(url, {
      method: method,
      body: JSON.stringify(cleanedData)
    });
    
    isModalOpen.value = false;
    await fetchRecaudaciones();

  } catch (error) {
    // Si entramos aquí, la API falló (422, 400, etc.)
    try {
      // Intentamos procesar el JSON de error
      const rawError = JSON.parse(error.message);
      
      if (rawError.detail && Array.isArray(rawError.detail)) {
        const mapErrors = {};
        
        rawError.detail.forEach(err => {
          const field = err.loc[err.loc.length - 1]; 
          mapErrors[field] = formatearMensajeError(err.msg);
        });

        // Formatea y completa los errores en los inputs
        errors.value = mapErrors;

      } else if (typeof rawError.detail === 'string') {
        alert("Aviso: " + rawError.detail);
      }
    } catch (e) {
      // Si el error no es JSON muestra el alert genérico
      console.error("No se pudo procesar el error:", error.message);
      alert("Error de conexión o servidor");
    }
  } finally {
    isLoading.value = false;
  }
};


const fetchListasAuxiliares = async () => {
  try {
    const [resChoferes, resCoches, resTurnos] = await Promise.all([
      apiFetch('/choferes'),
      apiFetch('/coches'),
      apiFetch('/recaudaciones/enums/turnos'),
    ]);
    choferes.value = resChoferes;
    coches.value = resCoches;
    opcionesTurno.value = resTurnos;
  } catch (error) {
    console.error("Error cargando listas auxiliares", error);
  }
};


const recaudacionSeleccionada = ref(null);
const abrirModalNuevaRecaudacion = () => {
  // Limpia los errores previos
  errors.value = {};
  recaudacionSeleccionada.value = null;
  isModalOpen.value = true;
}


const abrirModalEditarRecaudacion = (recaudacion) => {
  // Limpia los errores previos
  errors.value = {};
  recaudacionSeleccionada.value = { ...recaudacion };
  isModalOpen.value = true;
}


//  Limpia el Modal antes de cerrar
const cerrarModal = () => {
  errors.value = {};
  isModalOpen.value = false;
};


// KPI CALCULADO (Ejemplo simple)
const totalMensual = computed(() => {
  return recaudaciones.value.reduce((acc, curr) => acc + Number(curr.total_recaudado || 0), 0);
});


onMounted(() => {
  fetchRecaudaciones();
  fetchListasAuxiliares();
});
</script>

<template>
  <div>
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 gap-4">
      <div>
        <h2 class="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">Recaudaciones</h2>
        <p class="text-slate-500 dark:text-slate-400">Control de ingresos y egresos diarios</p>
      </div>

      <div class="flex gap-3">
        <div class="px-4 py-2 bg-slate-50 dark:bg-slate-800 rounded-lg border border-border-light dark:border-border-dark text-right">
          <p class="text-xs text-slate-500 uppercase font-bold">Total Acumulado</p>
          <p class="text-xl font-bold text-primary-dark dark:text-primary">{{ formatCurrency(totalMensual) }}</p>
        </div>

        <BaseButton icon="heroicons:plus"
        @click="abrirModalNuevaRecaudacion"
        >
          Nueva Planilla
        </BaseButton>

        <ModalFromRecaudacion
          :show="isModalOpen"
          :choferes="choferes"
          :coches="coches"
          :opcionesTurno="opcionesTurno"
          :recaudacionData="recaudacionSeleccionada"
          :errors="errors"
          :isLoading="isLoading"
          @close="cerrarModal"
          @save="handleSaveRecaudacion"
        />

      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-border-light dark:border-border-dark overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-slate-500 uppercase bg-slate-50 dark:bg-slate-900/50 border-b border-border-light dark:border-border-dark">
            <tr>
              <th class="px-6 py-3">Fecha / Turno</th>
              <th class="px-6 py-3">Coche / Chofer</th>
              <th class="px-6 py-3 text-right">Kms</th>
              <th class="px-6 py-3 text-right">Bruto</th>
              <th class="px-6 py-3 text-right">Gastos</th>
              <th class="px-6 py-3 text-right">A Entregar</th>
              <th class="px-6 py-3 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border-light dark:divide-border-dark">
            <tr v-for="item in recaudaciones" :key="item.id" class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
              
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white whitespace-nowrap">
                {{ formatDate(item.fecha_turno) }}
                <span class="block text-xs text-slate-500 font-normal uppercase mt-0.5">{{ item.turno }}</span>
              </td>

              <td class="px-6 py-4">
                <div class="flex flex-col">
                  <span class="font-medium text-slate-700 dark:text-slate-200">STX {{ item.coche?.matricula || '---' }}</span>
                  <span class="text-slate-500">{{ item.chofer?.nombre }} {{ item.chofer?.apellido }}</span>
                </div>
              </td>

              <td class="px-6 py-4 text-right font-mono text-slate-600 dark:text-slate-400">
                {{ item.km_totales }} km
                <span class="block text-xxs text-slate-400">Rend: {{ item.rendimiento }}$/Km</span>
              </td>

              <td class="px-6 py-4 text-right font-medium text-slate-900 dark:text-slate-200">
                {{ formatCurrency(item.total_recaudado) }}
              </td>

              <td class="px-6 py-4 text-right font-medium text-rose-600 dark:text-rose-400">
                {{ formatCurrency(item.total_gastos) }}
              </td>

              <td class="px-6 py-4 text-right font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50/50 dark:bg-emerald-900/10">
                {{ formatCurrency(item.total_entregar) }}
              </td>

              <td class="px-6 py-4 text-center">
                <button class="text-slate-400 hover:text-primary transition-colors">
                  <span class="material-symbols-outlined text-[20px]">visibility</span>
                </button>
              </td>

            </tr>
            <tr v-if="recaudaciones.length === 0 && !isLoading">
              <td colspan="7" class="px-6 py-10 text-center text-slate-500">
                No hay recaudaciones registradas aún.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>