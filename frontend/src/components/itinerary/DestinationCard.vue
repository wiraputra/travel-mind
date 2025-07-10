<template>
  <div class="destination-card bg-white p-3.5 rounded-lg shadow border border-gray-200 card-hover"
    :class="{ 'cursor-pointer': canEmitCardClick }" @click="handleCardClick">
    <div class="flex items-start space-x-3">
      <!-- Gambar -->
      <div class="flex-shrink-0">
        <img v-if="destination?.image_url" :src="destination.image_url" alt="Destination Image"
          class="w-20 h-20 rounded object-cover" />
        <div v-else class="w-20 h-20 rounded bg-gray-200 flex items-center justify-center text-gray-400">
          <svg class="w-10 h-10" fill="currentColor" viewBox="0 0 20 20">
            <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"></path>
          </svg>
        </div>
      </div>

      <!-- Info Utama -->
      <div class="flex-1 min-w-0">
        <div class="flex justify-between items-start">
          <h4 class="text-base font-semibold text-gray-800 truncate pr-2" :title="destination?.name">
            {{ destination?.name || 'Nama Destinasi Tidak Ada' }}
          </h4>
          <button v-if="showDeleteButton" @click.stop="$emit('delete-item', destinationItem.item_id)"
            class="text-gray-400 hover:text-red-500 transition-colors p-1 -m-1 flex-shrink-0" title="Hapus Destinasi">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <!-- Rating -->
        <div v-if="destination?.avg_rating" class="flex items-center mt-0.5 mb-1">
          <svg v-for="star in 5" :key="star" class="w-3.5 h-3.5"
            :class="star <= Math.round(destination.avg_rating) ? 'text-yellow-400' : 'text-gray-300'"
            fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z">
            </path>
          </svg>
          <span class="ml-1.5 text-xs text-gray-500">{{ destination.avg_rating.toFixed(1) }}</span>
        </div>
        <p v-else class="text-xs text-gray-400 mt-0.5 mb-1 italic">Belum ada rating</p>

        <!-- Durasi & Waktu Kunjungan (jika ada di ItineraryItem) -->
        <div class="text-xs text-gray-600 space-y-0.5">
          <p v-if="destinationItem.duration_minutes">
            <svg class="inline w-3.5 h-3.5 mr-1 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Durasi Rencana: <span class="font-medium">{{ destinationItem.duration_minutes }} menit</span>
          </p>
          <p v-else-if="destination?.typical_visit_duration_minutes">
            <svg class="inline w-3.5 h-3.5 mr-1 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Estimasi Durasi: <span class="font-medium">{{ destination.typical_visit_duration_minutes }} menit</span>
          </p>

          <p v-if="destinationItem.visit_time">
            <svg class="inline w-3.5 h-3.5 mr-1 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Rencana Jam: <span class="font-medium">{{ formatTime(destinationItem.visit_time) }}</span>
          </p>
        </div>

        <!-- Jam Buka -->
        <div v-if="openingHoursInfo.display" class="text-xs mt-1.5 flex items-start">
          <svg class="flex-shrink-0 w-3.5 h-3.5 mr-1 mt-0.5"
            :class="openingHoursInfo.isOpenNow && openingHoursInfo.text !== 'Tutup' ? 'text-green-600' : 'text-red-600'"
            fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z"
              clip-rule="evenodd"></path>
          </svg>
          <span
            :class="openingHoursInfo.isOpenNow && openingHoursInfo.text !== 'Tutup' ? 'text-green-700' : 'text-red-700'">
            {{ openingHoursInfo.text }}
            <span v-if="openingHoursInfo.isOpenNow && openingHoursInfo.text !== 'Tutup'"> (Buka)</span>
            <span
              v-else-if="!openingHoursInfo.isOpenNow && openingHoursInfo.text !== 'Tutup' && openingHoursInfo.text !== 'Info jam buka tidak tersedia'">
              (Sedang Tutup)</span>
          </span>
        </div>

        <p v-if="destinationItem.notes" class="text-xs text-gray-600 mt-2 pt-1 border-t border-gray-100 truncate"
          :title="destinationItem.notes">
          <span class="font-medium">Catatan:</span> {{ destinationItem.notes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  destinationItem: {
    type: Object,
    required: true,
  },
  showDeleteButton: {
    type: Boolean,
    default: true,
  },
  canEmitCardClick: {
    type: Boolean,
    default: true,
  }
});

