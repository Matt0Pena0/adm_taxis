<script setup>
import { ref, watch } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';


const props = defineProps({
  show: Boolean,
  isLoading: Boolean,
  choferes: Array,
  coches: Array,
  recaudacionData: { type: Object, default: null },
  opcionesTurno: { type: Array, default: () => [] } ,
  errors: { type: Object, default: () => ({}) } // Recibe los errores del padre
});

const emit = defineEmits(['close', 'save']);

const initialForm = {
  // Contexto
  chofer_id: '',
  coche_id: '',
  // Fechas
  turno: '',
  fecha_turno: '',

  // Kms
  km_entrada: '',
  km_salida: '',

  // Caja
  total_recaudado: '',
  combustible: 0,
  otros_gastos: 0,
  h13: 0,
  credito: 0,
};

const form = ref({ ...initialForm });

// Resetea el Modal
watch(() => props.show, (newVal) => {
  if (newVal) {
    form.value = props.recaudacionData ? { ...props.recaudacionData } : { ...initialForm };
  }
});

const handleSubmit = () => emit('save', { ...form.value });
</script>

<template>
  <BaseModal 
    :show="show"
    :title="recaudacionData ? 'Editar Recaudación Diaria' : 'Nueva Recaudación Diaria'" 
    @close="!isLoading && $emit('close')">
    
    <form @submit.prevent="handleSubmit" class="space-y-6">
      
      <div class="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-lg border border-border-light dark:border-border-dark grid grid-cols-1 md:grid-cols-2 gap-4">
        <BaseSelect 
          v-model="form.chofer_id" 
          label="Chofer" 
          :options="choferes.map(c => ({ value: c.id, label: `${c.nombre} ${c.apellido}` }))"
          :error="errors.chofer_id"
          required
        />
        <BaseSelect 
          v-model="form.coche_id" 
          label="Coche" 
          :options="coches.map(c => ({ value: c.id, label: `STX ${c.matricula}` }))"
          :error="errors.coche_id"
          required
        />
        <BaseInput 
          v-model="form.fecha_turno" 
          type="date" 
          label="Fecha" 
          :error="errors.fecha_turno"
          required
        />
        <BaseSelect 
          v-model="form.turno" 
          label="Turno" 
          :options="opcionesTurno"
          :error="errors.turno"
          required
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <BaseInput 
          v-model="form.km_salida" 
          type="number" 
          label="Km Salida" 
          placeholder="0"
          :error="errors.km_salida"
        />
        <BaseInput 
          v-model="form.km_entrada" 
          type="number" 
          label="Km Entrada" 
          placeholder="0"
          :error="errors.km_entrada"
        />
      </div>

      <hr class="border-border-light dark:border-border-dark">

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <BaseInput 
          v-model="form.total_recaudado" 
          type="number" 
          step="0.01"
          label="Total Recaudado" 
          class="md:col-span-2"
          placeholder="$ 0.00"
          :error="errors.total_recaudado"
          required
        />
        
        <BaseInput 
          v-model="form.combustible" 
          type="number" 
          step="0.01" 
          label="Combustible" 
          placeholder="$ 0.00"
          :error="errors.combustible"
        />
        <BaseInput 
          v-model="form.otros_gastos" 
          type="number" 
          step="0.01" 
          label="Otros Gastos" 
          placeholder="$ 0.00"
          :error="errors.otros_gastos"
        />
        <BaseInput 
          v-model="form.credito" 
          type="number" 
          step="0.01" 
          label="Crédito" 
          placeholder="$ 0.00"
          :error="errors.credito"
        />
        <BaseInput 
          v-model="form.h13" 
          type="number" 
          step="0.01" 
          label="H13" 
          placeholder="$ 0.00"
          :error="errors.h13"
        />
      </div>

    </form>

    <template #footer>
      <BaseButton @click="$emit('close')">Cancelar</BaseButton>
      <BaseButton variant="primary" @click="handleSubmit">Registrar Planilla</BaseButton>
    </template>
  </BaseModal>
</template>