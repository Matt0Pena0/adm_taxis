<!-- <script setup>
import BaseCard from '@/components/BaseCard.vue';
import BaseButton from '@/components/BaseButton.vue';


// Propiedades que recibe la tarjeta
const props = defineProps({
  coche: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit'])

</script>

<template>
  <BaseCard>

    <div class="absolute top-1 right-2">
      <span 
      class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border"
      :class="coche.estado === 'Activo' 
        ? 'bg-green-100 text-green-700 border-green-200 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800' 
        : 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700'">
      {{ coche.estado || 'Desconocido' }}
      </span>
    </div>
    
    <div class="p-6 flex flex-col items-center text-center border-b border-border-light dark:border-border-dark relative">

      <div class="size-20 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center mb-2 ring-4 ring-surface-light dark:ring-surface-dark group-hover:scale-110 transition-transform duration-300 group-hover:bg-primary/10 group-hover:text-primary">
        <span class="material-symbols-outlined text-4xl text-slate-400 dark:text-slate-500 group-hover:text-primary transition-colors">directions_car</span>
      </div>
      
      <h3 class="h-16 w-full flex items-center justify-center font-bold text-lg text-slate-900 dark:text-white leading-tight line-clamp-2 overflow-hidden px-2 uppercase">
        STX {{ coche.matricula }}
      </h3>

      <span class="text-xs text-slate-500 dark:text-slate-400">
        {{ coche.marca }} {{ coche.modelo }}
      </span>
      
    </div>

    <div class="mx-3 p-1 px-3 bg-slate-50 dark:bg-black/20 flex-1 flex flex-col gap-1">
      <div class="flex items-center justify-between">
        <span class="text-xxs font-medium text-slate-500 dark:text-slate-400 tracking-wide leading-tight">
          Movil:
        </span>
        <span class="text-xs font-mono font-medium text-slate-700 dark:text-slate-200">
          {{ coche.movil || '---' }}
        </span>
      </div>
    </div>

    <div class="p-3">

      <BaseButton icon="heroicons:pencil" 
      :full-width="true"
      @click="$emit('edit', coche)"
      >
        Editar Coche
      </BaseButton>

    </div>

  </BaseCard>
</template> -->
