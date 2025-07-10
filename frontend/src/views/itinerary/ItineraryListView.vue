<template>
  <div class="itinerary-list-view container mx-auto px-4 py-8 pt-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Itinerary Saya</h1>
      <router-link to="/itinerary/new"
        class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-5 rounded-lg shadow-md transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
        + Buat Itinerary Baru
      </router-link>
    </div>

    <div v-if="isLoading" class="text-center py-20">
      <svg class="animate-spin h-10 w-10 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
        </path>
      </svg>
      <p class="mt-4 text-gray-600">Memuat daftar itinerary...</p>
    </div>

    <div v-if="apiMessage.text"
      :class="['border-l-4 p-4 mb-6 rounded-md', apiMessage.type === 'error' ? 'bg-red-50 border-red-400 text-red-700' : 'bg-green-50 border-green-400 text-green-700']"
      role="alert">
      <p>{{ apiMessage.text }}</p>
    </div>

    <div v-if="!isLoading && itineraries.length === 0 && !apiMessage.text"
      class="text-center py-16 bg-white shadow-md rounded-lg">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"
        aria-hidden="true">
        <path vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
      </svg>
      <h3 class="mt-2 text-xl font-medium text-gray-900">Belum Ada Itinerary</h3>
      <p class="mt-1 text-sm text-gray-500">Mulai rencanakan perjalanan impian Anda sekarang!</p>
      <div class="mt-6">
        <router-link to="/itinerary/new"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
            aria-hidden="true">
            <path fill-rule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clip-rule="evenodd" />
          </svg>
          Buat Itinerary Baru
        </router-link>
      </div>
    </div>

    <div v-if="!isLoading && itineraries.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="itinerary in itineraries" :key="itinerary.itinerary_id"
        class="bg-white shadow-lg rounded-xl overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col">
        <div class="p-6 flex-grow">
          <h2 class="text-xl font-semibold text-gray-800 mb-2 truncate" :title="itinerary.itinerary_name">
            {{ itinerary.itinerary_name }}
          </h2>
          <p class="text-sm text-gray-500 mb-1">
            <span v-if="itinerary.start_date && itinerary.end_date">
              {{ formatDate(itinerary.start_date) }} - {{ formatDate(itinerary.end_date) }}
            </span>
            <span v-else-if="itinerary.number_of_days">
              {{ itinerary.number_of_days }} hari
            </span>
            <span v-else class="italic">Durasi belum ditentukan</span>
          </p>
          <p class="text-xs text-gray-400">Dibuat: {{ formatDate(itinerary.created_at, true) }}</p>
        </div>
        <div class="p-4 bg-gray-50 border-t border-gray-200 flex justify-end space-x-3">
          <router-link :to="{ name: 'itineraryResult', params: { id: itinerary.itinerary_id } }"
            class="text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors py-2 px-4 rounded-md hover:bg-indigo-50">
            Lihat Detail
          </router-link>
          <button @click="confirmDeleteItinerary(itinerary.itinerary_id)"
            class="text-sm font-medium text-red-600 hover:text-red-800 transition-colors py-2 px-4 rounded-md hover:bg-red-50"
            :disabled="isDeleting === itinerary.itinerary_id">
            <svg v-if="isDeleting === itinerary.itinerary_id"
              class="animate-spin -ml-1 mr-2 h-4 w-4 text-red-600 inline" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Hapus
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const itineraries = ref([]);
const isLoading = ref(true);
const isDeleting = ref(null);
const apiMessage = ref({ type: '', text: '' });

const fetchUserItineraries = async () => {
  isLoading.value = true;
  apiMessage.value = { type: '', text: '' };
  try {
    const response = await apiClient.get('/itineraries');
    itineraries.value = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (error) {
    console.error("Gagal mengambil daftar itinerary:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal memuat daftar itinerary.' };
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateString, includeTime = false) => {
  if (!dateString) return '-';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  if (includeTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
  }
  return new Date(dateString).toLocaleDateString('id-ID', options);
};

const confirmDeleteItinerary = (itineraryId) => {
  if (window.confirm("Apakah Anda yakin ingin menghapus itinerary ini? Semua data terkait akan hilang.")) {
    deleteItinerary(itineraryId);
  }
};

const deleteItinerary = async (itineraryId) => {
  isDeleting.value = itineraryId;
  apiMessage.value = { type: '', text: '' };
  try {
    await apiClient.delete(`/itineraries/${itineraryId}`);
    apiMessage.value = { type: 'success', text: 'Itinerary berhasil dihapus.' };
    itineraries.value = itineraries.value.filter(it => it.itinerary_id !== itineraryId);
    // atau fetchUserItineraries(); // untuk data yang paling update dari server
  } catch (error) {
    console.error("Gagal menghapus itinerary:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal menghapus itinerary.' };
  } finally {
    isDeleting.value = null;
  }
};

onMounted(() => {
  if (authStore.isAuthenticated) {
    fetchUserItineraries();
  } else {
    isLoading.value = false;
    apiMessage.value = { type: 'error', text: 'Anda harus login untuk melihat itinerary.' };
    // router.push('/login'); // Opsional
  }
});
</script>

<style scoped></style>
