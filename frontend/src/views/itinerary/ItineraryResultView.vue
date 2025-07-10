<template>
  <div class="itinerary-result-view container mx-auto px-2 sm:px-4 py-8">
    <div v-if="isLoadingPage && !itinerary" class="text-center py-20">
      <svg class="animate-spin h-10 w-10 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
        </path>
      </svg>
      <p class="mt-4 text-gray-600">Memuat detail itinerary...</p>
    </div>

    <div v-if="apiMessage.text && !isLoadingPage"
      :class="['border-l-4 p-4 mb-6 rounded-md', apiMessage.type === 'error' ? 'bg-red-50 border-red-400 text-red-700' : 'bg-green-50 border-green-400 text-green-700']"
      role="alert">
      <p>{{ apiMessage.text }}</p>
    </div>

    <div v-if="itinerary && !isLoadingPage">
      <!-- Header Itinerary -->
      <div class="bg-white shadow-lg rounded-lg p-6 mb-8">
        <div class="flex justify-between items-start mb-1">
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-800">
            {{ itinerary.itinerary_name }}
          </h1>
          <button @click="openEditItineraryModal" class="btn-outline btn-sm text-xs p-2" title="Edit Detail Itinerary">
            <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
              </path>
            </svg>
            Edit
          </button>
        </div>
        <p class="text-sm text-gray-500 mb-4">
          <span v-if="itinerary.start_date && itinerary.end_date">
            {{ formatDate(itinerary.start_date) }} - {{ formatDate(itinerary.end_date) }}
            <span v-if="itinerary.number_of_days">({{ itinerary.number_of_days }} hari)</span>
          </span>
          <span v-else-if="itinerary.number_of_days">
            {{ itinerary.number_of_days }} hari
          </span>
          <span v-else class="italic">Durasi belum ditentukan</span>
        </p>
        <p v-if="itinerary.notes" class="text-gray-700 text-sm whitespace-pre-line bg-gray-50 p-3 rounded-md">{{
          itinerary.notes }}</p>
      </div>

      <!-- Layout Kolom Kiri (Hari & Destinasi) dan Kolom Kanan (Peta) -->
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Kolom Kiri: Daftar Hari dan Destinasi -->
        <div class="w-full lg:w-2/5 xl:w-1/3 space-y-1 itinerary-days-list">
          <div v-if="isLoadingItems" class="text-center py-10">
            <svg class="animate-spin h-6 w-6 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            <p class="text-sm text-gray-500 mt-2">Memuat item...</p>
          </div>
          <div
            v-if="!isLoadingItems && (!itinerary.items || groupedItemsByDay.size === 0) && (itinerary.number_of_days === 0 || !itinerary.number_of_days)"
            class="text-center p-4 bg-slate-100 rounded-lg">
            <p class="text-gray-500 mb-2">Itinerary ini belum memiliki hari.</p>
            <button @click="promptNumberOfDays"
              class="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded text-sm">
              Tentukan Jumlah Hari
            </button>
          </div>
          <div
            v-if="!isLoadingItems && (!itinerary.items || groupedItemsByDay.size === 0) && itinerary.number_of_days > 0"
            class="text-center p-4 bg-slate-100 rounded-lg">
            <p class="text-gray-500">Belum ada rencana untuk itinerary ini.</p>
            <p class="text-xs text-gray-400 mt-1">Klik "+ Tambah Destinasi" pada hari yang diinginkan.</p>
          </div>

          <div v-if="!isLoadingItems && itinerary.number_of_days > 0"
            class="space-y-4 max-h-[calc(100vh-250px)] overflow-y-auto pr-2 custom-scrollbar">
            <ItineraryDay v-for="dayNumber in Array.from({ length: itinerary.number_of_days || 0 }, (_, i) => i + 1)"
              :key="dayNumber" :day-number="dayNumber" :destinations-for-day="getDestinationsForDay(dayNumber)"
              @order-updated="handleOrderUpdated" @card-click="handleCardClick" @delete-item="confirmDeleteItem"
              @add-destination-to-day="openAddDestinationModal" @optimize-day-route="handleOptimizeDayRoute" />
          </div>
        </div>

        <!-- Kolom Kanan: Peta -->
        <div class="w-full lg:w-3/5 xl:w-2/3 h-[50vh] lg:h-[calc(100vh-150px)] lg:sticky lg:top-24">
          <div id="mapContainer" class="w-full h-full rounded-lg shadow-lg border bg-gray-200">
            <l-map v-if="mapReady" ref="mapRef" :zoom="mapZoom" :center="mapCenter" style="height: 100%; width: 100%">
              <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
                name="OpenStreetMap"
                :attribution="'© <a href=\'http://osm.org/copyright\'>OpenStreetMap</a> contributors'"></l-tile-layer>
              <l-marker v-for="item in allMapMarkers" :key="item.item_id" :lat-lng="item.latLng"
                @click="focusOnItem(item)">
                <l-popup>
                  <b>{{ item.destination?.name }}</b><br />
                  Hari Ke-{{ item.day_number }} (Urutan {{ item.order_in_day }})
                </l-popup>
                <l-tooltip>{{ item.destination?.name }}</l-tooltip>
              </l-marker>
              <l-polyline v-for="(route, day) in routePolylines" :key="'route-ors-' + day" :lat-lngs="route.latLngs"
                :color="route.color" :weight="5" opacity="0.7"></l-polyline>
            </l-map>
            <div v-else class="flex items-center justify-center h-full text-gray-500">
              Memuat peta...
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!itinerary && !isLoadingPage && !apiMessage.text" class="text-center py-20">
      <p class="text-xl text-gray-500">Itinerary tidak ditemukan.</p>
      <router-link to="/itinerary/my-list" class="mt-4 inline-block text-indigo-600 hover:text-indigo-500">Kembali ke
        Daftar Itinerary</router-link>
    </div>

    <!-- Modal Edit Itinerary Detail -->
    <div v-if="showEditModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full z-50 flex items-center justify-center"
      @click.self="closeEditItineraryModal">
      <div class="relative mx-auto p-5 border w-full max-w-lg shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-xl leading-6 font-medium text-gray-900 mb-6 text-center">Edit Detail Itinerary</h3>

          <form @submit.prevent="handleUpdateItineraryDetails" class="space-y-4">
            <div v-if="editApiMessage.text"
              :class="['alert text-sm', editApiMessage.type === 'error' ? 'alert-error' : 'alert-success']">
              {{ editApiMessage.text }}
            </div>

            <div>
              <label for="edit_itinerary_name" class="input-label">Nama Itinerary <span
                  class="text-red-500">*</span></label>
              <input type="text" id="edit_itinerary_name" v-model="editableItinerary.itinerary_name" required
                class="input-field" />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="edit_start_date" class="input-label">Tanggal Mulai</label>
                <input type="date" id="edit_start_date" v-model="editableItinerary.start_date" class="input-field" />
              </div>
              <div>
                <label for="edit_end_date" class="input-label">Tanggal Selesai</label>
                <input type="date" id="edit_end_date" v-model="editableItinerary.end_date"
                  :min="editableItinerary.start_date" class="input-field" />
              </div>
            </div>

            <div>
              <label for="edit_number_of_days" class="input-label">Jumlah Hari (Opsional)</label>
              <input type="number" id="edit_number_of_days" v-model.number="editableItinerary.number_of_days" min="1"
                class="input-field" />
              <p class="mt-1 text-xs text-gray-500">Jika tanggal diisi, jumlah hari akan dihitung otomatis. Isi ini jika
                tidak menggunakan tanggal spesifik.</p>
            </div>

            <div>
              <label for="edit_notes" class="input-label">Catatan Tambahan</label>
              <textarea id="edit_notes" v-model="editableItinerary.notes" rows="3" class="input-field"></textarea>
            </div>

            <div class="pt-4 flex justify-end space-x-3">
              <button type="button" @click="closeEditItineraryModal" class="btn btn-outline">Batal</button>
              <button type="submit" :disabled="isUpdatingItinerary" class="btn btn-primary">
                <svg v-if="isUpdatingItinerary" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                  </path>
                </svg>
                Simpan Perubahan
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal Tambah Destinasi -->
    <AddDestinationModal :show="showAddModal" :target-day="targetDayForModal" @close="showAddModal = false"
      @destination-selected="handleDestinationSelected" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import ItineraryDay from '@/components/itinerary/ItineraryDay.vue';
