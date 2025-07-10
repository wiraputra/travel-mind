<template>
  <div class="create-itinerary-view container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto bg-white shadow-xl rounded-lg p-6 md:p-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Buat Itinerary Cerdas</h1>
      <p class="text-center text-gray-600 mb-8 -mt-4">
        Biarkan AI kami membantu merancang perjalanan Anda!
      </p>

      <form @submit.prevent="handleCreateItineraryWithAI" class="space-y-6">
        <div v-if="apiMessage.text" :class="['alert', apiMessage.type === 'error' ? 'alert-error' : 'alert-success']"
          role="alert">
          <p>{{ apiMessage.text }}</p>
        </div>

        <div>
          <label for="itinerary_name" class="input-label">Nama Itinerary <span class="text-red-500">*</span></label>
          <input type="text" id="itinerary_name" v-model="form.itinerary_name" required class="input-field"
            placeholder="Contoh: Petualangan Bali 3 Hari" />
        </div>

        <div>
          <label for="destination_city" class="input-label">Kota/Wilayah Tujuan Utama <span
              class="text-red-500">*</span></label>
          <input type="text" id="destination_city" v-model="form.preferences.destination_city" required
            class="input-field" placeholder="Contoh: Ubud, Bali atau Yogyakarta" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="start_date" class="input-label">Tanggal Mulai</label>
            <input type="date" id="start_date" v-model="form.start_date" class="input-field" />
          </div>
          <div>
            <label for="end_date" class="input-label">Tanggal Selesai</label>
            <input type="date" id="end_date" v-model="form.end_date" :min="form.start_date" class="input-field" />
          </div>
        </div>

        <div>
          <label for="number_of_days" class="input-label">Jumlah Hari (Jika tidak mengisi tanggal)</label>
          <input type="number" id="number_of_days" v-model.number="form.number_of_days" min="1" class="input-field"
            placeholder="Contoh: 3" />
          <p class="mt-1 text-xs text-gray-500">Kosongkan jika sudah mengisi tanggal mulai dan selesai. Akan dihitung
            otomatis.</p>
        </div>

        <!-- Preferensi AI -->
        <div class="pt-6 border-t mt-6">
          <h3 class="text-xl font-semibold text-gray-700 mb-1">Preferensi Perjalanan Anda</h3>
          <p class="text-sm text-gray-500 mb-4">Bantu AI kami merancang itinerary terbaik.</p>

          <div class="space-y-4">
            <div>
              <label class="input-label">Minat Utama (Pilih beberapa):</label>
              <div class="mt-2 grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-2">
                <label v-for="interest in availableInterests" :key="interest.value"
                  class="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded-md">
                  <input type="checkbox" :value="interest.value" v-model="form.preferences.interests"
                    class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500">
                  <span class="text-sm text-gray-700">{{ interest.label }}</span>
                </label>
              </div>
            </div>

            <div>
              <label class="input-label">Gaya Perjalanan / Pace:</label>
              <div class="mt-2 flex flex-wrap gap-x-6 gap-y-2">
                <label v-for="paceOption in availablePaces" :key="paceOption.value"
                  class="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded-md">
                  <input type="radio" :value="paceOption.value" v-model="form.preferences.pace" name="pace"
                    class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                  <span class="text-sm text-gray-700">{{ paceOption.label }}</span>
                </label>
              </div>
            </div>

            <div>
              <label class="input-label">Estimasi Budget:</label>
              <div class="mt-2 flex flex-wrap gap-x-6 gap-y-2">
                <label v-for="budgetOption in availableBudgets" :key="budgetOption.value"
                  class="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded-md">
                  <input type="radio" :value="budgetOption.value" v-model="form.preferences.budget" name="budget"
                    class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                  <span class="text-sm text-gray-700">{{ budgetOption.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <div>
            <label class="input-label">Tipe Perjalanan:</label>
            <div class="mt-2 flex flex-wrap gap-x-6 gap-y-2">
              <label v-for="tripType in availableTripTypes" :key="tripType.value"
                class="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded-md">
                <input type="radio" :value="tripType.value" v-model="form.preferences.trip_type" name="trip_type"
                  class="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500">
                <span class="text-sm text-gray-700">{{ tripType.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <div>
          <label for="notes" class="input-label">Catatan Tambahan (Opsional)</label>
          <textarea id="notes" v-model="form.notes" rows="3" class="input-field"
            placeholder="Contoh: Tidak suka tempat ramai, ingin coba kuliner lokal pedas, alergi seafood, dll."></textarea>
        </div>


        <div class="pt-8">
          <button type="submit" :disabled="isLoading" class="btn-primary w-full text-base">
            <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
              fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Generate Itinerary dengan AI
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/services/api';

const router = useRouter();

const form = reactive({
  itinerary_name: '',
  start_date: '',
  end_date: '',
  number_of_days: null,
  notes: '',
  preferences: {
    destination_city: '',
    interests: [],
    pace: 'sedang',
    budget: 'sedang',
    tripType: 'solo'
  },
});

const isLoading = ref(false);
const apiMessage = ref({ type: '', text: '' });

const availableInterests = ref([
  { label: 'Alam & Pemandangan', value: 'alam' },
  { label: 'Sejarah & Budaya', value: 'sejarah' },
  { label: 'Kuliner', value: 'kuliner' },
  { label: 'Belanja', value: 'belanja' },
  { label: 'Seni & Museum', value: 'seni' },
  { label: 'Hiburan & Relaksasi', value: 'hiburan' },
  { label: 'Petualangan', value: 'petualangan' },
]);

const availablePaces = ref([
  { label: 'Santai (1-2 destinasi/hari)', value: 'santai' },
  { label: 'Sedang (2-3 destinasi/hari)', value: 'sedang' },
  { label: 'Padat (3+ destinasi/hari)', value: 'padat' },
]);

const availableBudgets = ref([
  { label: 'Hemat (Backpacker)', value: 'hemat' },
  { label: 'Sedang (Nyaman)', value: 'sedang' },
  { label: 'Mewah (Premium)', value: 'mewah' },
]);

const availableTripTypes = ref([
  { label: 'Solo Traveler', value: 'solo' },
  { label: 'Pasangan', value: 'pasangan' },
  { label: 'Keluarga (dengan anak)', value: 'keluarga' },
  { label: 'Grup Teman', value: 'grup' },
]);

const handleCreateItineraryWithAI = async () => {
  isLoading.value = true;
  apiMessage.value = { type: '', text: '' };

  if (!form.itinerary_name || !form.preferences.destination_city) {
    apiMessage.value = { type: 'error', text: 'Nama itinerary dan Kota Tujuan tidak boleh kosong.' };
    isLoading.value = false;
    return;
  }
  if ((form.start_date && !form.end_date) || (!form.start_date && form.end_date)) {
    apiMessage.value = { type: 'error', text: 'Jika mengisi satu tanggal, tanggal lainnya juga harus diisi.' };
    isLoading.value = false;
    return;
  }
  if (form.start_date && form.end_date && new Date(form.end_date) < new Date(form.start_date)) {
    apiMessage.value = { type: 'error', text: 'Tanggal selesai tidak boleh sebelum tanggal mulai.' };
    isLoading.value = false;
    return;
  }
  if (!form.start_date && !form.end_date && (!form.number_of_days || form.number_of_days < 1)) {
    apiMessage.value = { type: 'error', text: 'Isi tanggal mulai & selesai, atau jumlah hari yang valid.' };
    isLoading.value = false;
    return;
  }
  if (form.preferences.interests.length === 0) {
    apiMessage.value = { type: 'error', text: 'Pilih minimal satu minat perjalanan.' };
    isLoading.value = false;
    return;
  }


  const payload = {
    itinerary_name: form.itinerary_name,
    notes: form.notes,
    preferences: form.preferences,
  };

  if (form.start_date && form.end_date) {
    payload.start_date = form.start_date;
    payload.end_date = form.end_date;
  } else if (form.number_of_days) {
    payload.number_of_days = form.number_of_days;
  }

  if (!form.preferences.trip_type) {
    apiMessage.value = { type: 'error', text: 'Pilih tipe perjalanan.' };
    isLoading.value = false;
    return;
  }

  try {
    const response = await apiClient.post('/itineraries/generate-ai', payload);
    apiMessage.value = { type: 'success', text: response.data.msg || 'Itinerary AI berhasil dibuat!' };

    const newItineraryId = response.data.itinerary_id;
    if (newItineraryId) {
      setTimeout(() => {
        router.push({ name: 'itineraryResult', params: { id: newItineraryId } });
      }, 1500);
    } else {
      apiMessage.value = { type: 'error', text: 'Gagal mendapatkan ID itinerary baru dari AI.' };
    }

  } catch (error) {
    console.error("Gagal membuat itinerary AI:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal membuat itinerary dengan AI. Coba lagi.' };
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped></style>
