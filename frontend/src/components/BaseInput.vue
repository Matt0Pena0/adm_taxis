<script setup>
// Define las props necesarias para un input genérico
defineProps({
  label: { type: String, default: '' },
  modelValue: { type: [String, Number], default: '' }, // Requerido para v-model
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: '' }
});



const formatearMensajeError = (msg) => {
  // Limpia el prefijo del ValueError técnico de Pydantic
  const cleanMsg = msg.replace("Value error, ", "");

  // Mapea los errores de "campo obligatorio"
  if (cleanMsg === "Field required" || cleanMsg.includes("valid string")) {
    return "Este campo es obligatorio.";
  }

  return cleanMsg; 
};


// Define el evento para actualizar el valor (v-model)
defineEmits(['update:modelValue']);
</script>

<template>
  <div class="flex flex-col w-full gap-1.5">
    <label 
      v-if="label" 
      class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider px-1"
    >
      {{ label }} <span v-if="required" class="text-danger">*</span>
    </label>

    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      @input="$emit('update:modelValue', $event.target.value)"
      class="dark:text-white font-medium w-full p-2.5 rounded-lg border bg-transparent transition-all outline-none 
             focus:ring-2 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
      :class="[
        error 
          ? 'border-danger focus:border-danger' 
          : 'border-slate-200 dark:border-slate-700 focus:border-primary'
      ]"
    >

    <span v-if="error" class="text-xs text-danger font-medium px-1">
      {{ error }}
    </span>
  </div>
</template>