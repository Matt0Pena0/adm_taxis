<script setup>
import { Icon } from '@iconify/vue';
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
  to: {
    type: [String, Object],
    default: null
  },
  variant: {
    type: String,
    default: 'outline'
  },
  icon: {
    type: String,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
});

// 1. CLASES BASE
const baseClasses = "flex items-center justify-center p-2 px-2 rounded-lg border border-border-light dark:border-border-dark text-sm font-bold transition-colors gap-2 focus:outline-none disabled:opacity-50";

// 2. VARIANTES
const variants = {
  outline: "bg-primary hover:bg-primary-dark text-on-primary border-border-light dark:border-border-dark text-sm font-extrabold text-slate-600 hover:bg-primary hover:text-slate-600 dark:hover:text-on-primary dark:text-on-primary hover:border-primary focus:outline-none disabled:opacity-50",
  
  primary: "bg-primary text-slate-900 border-primary hover:bg-primary-dark font-bold",
  
  danger: "bg-danger text-white border-danger hover:bg-danger-dark font-bold"
};

// 2. LÓGICA DE ANCHO
const widthClass = computed(() => props.fullWidth ? 'w-full' : 'w-fit');

const buttonClasses = computed(() => {
  return `${baseClasses} ${variants[props.variant] || variants.outline} ${widthClass.value}`;
});
</script>

<template>
  <component
    :is="to ? RouterLink : 'button'"
    :to="to"
    :class="buttonClasses"
    :disabled="disabled"
  >
    <div v-if="icon || $slots.icon" class="flex items-center justify-center flex-shrink-0 w-5 h-5">
      <slot name="icon">
        <Icon v-if="icon" :icon="icon" class="w-full h-full" />
      </slot>
    </div>

    <span class="inline-block">
      <slot />
    </span>
  </component>
</template>