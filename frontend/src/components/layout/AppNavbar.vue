<template>
  <nav class="bg-gradient-to-r from-blue-600 to-indigo-700 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo/Brand -->
        <div class="flex-shrink-0">
          <router-link to="/" class="text-white text-2xl font-bold tracking-tight hover:opacity-80 transition-opacity">
            Travel Mind
          </router-link>
        </div>

        <!-- Links (Desktop) -->
        <div class="hidden md:block">
          <div class="ml-10 flex items-baseline space-x-4">
            <router-link to="/"
              class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
              active-class="bg-blue-800 text-white">
              Home
            </router-link>

            <template v-if="authStore.isAuthenticated">
              <router-link to="/itinerary/new"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                active-class="bg-blue-800 text-white">
                Buat Itinerary
              </router-link>
              <router-link to="/itinerary/my-list"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                active-class="bg-blue-800 text-white">
                Itinerary Saya
              </router-link>
              <router-link to="/profile"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                active-class="bg-blue-800 text-white">
                Profil
              </router-link>
              <a href="#" @click.prevent="handleLogout"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Logout ({{ authStore.user?.username }})
              </a>
            </template>
            <template v-else>
              <router-link to="/login"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                active-class="bg-blue-800 text-white">
                Login
              </router-link>
              <router-link to="/register"
                class="text-gray-200 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                active-class="bg-blue-800 text-white">
                Register
              </router-link>
            </template>
          </div>
        </div>

        <!-- Mobile menu button (Contoh, implementasi penuh butuh state & event) -->
        <div class="-mr-2 flex md:hidden">
          <button @click="mobileMenuOpen = !mobileMenuOpen" type="button"
            class="bg-blue-600 inline-flex items-center justify-center p-2 rounded-md text-gray-300 hover:text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-blue-700 focus:ring-white"
            aria-controls="mobile-menu" aria-expanded="false">
            <span class="sr-only">Open main menu</span>
            <!-- Icon for menu open -->
            <svg v-if="!mobileMenuOpen" class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <!-- Icon for menu close -->
            <svg v-else class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu, show/hide based on menu state. -->
    <div v-if="mobileMenuOpen" class="md:hidden" id="mobile-menu">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <router-link to="/"
          class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
          active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Home</router-link>
        <template v-if="authStore.isAuthenticated">
          <router-link to="/itinerary/new"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Buat Itinerary</router-link>
          <router-link to="/itinerary/my-list"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Itinerary Saya</router-link>
          <router-link to="/profile"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Profil</router-link>
          <a href="#" @click.prevent="handleLogoutMobile"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors">Logout
            ({{ authStore.user?.username }})</a>
        </template>
        <template v-else>
          <router-link to="/login"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Login</router-link>
          <router-link to="/register"
            class="text-gray-200 hover:bg-blue-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="bg-blue-800 text-white" @click="mobileMenuOpen = false">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const mobileMenuOpen = ref(false);

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

const handleLogoutMobile = () => {
  handleLogout();
  mobileMenuOpen.value = false;
};
</script>

<style scoped>
/* Router link active class kustom jika defaultnya tidak cukup */
/* .router-link-exact-active {
  @apply bg-blue-800 text-white;
} */
/* Kita sudah menggunakan active-class prop di <router-link> */
</style>
