<script setup>
defineProps({
  label: String,
  modelValue: [String, Number],
  options: { type: Array, default: () => [] },
  error: String,
  required: Boolean,
  disabled: Boolean
});

defineEmits(['update:modelValue']);
</script>

<template>
  <div class="flex flex-col w-full gap-1.5">
    <label v-if="label" class="text-xs font-bold text-slate-500 uppercase px-1">
      {{ label }} <span v-if="required" class="text-danger">*</span>
    </label>

    <select
      :value="modelValue"
      :disabled="disabled"
      @change="$emit('update:modelValue', $event.target.value)"
      class="text-white w-full p-2.5 rounded-lg border dark:bg-slate-800 transition-all outline-none focus:ring-2 focus:ring-primary/20 appearance-none"
      :class="[
        error ? 'border-danger' : 'border-slate-200 dark:border-slate-700 focus:border-primary',
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      ]"
    >
      <option value="" disabled selected class="text-primary-light">Seleccione una opción</option>
      <option 
        v-for="opt in options" 
        :key="typeof opt === 'object' ? opt.value : opt" 
        :value="typeof opt === 'object' ? opt.value : opt"
      >
        {{ typeof opt === 'object' ? opt.label : opt }}
      </option>
    </select>

    <span v-if="error" class="text-xs text-danger font-medium px-1">{{ error }}</span>
  </div>
</template>