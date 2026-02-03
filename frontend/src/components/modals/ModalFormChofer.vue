<script setup>
import { ref, watch } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';


const props = defineProps({
  show: Boolean,
  isLoading: Boolean,
  choferData: { type: Object, default: null },
  opcionesEstado: { type: Array, default: () => [] },
  errors: { type: Object, default: () => ({}) } // Recibe los errores del padre
});

const emit = defineEmits(['close', 'save']);

const initialForm = {
  codigo_chofer: '',
  cedula_identidad: '',
  nombre: '',
  apellido: '',
  telefono: '',
  vencimiento_libreta: '',
  fecha_ingreso: new Date().toISOString().split('T')[0], // Hoy por defecto
  fecha_egreso: '',
  estado: '',
};

const form = ref({ ...initialForm });

// Resetea el Modal
watch(() => props.show, (newVal) => {
  if (newVal) {
    form.value = props.choferData ? { ...props.choferData } : { ...initialForm };
  }
});

const handleSave = () => emit('save', { ...form.value });
</script>

<template>
  <BaseModal 
    :show="show" 
    :title="choferData ? 'Editar Chofer' : 'Nuevo Chofer'" 
    @close="!isLoading && $emit('close')"
  >
    <form class="grid grid-cols-1 md:grid-cols-2 gap-5" @submit.prevent="handleSave">
      <BaseInput 
        v-model="form.nombre"
        label="Nombre"
        :error="errors.nombre"
        placeholder="Ej: José Pedro"
        class="col-span-2"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.apellido"
        label="Apellido"
        :error="errors.apellido"
        placeholder="Ej: Perez Román"
        class="col-span-2"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.telefono"
        label="Teléfono"
        type="tel"
        :error="errors.telefono"
        placeholder="Ej: 099123456"
        class="col-span-2"
        :disabled="isLoading"
      />
      <BaseInput 
        v-model="form.cedula_identidad"
        label="Cédula de Identidad"
        :error="errors.cedula_identidad"
        placeholder="Ej: 51234567"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.codigo_chofer"
        label="Código de Chofer"
        :error="errors.codigo_chofer"
        placeholder="Ej: 1234"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.vencimiento_libreta"
        label="Vencimiento de Libreta"
        type="date"
        :error="errors.vencimiento_libreta"
        :disabled="isLoading"
        required
      />
      <BaseSelect 
        v-model="form.estado"
        label="Estado del Chofer"
        :error="errors.estado"
        :options="opcionesEstado"
        :disabled="isLoading"
      />
      <BaseInput 
        v-model="form.fecha_ingreso"
        label="Fecha de ingreso"
        type="date"
        :error="errors.fecha_ingreso"
        :disabled="isLoading"
      />
      <BaseInput 
        v-model="form.fecha_egreso"
        label="Fecha de egreso"
        type="date"
        :error="errors.fecha_egreso"
        :disabled="isLoading"
      />
    </form>

    <template #footer>
      <BaseButton :disabled="isLoading" @click="$emit('close')">Cancelar</BaseButton>
      <BaseButton variant="primary" :disabled="isLoading" @click="handleSave">
        {{ isLoading ? 'Guardando...' : 'Guardar Chofer' }}
      </BaseButton>
    </template>
  </BaseModal>
</template>