import AddDestinationModal from '@/components/itinerary/AddDestinationModal.vue';

import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup, LTooltip, LPolyline } from "@vue-leaflet/vue-leaflet";
import L from 'leaflet';

const route = useRoute();
const router = useRouter();
const itinerary = ref(null);
const isLoadingPage = ref(true);
const isLoadingItems = ref(false);
const apiMessage = ref({ type: '', text: '' });

const showAddModal = ref(false);
const targetDayForModal = ref(null);

// State untuk Edit Itinerary Modal
const showEditModal = ref(false);
const isUpdatingItinerary = ref(false);
const editApiMessage = ref({ type: '', text: '' });
const editableItinerary = reactive({
  itinerary_id: null,
  itinerary_name: '',
  start_date: '',
  end_date: '',
  number_of_days: null,
  notes: '',
});

const mapReady = ref(false);
const mapRef = ref(null);
const mapZoom = ref(6);
const mapCenter = ref([-2.548926, 118.0148634]); // Default Indonesia
const defaultMapCenter = [-2.548926, 118.0148634];
const defaultZoom = 6;

const itineraryId = computed(() => route.params.id);

const routePolylines = ref({});
const userLocation = ref(null)
const isOptimizing = ref(null);

const fetchItineraryDetail = async () => {
  isLoadingPage.value = true;
  apiMessage.value = { type: '', text: '' };
  if (!itineraryId.value) {
    apiMessage.value = { type: 'error', text: 'ID Itinerary tidak valid.' };
    itinerary.value = null;
    isLoadingPage.value = false;
    return;
  }
  try {
    const response = await apiClient.get(`/itineraries/${itineraryId.value}`);
    itinerary.value = response.data;
    if (itinerary.value && itinerary.value.items) {
      updateMapFocus();
    }
    mapReady.value = true;
  } catch (error) {
    console.error("Gagal mengambil detail itinerary:", error);
    itinerary.value = null;
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal memuat itinerary.' };
  } finally {
    isLoadingPage.value = false;
  }
};

