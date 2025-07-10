<template>
  <div class="profile-view container mx-auto px-4 py-8 pt-8">
    <div class="bg-white shadow-xl rounded-lg p-6 md:p-10 max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Profil Saya</h1>

      <div v-if="isLoading && !user" class="text-center py-10">
        <svg class="animate-spin h-8 w-8 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
          </path>
        </svg>
        <p class="text-gray-600 mt-2">Memuat profil...</p>
      </div>
      <div v-if="apiMessage.text"
        :class="['border-l-4 p-4 mb-6', apiMessage.type === 'success' ? 'bg-green-50 border-green-400 text-green-700' : 'bg-red-50 border-red-400 text-red-700']"
        role="alert">
        <p>{{ apiMessage.text }}</p>
      </div>

      <!-- <div v-if="profileErrorMessage" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6" role="alert">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
              aria-hidden="true">
              <path fill-rule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 3.005-1.742 3.005H4.42c-1.53 0-2.493-1.671-1.743-3.005l5.58-9.92zM10 11a1 1 0 100-2 1 1 0 000 2zm0 4a1 1 0 100-2 1 1 0 000 2z"
                clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">{{ profileErrorMessage }}</p>
          </div>
        </div>
      </div> -->

      <div v-if="user" class="space-y-6">
        <!-- Foto Profil (Placeholder) -->
        <div class="flex flex-col items-center space-y-4">
          <div
            class="w-32 h-32 rounded-full bg-gray-300 flex items-center justify-center text-gray-500 text-4xl overflow-hidden">
            <!-- <img v-if="user.profile_picture_url" :src="user.profile_picture_url" alt="Foto Profil" class="w-full h-full object-cover"> -->
            <span v-if="user.username">{{ user.username.charAt(0).toUpperCase() }}</span>
            <svg v-else class="w-16 h-16" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd">
              </path>
            </svg>
          </div>
          <!-- <button class="text-sm text-indigo-600 hover:text-indigo-500">Ubah Foto</button> -->
        </div>

        <!-- Informasi Profil -->
        <form @submit.prevent="handleProfileUpdate">
          <div>
            <h3 class="text-lg font-medium text-gray-900 border-b pb-2 mb-4">Informasi Akun</h3>
            <dl class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-2 items-center">
                <dt class="text-sm font-medium text-gray-500">Username:</dt>
                <dd class="md:col-span-2 text-sm text-gray-900 bg-gray-100 p-2.5 rounded">{{ user.username }} <span
                    class="text-xs text-gray-400">(tidak dapat diubah)</span></dd>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-2 items-center">
                <dt class="text-sm font-medium text-gray-500">Email:</dt>
                <dd class="md:col-span-2 text-sm text-gray-900 bg-gray-100 p-2.5 rounded">{{ user.email }} <span
                    class="text-xs text-gray-400">(tidak dapat diubah)</span></dd>
              </div>

              <!-- Editable Full Name -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-2 items-center">
                <dt class="text-sm font-medium text-gray-500">Nama Lengkap:</dt>
                <dd class="md:col-span-2">
                  <input type="text" id="full_name" v-model="editableProfile.full_name"
                    class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
                </dd>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-2 items-center">
                <dt class="text-sm font-medium text-gray-500">Terdaftar Sejak:</dt>
                <dd class="md:col-span-2 text-sm text-gray-900 bg-gray-100 p-2.5 rounded">{{ formattedJoinDate }}</dd>
              </div>
            </dl>
          </div>

          <!-- Ubah Password (Opsional, disiapkan) -->
          <div class="pt-6 border-t mt-6">
            <h3 class="text-lg font-medium text-gray-900 border-b pb-2 mb-4">Ubah Password</h3>
            <div class="space-y-4">
              <div>
                <label for="current_password" class="block text-sm font-medium text-gray-700">Password Saat Ini</label>
                <input type="password" id="current_password" v-model="editableProfile.current_password"
                  autocomplete="current-password"
                  class="mt-1 appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
              </div>
              <div>
                <label for="new_password" class="block text-sm font-medium text-gray-700">Password Baru</label>
                <input type="password" id="new_password" v-model="editableProfile.new_password"
                  autocomplete="new-password"
                  class="mt-1 appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
              </div>
              <div>
                <label for="confirm_new_password" class="block text-sm font-medium text-gray-700">Konfirmasi Password
                  Baru</label>
                <input type="password" id="confirm_new_password" v-model="editableProfile.confirm_new_password"
                  autocomplete="new-password"
                  class="mt-1 appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
              </div>
            </div>
          </div>

          <!-- Tombol Aksi -->
          <div class="pt-8 flex justify-end space-x-3">
            <button type="button" @click="resetForm"
              class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Batal
            </button>
            <button type="submit" :disabled="isUpdating"
              class="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
              <svg v-if="isUpdating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';

