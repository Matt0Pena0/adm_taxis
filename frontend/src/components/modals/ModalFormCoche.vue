<script setup>
import { ref, watch } from 'vue';
import BaseModal from '@/components/modals/BaseModal.vue';
import BaseButton from '@/components/BaseButton.vue';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';


const props = defineProps({
  show: Boolean,
  isLoading: Boolean,
  cocheData: { type: Object, default: null },
  opcionesEstado: { type: Array, default: () => [] },
  errors: { type: Object, default: () => ({}) } // Recibe los errores del padre
});

const emit = defineEmits(['close', 'save']);

const initialForm = {
  matricula: '',
  movil: '',
  marca: '',
  modelo: '',
  año: '',
  kilometros: 0,
  estado: '',
};

const form = ref({ ...initialForm });

watch(() => props.show, (newCoche) => {
  if (newCoche) {
    form.value = props.cocheData ? { ...props.cocheData } : { ...initialForm };
  }
});

const handleSave = () => emit('save', { ...form.value });
</script>

<template>
  <BaseModal 
    :show="show" 
    :title="cocheData ? 'Editar Coche' : 'Nuevo Coche'" 
    @close="!isLoading && $emit('close')"
  >
    <form class="grid grid-cols-1 md:grid-cols-2 gap-5" @submit.prevent="handleSave">
      <BaseInput 
        v-model="form.matricula"
        label="Matricula"
        :error="errors.matricula"
        placeholder="Ej: 1234"
        class="col-span-2"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.movil"
        label="Movil"
        :error="errors.movil"
        placeholder="Ej: 4321"
        class="col-span-2"
        :disabled="isLoading"
        required
      />
      <BaseInput 
        v-model="form.marca"
        label="Marca"
        :error="errors.marca"
        :disabled="isLoading"
      />
      <BaseInput 
      v-model="form.modelo"
        label="Modelo"
        :error="errors.modelo"
        :disabled="isLoading"
      />
      <BaseInput 
        v-model="form.año"
        label="Año"
        :error="errors.año"
        placeholder="Ej: 1234"
        :disabled="isLoading"
      />
      <BaseInput 
        v-model="form.kilometros"
        label="Kilometros"
        :error="errors.kilometros"
        :disabled="isLoading"
        placeholder="0"
        required
      />
      <BaseSelect 
        v-model="form.estado"
        label="Estado del Coche"
        class="col-span-2"
        :error="errors.estado"
        :options="opcionesEstado"
        :disabled="isLoading"
      />
    </form>

    <template #footer>
      <BaseButton :disabled="isLoading" @click="$emit('close')">Cancelar</BaseButton>
      <BaseButton variant="primary" :disabled="isLoading" @click="handleSave">
        {{ isLoading ? 'Guardando...' : 'Guardar Coche' }}
      </BaseButton>
    </template>
  </BaseModal>
</template>