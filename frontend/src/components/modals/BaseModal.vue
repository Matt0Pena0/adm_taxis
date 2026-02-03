<script setup>
import { onMounted, onUnmounted } from 'vue';

// Lógica de 'v-model' para abrir/cerrar
const props = defineProps({
  show: { type: Boolean, default: false },
  title: { type: String, default: 'Modal' }
});

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};

const handleEsc = (esc) => {
  if (esc.key === 'Escape' && props.show) closeModal();
}

onMounted(() => window.addEventListener('keydown', handleEsc));
onUnmounted(() => window.removeEventListener('keydown', handleEsc))

</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div 
          class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm" 
          @click="closeModal"
        ></div>

        <div class="relative w-full max-w-lg bg-white dark:bg-slate-800 rounded-2xl shadow-2xl overflow-hidden transform transition-all">
          
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">{{ title }}</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600 dark:hover:text-white transition-colors">
              <span class="i-heroicons-x-mark w-6 h-6"></span>
            </button>
          </div>

          <div class="px-6 py-4">
            <slot />
          </div>

          <div v-if="$slots.footer" class="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-700 flex justify-end gap-3">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>