// Fungsi untuk membuka modal edit dan mengisi form
const openEditItineraryModal = () => {
  if (itinerary.value) {
    editableItinerary.itinerary_id = itinerary.value.itinerary_id;
    editableItinerary.itinerary_name = itinerary.value.itinerary_name;
    editableItinerary.start_date = itinerary.value.start_date ? itinerary.value.start_date.split('T')[0] : '';
    editableItinerary.end_date = itinerary.value.end_date ? itinerary.value.end_date.split('T')[0] : '';
    editableItinerary.number_of_days = itinerary.value.number_of_days;
    editableItinerary.notes = itinerary.value.notes || '';
    editApiMessage.value = { type: '', text: '' };
    showEditModal.value = true;
  }
};

const closeEditItineraryModal = () => {
  showEditModal.value = false;
};

const handleUpdateItineraryDetails = async () => {
  isUpdatingItinerary.value = true;
  editApiMessage.value = { type: '', text: '' };

  if (!editableItinerary.itinerary_name) {
    editApiMessage.value = { type: 'error', text: 'Nama itinerary tidak boleh kosong.' };
    isUpdatingItinerary.value = false;
    return;
  }
  // Validasi tanggal jika ada
  if ((editableItinerary.start_date && !editableItinerary.end_date) || (!editableItinerary.start_date && editableItinerary.end_date)) {
    editApiMessage.value = { type: 'error', text: 'Jika mengisi satu tanggal, tanggal lainnya juga harus diisi.' };
    isUpdatingItinerary.value = false;
    return;
  }
  if (editableItinerary.start_date && editableItinerary.end_date && new Date(editableItinerary.end_date) < new Date(editableItinerary.start_date)) {
    editApiMessage.value = { type: 'error', text: 'Tanggal selesai tidak boleh sebelum tanggal mulai.' };
    isUpdatingItinerary.value = false;
    return;
  }
  // Jika tanggal tidak diisi, number_of_days harus diisi
  if (!editableItinerary.start_date && !editableItinerary.end_date && (!editableItinerary.number_of_days || editableItinerary.number_of_days < 1)) {
    editApiMessage.value = { type: 'error', text: 'Isi tanggal mulai & selesai, atau jumlah hari yang valid.' };
    isUpdatingItinerary.value = false;
    return;
  }


  const payload = {
    itinerary_name: editableItinerary.itinerary_name,
    start_date: editableItinerary.start_date || null, // Kirim null jika kosong
    end_date: editableItinerary.end_date || null,     // Kirim null jika kosong
    number_of_days: editableItinerary.number_of_days || null,
    notes: editableItinerary.notes,
    // preferences tidak diubah di sini, jadi tidak perlu dikirim
  };
  // Jika tanggal diisi, backend akan menghitung number_of_days, jadi kita bisa set number_of_days ke null jika tanggal ada
  if (payload.start_date && payload.end_date) {
    payload.number_of_days = null;
  }


  try {
    const response = await apiClient.put(`/itineraries/${editableItinerary.itinerary_id}`, payload);
    itinerary.value = { ...itinerary.value, ...response.data }; // Update data itinerary utama dengan respons
    // (Backend harus mengembalikan objek itinerary yang diupdate)
    editApiMessage.value = { type: 'success', text: 'Detail itinerary berhasil diperbarui!' };
    setTimeout(() => {
      closeEditItineraryModal();
    }, 1500); // Tutup modal setelah pesan sukses
  } catch (error) {
    console.error("Gagal update detail itinerary:", error);
    editApiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal memperbarui detail.' };
  } finally {
    isUpdatingItinerary.value = false;
  }
};