const emit = defineEmits(['card-click', 'delete-item']);

const destination = computed(() => props.destinationItem.destination);

const formatTime = (timeString) => {
  if (!timeString) return '';
  const parts = timeString.split(':');
  return `${parts[0]}:${parts[1]}`;
};

const getOpeningHoursForDay = (openingHoursJson, targetDay) => {
  if (!openingHoursJson || typeof openingHoursJson !== 'object') {
    return { text: 'Info jam buka tidak tersedia', range: null };
  }

  const days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  const targetDayStr = days[targetDay];

  let hoursStr = null;

  const jsonKeys = Object.keys(openingHoursJson);
  const foundKey = jsonKeys.find(key => key.toLowerCase() === targetDayStr);

  if (foundKey) {
    hoursStr = openingHoursJson[foundKey];
  } else {
    const defaultKey = jsonKeys.find(key => key.toLowerCase() === 'default');
    if (defaultKey) {
      hoursStr = openingHoursJson[defaultKey];
    }
  }

  if (!hoursStr) {
    return { text: 'Info jam buka tidak tersedia', range: null };
  }

  if (String(hoursStr).toLowerCase() === 'tutup' || String(hoursStr).toLowerCase() === 'closed') {
    return { text: 'Tutup', range: null };
  }
  if (String(hoursStr).toLowerCase() === '24 jam' || String(hoursStr).toLowerCase() === '24 hours') {
    return { text: 'Buka 24 Jam', range: { openH: 0, openM: 0, closeH: 23, closeM: 59 } };
  }

  if (String(hoursStr).includes('-')) {
    const [openTimeStr, closeTimeStr] = String(hoursStr).split('-');
    try {
      const [openH, openM] = openTimeStr.trim().split(':').map(Number);
      const [closeH, closeM] = closeTimeStr.trim().split(':').map(Number);
      return { text: hoursStr, range: { openH, openM, closeH, closeM } };
    } catch (e) {
      return { text: hoursStr, range: null };
    }
  }
  return { text: hoursStr, range: null };
}

const openingHoursInfo = computed(() => {
  if (!destination.value || !destination.value.opening_hours) return { display: false, text: '', isOpenNow: false };

  const todayDate = new Date();
  const todayDayIndex = todayDate.getDay();

  const hoursData = getOpeningHoursForDay(destination.value.opening_hours, todayDayIndex);

  if (hoursData.text === 'Info jam buka tidak tersedia' || hoursData.text === 'Tutup') {
    return { display: true, text: `Hari ini: ${hoursData.text}`, isOpenNow: false };
  }
  if (hoursData.text === 'Buka 24 Jam') {
    return { display: true, text: `Hari ini: ${hoursData.text}`, isOpenNow: true };
  }


  let isOpen = false;
  if (hoursData.range) {
    const now = new Date();
    const currentHours = now.getHours();
    const currentMinutes = now.getMinutes();
    const nowInMinutes = currentHours * 60 + currentMinutes;

    const { openH, openM, closeH, closeM } = hoursData.range;
    const openInMinutes = openH * 60 + openM;
    let closeInMinutes = closeH * 60 + closeM;

    if (closeInMinutes < openInMinutes) {
      closeInMinutes += 24 * 60;
      const adjustedNowInMinutes = (currentHours < openH) ? nowInMinutes + 24 * 60 : nowInMinutes;
      if (adjustedNowInMinutes >= openInMinutes && adjustedNowInMinutes < closeInMinutes) {
        isOpen = true;
      }
    } else {
      if (nowInMinutes >= openInMinutes && nowInMinutes < closeInMinutes) {
        isOpen = true;
      }
    }
  }
  return { display: true, text: `Hari ini: ${hoursData.text}`, isOpenNow: isOpen };
});

const handleCardClick = () => {
  if (props.canEmitCardClick) {
    emit('card-click', props.destinationItem);
  }
};

</script>
