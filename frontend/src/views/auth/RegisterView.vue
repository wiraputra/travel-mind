<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md text-center mb-8">
      <router-link to="/" class="text-5xl font-extrabold text-white hover:opacity-80 transition-opacity">
        Travel Mind
      </router-link>
      <h2 class="mt-4 text-center text-2xl font-semibold text-gray-300">
        Buat akun baru
      </h2>
    </div>

    <div class="mt-2 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-2xl rounded-xl sm:px-10">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-400 p-4 mb-6">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                  fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-green-700">{{ successMessage }}</p>
              </div>
            </div>
          </div>
          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                  fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 3.005-1.742 3.005H4.42c-1.53 0-2.493-1.671-1.743-3.005l5.58-9.92zM10 11a1 1 0 100-2 1 1 0 000 2zm0 4a1 1 0 100-2 1 1 0 000 2z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-700">{{ errorMessage }}</p>
              </div>
            </div>
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-gray-700"> Username </label>
            <div class="mt-1">
              <input id="username" name="username" type="text" v-model="username" required
                class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700"> Alamat Email </label>
            <div class="mt-1">
              <input id="email" name="email" type="email" v-model="email" autocomplete="email" required
                class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700"> Nama Lengkap <span
                class="text-xs text-gray-500">(Opsional)</span></label>
            <div class="mt-1">
              <input id="full_name" name="full_name" type="text" v-model="full_name"
                class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700"> Password </label>
            <div class="mt-1">
              <input id="password" name="password" type="password" v-model="password" autocomplete="new-password"
                required
                class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <button type="submit" :disabled="isLoading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
              <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              Daftar
            </button>
          </div>
        </form>
        <div class="mt-6 text-center text-sm text-gray-600">
          Sudah punya akun?
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500"> Login di sini
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const email = ref('');
const password = ref('');
const full_name = ref('');
const errorMessage = ref(null);
const successMessage = ref(null);
const isLoading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleRegister = async () => {
  isLoading.value = true;
  errorMessage.value = null;
  successMessage.value = null;
  try {
    const response = await authStore.registerAction({
      username: username.value,
      email: email.value,
      password: password.value,
      full_name: full_name.value || undefined,
    });
    successMessage.value = `${response.msg || 'Registrasi berhasil!'} Silakan login.`;
    username.value = '';
    email.value = '';
    password.value = '';
    full_name.value = '';
    setTimeout(() => {
      if (successMessage.value) router.push('/login');
    }, 2500);
  } catch (error) {
    errorMessage.value = error.msg || 'Registrasi gagal. Coba lagi.';
  } finally {
    isLoading.value = false;
  }
};
</script>