const groupedItemsByDay = computed(() => {
  if (!itinerary.value || !itinerary.value.items) {
    return new Map();
  }
  const groups = new Map();
  const sortedItems = [...itinerary.value.items].sort((a, b) => {
    if (a.day_number === b.day_number) {
      return a.order_in_day - b.order_in_day;
    }
    return a.day_number - b.day_number;
  });

  sortedItems.forEach(item => {
    if (!groups.has(item.day_number)) {
      groups.set(item.day_number, []);
    }
    groups.get(item.day_number).push(item);
  });
  return groups;
});

const getDestinationsForDay = (dayNumber) => {
  return groupedItemsByDay.value.get(dayNumber) || [];
};

const allMapMarkers = computed(() => {
  if (!itinerary.value || !itinerary.value.items) return [];
  return itinerary.value.items
    .filter(item => item.destination && item.destination.latitude != null && item.destination.longitude != null)
    .map(item => ({
      ...item,
      latLng: [parseFloat(item.destination.latitude), parseFloat(item.destination.longitude)],
    }));
});

const dailyRoutes = computed(() => {
  const routes = {};
  if (!itinerary.value || !itinerary.value.items || itinerary.value.items.length < 1) return routes;

  const colors = ['#3B82F6', '#EF4444', '#10B981', '#8B5CF6', '#F59E0B', '#06B6D4', '#EC4899']; // Tailwind colors

  groupedItemsByDay.value.forEach((itemsInDay, dayNumber) => {
    const validCoords = itemsInDay
      .filter(item => item.destination && item.destination.latitude != null && item.destination.longitude != null)
      .map(item => [parseFloat(item.destination.latitude), parseFloat(item.destination.longitude)]);

    if (validCoords.length > 1) {
      routes[dayNumber] = {
        latLngs: validCoords,
        color: colors[(dayNumber - 1) % colors.length]
      };
    }
  });
  return routes;
});

const updateMapFocus = async () => {
  await nextTick();
  if (mapReady.value && mapRef.value && mapRef.value.leafletObject) {
    const mapInstance = mapRef.value.leafletObject;
    if (allMapMarkers.value.length > 0) {
      const bounds = L.latLngBounds(allMapMarkers.value.map(marker => marker.latLng));
      if (bounds.isValid()) {
        mapInstance.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
      } else if (allMapMarkers.value.length === 1) {
        mapInstance.setView(allMapMarkers.value[0].latLng, 13);
      }
    } else {
      mapInstance.setView(defaultMapCenter, defaultZoom);
    }
  } else if (allMapMarkers.value.length > 0) {
    const firstMarker = allMapMarkers.value[0];
    mapCenter.value = firstMarker.latLng;
    mapZoom.value = 13;
  } else {
    mapCenter.value = defaultMapCenter;
    mapZoom.value = defaultZoom;
  }
};

