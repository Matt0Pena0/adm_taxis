<script setup>
import { ref, onMounted } from 'vue'

import { apiFetch } from '@/services/api'
import ChoferCard from '@/components/ChoferCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import ModalFromChofer from '@/components/modals/ModalFormChofer.vue'


const choferes = ref([])
const error = ref(null)
const errors = ref({})
const isLoading = ref(true)
const isModalOpen = ref(false)


const formatearMensajeError = (msg) => {
  // Limpia el prefijo del ValueError técnico de Pydantic
  const cleanMsg = msg.replace("Value error, ", "");
  
  // Mapea los errores de "campo obligatorio"
  if (cleanMsg === "Field required" || cleanMsg.includes("valid string")) {
    return "Este campo es obligatorio.";
  }
  
  return cleanMsg; 
};


// Establece la conexion con la API
const fetchChoferes = async () => {
  try {
    isLoading.value = true;
    choferes.value = await apiFetch('/choferes')
  } catch (e) {
    error.value = "Error conectando con el servidor."
  } finally {
    isLoading.value = false
  }
}


const handleSaveChofer = async (choferData) => {
  isLoading.value = true;
  errors.value = {}; // Limpiamos errores previos

  const cleanedData = Object.fromEntries(
    Object.entries(choferData).filter(([_, v]) => v !== '' && v !== null && v !== undefined)
  );

  try {
    const isEditing = !!choferSeleccionado.value?.id;
    const url = isEditing ? `/choferes/${choferSeleccionado.value.id}` : '/choferes';
    const method = isEditing ? 'PATCH' : 'POST';

    await apiFetch(url, {
      method: method,
      body: JSON.stringify(cleanedData)
    });
    
    isModalOpen.value = false;
    await fetchChoferes();
    
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


const estadosChofer = ref([]);
const fetchEnums = async () => {
  try {
    const data = await apiFetch('choferes/enums/estados');
    estadosChofer.value = data;
  } catch (error) {
    console.error("Error cargando enums", error)
  }
};


const choferSeleccionado = ref(null);
const abrirModalNuevoChofer = () => {
  // Limpia los errores previos
  errors.value = {}; 
  choferSeleccionado.value = null;
  isModalOpen.value = true;
};


const abrirModalEditarChofer = (chofer) => {
  // Limpia los errores previos
  errors.value = {};
  choferSeleccionado.value = { ...chofer };
  isModalOpen.value = true;
};


//  Limpia el Modal antes de cerrar
const cerrarModal = () => {
  errors.value = {};
  isModalOpen.value = false;
};


onMounted(() => {
  fetchChoferes();
  fetchEnums();
});
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">Gestión de Choferes</h2>
     
      <BaseButton icon="heroicons:plus"
      @click="abrirModalNuevoChofer"
      >
        Nuevo Chofer
      </BaseButton>

      <ModalFromChofer
        :show="isModalOpen"
        :choferData="choferSeleccionado"
        :opciones-estado="estadosChofer"
        :errors="errors"
        :isLoading="isLoading"
        @close="cerrarModal"
        @save="handleSaveChofer"
      />

    </div>

    <div v-if="isLoading" class="text-center py-20">
      <span class="material-symbols-outlined animate-spin text-4xl text-primary">Cargando...</span>
      <p class="mt-2">Enseguida verás la lista de choferes...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg border border-red-200">
      {{ error }}
    </div>

    <div class="grid grid-cols-[repeat(auto-fill,minmax(200px,2fr))] gap-2 md:gap-3 xl:gap-6">
      
      <ChoferCard 
        v-for="choferItem in choferes"
        :key="choferItem.id"
        :chofer="choferItem"
        @edit="abrirModalEditarChofer"
      />
      
    </div>
  </div>
</template>
