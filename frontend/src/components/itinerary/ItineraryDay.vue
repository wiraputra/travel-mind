<template>
  <div class="itinerary-day mb-6 p-4 bg-slate-50 rounded-lg shadow">
    <div class="flex justify-between items-center mb-3">
      <h3 class="text-xl font-semibold text-slate-700">Hari Ke-{{ dayNumber }}</h3>
      <div class="space-x-2">
        <button v-if="destinationsForDay.length > 1" @click="$emit('optimize-day-route', dayNumber)"
          class="text-xs bg-teal-500 hover:bg-teal-600 text-white py-1 px-2 rounded-md shadow-sm transition-colors"
          title="Hitung rute terpendek untuk hari ini">
          Optimalkan Rute
        </button>
        <button v-if="!editingOrder && destinationsForDay.length > 1" @click="toggleEditOrderMode"
          class="text-xs bg-yellow-500 hover:bg-yellow-600 text-white py-1 px-2 rounded-md shadow-sm transition-colors">
          Ubah Urutan
        </button>
        <button v-if="editingOrder" @click="saveOrder"
          class="text-xs bg-green-500 hover:bg-green-600 text-white py-1 px-2 rounded-md shadow-sm transition-colors">
          Simpan Urutan
        </button>
        <button v-if="editingOrder" @click="cancelEditOrderMode"
          class="text-xs bg-gray-400 hover:bg-gray-500 text-white py-1 px-2 rounded-md shadow-sm transition-colors">
          Batal
        </button>
        <button @click="$emit('add-destination-to-day', dayNumber)"
          class="text-sm bg-indigo-500 hover:bg-indigo-600 text-white py-1 px-3 rounded-md shadow-sm transition-colors">
          + Tambah Destinasi
        </button>
      </div>
    </div>

    <div v-if="destinationsForDay.length === 0" class="text-center text-gray-500 py-4">
      Belum ada destinasi untuk hari ini.
    </div>

    <!-- Tampilan Normal -->
    <div v-if="!editingOrder && destinationsForDay.length > 0" class="space-y-2">
      <DestinationCard v-for="item in destinationsForDay" :key="item.item_id" :destination-item="item"
        @card-click="onCardClick" @delete-item="onDeleteItem" class="transition-all duration-300 ease-in-out" />
    </div>

    <!-- Tampilan Mode Edit Urutan -->
    <ul v-if="editingOrder && localOrderedItems.length > 0" class="space-y-2">
      <li v-for="(item, index) in localOrderedItems" :key="item.item_id"
        class="flex items-center justify-between p-3 bg-white rounded-md border border-gray-300 shadow-sm">
        <span class="text-sm text-gray-700 truncate" :title="item.destination?.name">
          {{ index + 1 }}. {{ item.destination?.name || 'Destinasi tidak valid' }}
        </span>
        <div class="flex-shrink-0 space-x-1">
          <button @click="moveItem(index, 'up')" :disabled="index === 0"
            class="p-1 rounded-full hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed" title="Naik">
            <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 3a1 1 0 00-.707.293l-3 3a1 1 0 001.414 1.414L10 5.414l2.293 2.293a1 1 0 001.414-1.414l-3-3A1 1 0 0010 3z"
                clip-rule="evenodd"></path>
            </svg>
          </button>
          <button @click="moveItem(index, 'down')" :disabled="index === localOrderedItems.length - 1"
            class="p-1 rounded-full hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed" title="Turun">
            <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 17a1 1 0 00.707-.293l3-3a1 1 0 00-1.414-1.414L10 14.586l-2.293-2.293a1 1 0 00-1.414 1.414l3 3A1 1 0 0010 17z"
                clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import DestinationCard from './DestinationCard.vue';

const props = defineProps({
  dayNumber: {
    type: Number,
    required: true,
  },
  destinationsForDay: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(['order-updated', 'card-click', 'delete-item', 'add-destination-to-day', 'optimize-day-route']);

const editingOrder = ref(false);
const localOrderedItems = ref([]);

watch(() => props.destinationsForDay, (newVal) => {
  if (!editingOrder.value) {
    localOrderedItems.value = [...newVal];
  }
}, { immediate: true, deep: true });

const toggleEditOrderMode = () => {
  editingOrder.value = true;
  localOrderedItems.value = [...props.destinationsForDay];
};

const cancelEditOrderMode = () => {
  editingOrder.value = false;
  localOrderedItems.value = [...props.destinationsForDay];
};

const saveOrder = () => {
  editingOrder.value = false;
  emit('order-updated', {
    dayNumber: props.dayNumber,
    updatedItems: localOrderedItems.value.map((item, index) => ({
      ...item,
      order_in_day: index + 1,
    })),
  });
};

const moveItem = (index, direction) => {
  const newIndex = direction === 'up' ? index - 1 : index + 1;
  if (newIndex < 0 || newIndex >= localOrderedItems.value.length) return;

  const itemToMove = localOrderedItems.value.splice(index, 1)[0];
  localOrderedItems.value.splice(newIndex, 0, itemToMove);
};

const onCardClick = (destinationItem) => {
  emit('card-click', destinationItem);
};

const onDeleteItem = (itemId) => {
  // Jika sedang edit order, mungkin perlu konfirmasi atau handle berbeda
  if (editingOrder.value) {
    const itemIndex = localOrderedItems.value.findIndex(item => item.item_id === itemId);
    if (itemIndex > -1) {
      localOrderedItems.value.splice(itemIndex, 1);
      // Tetap di mode edit, user bisa save order baru nanti
    }
  } else {
    emit('delete-item', { dayNumber: props.dayNumber, itemId });
  }
};
</script>