const handleCardClick = async (destinationItem) => {
  if (destinationItem.destination && destinationItem.destination.latitude != null && destinationItem.destination.longitude != null) {
    const latLng = [parseFloat(destinationItem.destination.latitude), parseFloat(destinationItem.destination.longitude)];
    if (mapReady.value && mapRef.value && mapRef.value.leafletObject) {
      await nextTick();
      mapRef.value.leafletObject.flyTo(latLng, 15);
    } else {
      mapCenter.value = latLng;
      mapZoom.value = 15;
    }
  }
};

const focusOnItem = (item) => {
  if (item.latLng) {
    if (mapReady.value && mapRef.value && mapRef.value.leafletObject) {
      mapRef.value.leafletObject.flyTo(item.latLng, 15);
    } else {
      mapCenter.value = item.latLng;
      mapZoom.value = 15;
    }
  }
}

const openAddDestinationModal = (dayNumber) => {
  targetDayForModal.value = dayNumber;
  showAddModal.value = true;
};

const handleDestinationSelected = async ({ destinationId, dayNumber }) => {
  if (!itinerary.value) return;
  isLoadingItems.value = true;
  apiMessage.value = { type: '', text: '' };
  try {
    const response = await apiClient.post(`/itineraries/${itinerary.value.itinerary_id}/items`, {
      destination_id: destinationId,
      day_number: dayNumber,
    });
    apiMessage.value = { type: 'success', text: response.data.msg || 'Destinasi berhasil ditambahkan!' };
    await fetchItineraryDetail(); // Refresh
  } catch (error) {
    console.error("Error adding destination:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal menambahkan destinasi.' };
  } finally {
    isLoadingItems.value = false;
  }
  showAddModal.value = false;
};

const confirmDeleteItem = async ({ dayNumber, itemId }) => {
  if (window.confirm("Anda yakin ingin menghapus destinasi ini dari itinerary?")) {
    isLoadingItems.value = true;
    apiMessage.value = { type: '', text: '' };
    try {
      const response = await apiClient.delete(`/itineraries/${itinerary.value.itinerary_id}/items/${itemId}`);
      apiMessage.value = { type: 'success', text: response.data.msg || 'Destinasi berhasil dihapus.' };
      await fetchItineraryDetail(); // Refresh
    } catch (error) {
      console.error("Error deleting item:", error);
      apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal menghapus destinasi.' };
    } finally {
      isLoadingItems.value = false;
    }
  }
};

const handleOrderUpdated = async ({ dayNumber, updatedItems }) => {
  if (!itinerary.value) return;
  isLoadingItems.value = true;
  apiMessage.value = { type: '', text: '' };

  // Membangun payload untuk endpoint /reorder
  // Ambil semua item dari state saat ini, lalu update yang dari hari yang diubah
  const currentItemsMap = new Map(itinerary.value.items.map(item => [item.item_id, item]));
  updatedItems.forEach(updItem => {
    if (currentItemsMap.has(updItem.item_id)) {
      currentItemsMap.set(updItem.item_id, { ...currentItemsMap.get(updItem.item_id), ...updItem });
    }
  });

  const reorderPayload = Array.from(currentItemsMap.values()).map(item => ({
    item_id: item.item_id,
    day_number: item.day_number,
    order_in_day: item.order_in_day,
  }));

  try {
    const response = await apiClient.put(
      `/itineraries/${itinerary.value.itinerary_id}/items/reorder`,
      reorderPayload
    );
    apiMessage.value = { type: 'success', text: response.data.msg || 'Urutan berhasil disimpan.' };
    await fetchItineraryDetail();
  } catch (error) {
    console.error("Error reordering items:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal menyimpan urutan.' };
    await fetchItineraryDetail();
  } finally {
    isLoadingItems.value = false;
  }
};

const promptNumberOfDays = async () => {
  const days = window.prompt("Masukkan jumlah hari untuk itinerary ini:", itinerary.value?.number_of_days || 1);
  if (days !== null) {
    const numDays = parseInt(days);
    if (!isNaN(numDays) && numDays > 0) {
      try {
        isLoadingPage.value = true;
        apiMessage.value = { type: '', text: '' };
        await apiClient.put(`/itineraries/${itinerary.value.itinerary_id}`, {
          number_of_days: numDays,
          itinerary_name: itinerary.value.itinerary_name,
          start_date: itinerary.value.start_date,
          end_date: itinerary.value.end_date,
          notes: itinerary.value.notes,
        });
        await fetchItineraryDetail();
        apiMessage.value = { type: 'success', text: 'Jumlah hari berhasil diupdate.' };
      } catch (error) {
        apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal mengupdate jumlah hari.' };
      } finally {
        isLoadingPage.value = false;
      }
    } else {
      alert("Jumlah hari tidak valid.");
    }
  }
};

const formatDate = (dateString, includeTime = false) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  if (includeTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
  }
  return new Date(dateString).toLocaleDateString('id-ID', options);
};

const getUserLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        apiMessage.value = { type: 'success', text: 'Lokasi Anda berhasil dideteksi.' };
        setTimeout(() => { apiMessage.value = { type: '', text: '' } }, 3000);
      },
      (error) => {
        console.error("Error mendapatkan lokasi:", error);
        apiMessage.value = { type: 'info', text: 'Izinkan akses lokasi di browser Anda untuk menggunakan fitur optimasi rute.' };
      }
    );
  } else {
    apiMessage.value = { type: 'error', text: 'Geolocation tidak didukung oleh browser ini.' };
  }
};

