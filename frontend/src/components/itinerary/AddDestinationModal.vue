<template>
  <div v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center"
    @click.self="closeModal">
    <div class="relative mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
      <div class="mt-3 text-center">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Tambah Destinasi ke Hari Ke-{{ targetDay }}</h3>

        <!-- Input Pencarian Destinasi -->
        <div class="my-4 px-2">
          <input type="text" v-model="searchTerm" @input="debouncedSearchDestinations"
            placeholder="Cari nama destinasi..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
        </div>

        <!-- Daftar Hasil Pencarian -->
        <div class="max-h-60 overflow-y-auto border rounded-md" v-if="!searchLoading">
          <ul v-if="searchResults.length > 0" class="divide-y divide-gray-200">
            <li v-for="dest in searchResults" :key="dest.destination_id" @click="selectDestination(dest)"
              class="p-3 hover:bg-gray-100 cursor-pointer text-left">
              <p class="font-semibold text-sm text-gray-800">{{ dest.name }}</p>
              <p class="text-xs text-gray-500">{{ dest.city }}, {{ dest.country }}</p>
            </li>
          </ul>
          <p v-else-if="searchTerm && !searchLoading" class="text-gray-500 p-4">
            Tidak ada destinasi ditemukan untuk "{{ searchTerm }}".
          </p>
          <p v-else-if="!searchTerm && !searchLoading" class="text-gray-500 p-4">
            Mulai ketik untuk mencari destinasi.
          </p>
        </div>
        <div v-if="searchLoading" class="text-center py-4">
          <svg class="animate-spin h-6 w-6 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
        </div>

        <!-- Tombol Aksi -->
        <div class="items-center px-4 py-3 mt-4">
          <button @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 mr-2">
            Batal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import apiClient from '@/services/api';
import { debounce } from 'lodash-es';

const props = defineProps({
  show: Boolean,
  targetDay: Number,
});
const emit = defineEmits(['close', 'destination-selected']);

const searchTerm = ref('');
const searchResults = ref([]);
const searchLoading = ref(false);

const searchDestinations = async () => {
  if (!searchTerm.value || searchTerm.value.length < 2) {
    searchResults.value = [];
    return;
  }
  searchLoading.value = true;
  try {
    const response = await apiClient.get('/destinations', { params: { q: searchTerm.value, per_page: 10 } });
    searchResults.value = response.data.destinations;
  } catch (error) {
    console.error("Error searching destinations:", error);
    searchResults.value = [];
  } finally {
    searchLoading.value = false;
  }
};

// Gunakan debounce untuk mencegah API call pada setiap ketikan
const debouncedSearchDestinations = debounce(searchDestinations, 500);

const selectDestination = (destination) => {
  emit('destination-selected', { destinationId: destination.destination_id, dayNumber: props.targetDay });
  closeModalAndReset();
};

const closeModal = () => {
  emit('close');
};

const closeModalAndReset = () => {
  closeModal();
  searchTerm.value = '';
  searchResults.value = [];
}

watch(() => props.show, (newVal) => {
  if (!newVal) { // Jika modal ditutup, reset state
    searchTerm.value = '';
    searchResults.value = [];
  }
});
</script>