const authStore = useAuthStore();
const user = ref(null);
const isLoading = ref(true);
const isUpdating = ref(false);
const apiMessage = ref({ type: '', text: '' });

// Data yang bisa diedit, diinisialisasi kosong atau dari user
const editableProfile = reactive({
  full_name: '',
  current_password: '',
  new_password: '',
  confirm_new_password: '',
});

// Fungsi untuk mengisi form editableProfile dari data user yang sudah di-fetch
const populateEditableProfile = (sourceUser) => {
  if (sourceUser) {
    editableProfile.full_name = sourceUser.full_name || '';
    // Kosongkan field password
    editableProfile.current_password = '';
    editableProfile.new_password = '';
    editableProfile.confirm_new_password = '';
  }
};

const fetchUserProfile = async () => {
  isLoading.value = true;
  apiMessage.value = { type: '', text: '' };
  if (!authStore.token) {
    apiMessage.value = { type: 'error', text: "Anda harus login untuk melihat profil." };
    isLoading.value = false;
    return;
  }
  try {
    const response = await apiClient.get('/auth/profile');
    user.value = response.data;
    populateEditableProfile(user.value);

    // Update juga user di authStore jika data dari /profile lebih lengkap
    authStore.user = { ...authStore.user, ...response.data };
    localStorage.setItem('user-info', JSON.stringify(authStore.user));

  } catch (error) {
    console.error("Gagal mengambil profil:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || "Tidak dapat memuat profil." };
  } finally {
    isLoading.value = false;
  }
};

const handleProfileUpdate = async () => {
  isUpdating.value = true;
  apiMessage.value = { type: '', text: '' };

  if (editableProfile.new_password && editableProfile.new_password !== editableProfile.confirm_new_password) {
    apiMessage.value = { type: 'error', text: 'Konfirmasi password baru tidak cocok.' };
    isUpdating.value = false;
    return;
  }
  if (editableProfile.new_password && !editableProfile.current_password) {
    apiMessage.value = { type: 'error', text: 'Password saat ini dibutuhkan untuk mengubah password.' };
    isUpdating.value = false;
    return;
  }


  const payload = {
    full_name: editableProfile.full_name,
  };

  if (editableProfile.new_password) {
    payload.current_password = editableProfile.current_password;
    payload.new_password = editableProfile.new_password;
  }

  try {
    const response = await apiClient.put('/auth/profile', payload);
    user.value = { ...user.value, ...response.data.user };
    populateEditableProfile(user.value);

    // Update juga user di authStore
    authStore.user = { ...authStore.user, ...response.data.user };
    localStorage.setItem('user-info', JSON.stringify(authStore.user));

    apiMessage.value = { type: 'success', text: response.data.msg || 'Profil berhasil diperbarui!' };
  } catch (error) {
    console.error("Gagal update profil:", error);
    apiMessage.value = { type: 'error', text: error.response?.data?.msg || 'Gagal memperbarui profil.' };
  } finally {
    isUpdating.value = false;
  }
};

const resetForm = () => {
  if (user.value) {
    populateEditableProfile(user.value);
  }
  apiMessage.value = { type: '', text: '' };
};

const formattedJoinDate = computed(() => {
  if (user.value && user.value.created_at) {
    const date = new Date(user.value.created_at);
    return date.toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric' });
  }
  return '-';
});

onMounted(() => {
  fetchUserProfile();
});

// Jika user dari store berubah (misalnya karena login/logout di tab lain), fetch ulang
watch(() => authStore.user?.userId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    fetchUserProfile();
  }
});
</script>

<style scoped></style>