const handleOptimizeDayRoute = async (dayNumber) => {
  if (!userLocation.value) {
    getUserLocation();
    alert("Lokasi Anda sedang dideteksi. Harap izinkan akses lokasi di browser Anda dan coba lagi.");
    return;
  }

  isOptimizing.value = dayNumber;
  apiMessage.value = { type: '', text: '' };

  try {
    const response = await apiClient.post(
      `/itineraries/${itineraryId.value}/days/${dayNumber}/optimize-route`,
      {
        start_coords: [userLocation.value.longitude, userLocation.value.latitude],
      }
    );

    const { route_geometry, distance_meters, duration_seconds } = response.data;

    const leafletCoords = route_geometry.coordinates.map(coord => [coord[1], coord[0]]);

    const colors = ['#3B82F6', '#EF4444', '#10B981', '#8B5CF6', '#F59E0B', '#06B6D4', '#EC4899'];

    routePolylines.value[dayNumber] = {
      latLngs: leafletCoords,
      color: colors[(dayNumber - 1) % colors.length]
    };

    if (mapRef.value && mapRef.value.leafletObject) {
      const routeBounds = L.latLngBounds(leafletCoords);
      if (routeBounds.isValid()) {
        mapRef.value.leafletObject.fitBounds(routeBounds, { padding: [50, 50] });
      }
    }

    apiMessage.value = { type: 'success', text: `Rute untuk Hari Ke-${dayNumber} berhasil dibuat! Estimasi: ${(distance_meters / 1000).toFixed(1)} km / ${Math.round(duration_seconds / 60)} menit.` };

  } catch (error) {
    console.error("Gagal mengoptimalkan rute:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || `Gagal membuat rute untuk Hari Ke-${dayNumber}.` };
  } finally {
    isOptimizing.value = null;
  }
};

onMounted(() => {
  fetchItineraryDetail();
  getUserLocation();
});

watch(itineraryId, (newId, oldId) => {
  if (newId && newId !== oldId) {
    mapReady.value = false;
    fetchItineraryDetail();
  }
});

watch(allMapMarkers, () => {
  updateMapFocus();
}, { deep: true });

</script>

<style scoped>
#mapContainer {
  min-height: 400px;
}

.lg\:sticky {

  /* Untuk browser yang tidak support Tailwind JIT v3 penuh untuk sticky */
  @media (min-width: 1024px) {
    position: sticky;
  }
}

.lg\:top-24 {
  @media (min-width: 1024px) {
    top: 6rem;
  }
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #9ca3af;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #6b7280;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background-color: #f3f4f6;
}

.itinerary-days-list {
  max-height: 70vh;
}

@media (min-width: 1024px) {
  .itinerary-days-list {
    max-height: calc(100vh - theme('spacing.24') - 60px);
  }
}
</style>
