<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-indigo-700 via-purple-600 to-pink-600 text-white py-20 md:py-32">
      <div class="container mx-auto px-6 text-center">
        <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight leading-tight mb-6">
          Rencanakan Perjalanan Impian Anda dengan <span class="block md:inline">Travel Mind</span>
        </h1>
        <p class="text-lg md:text-xl text-indigo-100 mb-10 max-w-2xl mx-auto">
          Biarkan AI cerdas kami membantu Anda menyusun itinerary perjalanan yang personal dan tak terlupakan, sesuai
          dengan preferensi dan gaya Anda.
        </p>
        <div class="space-y-4 sm:space-y-0 sm:space-x-4">
          <router-link v-if="!authStore.isAuthenticated" to="/register"
            class="inline-block bg-white text-indigo-600 font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-indigo-50 transition-colors text-lg transform hover:scale-105">
            Mulai Sekarang (Gratis!)
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/itinerary/new"
            class="inline-block bg-white text-indigo-600 font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-indigo-50 transition-colors text-lg transform hover:scale-105">
            Buat Itinerary Baru
          </router-link>
          <router-link v-if="!authStore.isAuthenticated" to="/login"
            class="inline-block bg-transparent border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-indigo-600 transition-colors text-lg transform hover:scale-105">
            Sudah Punya Akun? Login
          </router-link>
        </div>
      </div>
    </section>

    <!-- Fitur Unggulan Kami Section -->
    <section class="py-16 lg:py-24 bg-slate-50">
      <div class="container mx-auto px-6">
        <div class="text-center mb-12 lg:mb-16">
          <h2 class="text-3xl lg:text-4xl font-bold text-gray-800">Fitur Unggulan Kami</h2>
          <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">Temukan kemudahan merencanakan perjalanan dengan
            teknologi AI terdepan.</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8 lg:gap-12">
          <!-- Fitur 1 -->
          <div
            class="feature-card bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div
              class="flex items-center justify-center w-16 h-16 mb-6 bg-indigo-100 text-indigo-600 rounded-full mx-auto">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                </path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-3 text-center">Rekomendasi AI Personal</h3>
            <p class="text-gray-600 text-sm leading-relaxed text-center">
              Itinerary dibuat khusus untuk Anda berdasarkan minat, gaya perjalanan, dan budget. Ucapkan selamat tinggal
              pada rencana generik!
            </p>
          </div>
          <!-- Fitur 2 -->
          <div
            class="feature-card bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div
              class="flex items-center justify-center w-16 h-16 mb-6 bg-purple-100 text-purple-600 rounded-full mx-auto">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-3 text-center">Peta & Rute Interaktif</h3>
            <p class="text-gray-600 text-sm leading-relaxed text-center">
              Visualisasikan seluruh perjalanan Anda. Atur ulang destinasi dengan mudah dan lihat estimasi rute secara
              langsung di peta.
            </p>
          </div>
          <!-- Fitur 3 -->
          <div
            class="feature-card bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
            <div class="flex items-center justify-center w-16 h-16 mb-6 bg-pink-100 text-pink-600 rounded-full mx-auto">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6V4m0 16v-2m8-8h-2M4 12H2m15.364 6.364l-1.414-1.414M6.343 6.343l-1.414-1.414m12.728 0l-1.414 1.414M6.343 17.657l-1.414 1.414M16 12a4 4 0 11-8 0 4 4 0 018 0z">
                </path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-3 text-center">Fleksibel & Mudah Dikelola</h3>
            <p class="text-gray-600 text-sm leading-relaxed text-center">
              Simpan semua itinerary Anda, edit kapan saja, dan akses dari mana saja. Perencanaan perjalanan jadi lebih
              menyenangkan!
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Bagaimana Cara Kerjanya Section -->
    <section class="py-16 lg:py-24 bg-white">
      <div class="container mx-auto px-6">
        <div class="text-center mb-12 lg:mb-16">
          <h2 class="text-3xl lg:text-4xl font-bold text-gray-800">Bagaimana Cara Kerjanya?</h2>
          <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">Hanya dengan beberapa langkah mudah, itinerary impian
            Anda siap!</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8 lg:gap-10 relative">
          <!-- Garis penghubung (opsional, bisa dibuat dengan pseudo-elements atau SVG) -->
          <!-- Langkah 1 -->
          <div class="step-card text-center p-6">
            <div
              class="flex items-center justify-center w-20 h-20 mb-6 border-4 border-indigo-500 text-indigo-600 rounded-full mx-auto text-3xl font-bold">
              1
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Beritahu Preferensi Anda</h3>
            <p class="text-gray-600 text-sm leading-relaxed">
              Isi form singkat mengenai tujuan, durasi, minat, dan gaya perjalanan yang Anda inginkan.
            </p>
          </div>
          <!-- Langkah 2 -->
          <div class="step-card text-center p-6">
            <div
              class="flex items-center justify-center w-20 h-20 mb-6 border-4 border-purple-500 text-purple-600 rounded-full mx-auto text-3xl font-bold">
              2
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">AI Menyusun Rencana</h3>
            <p class="text-gray-600 text-sm leading-relaxed">
              Sistem cerdas kami akan menganalisis preferensi Anda dan membuat draf itinerary lengkap dengan rekomendasi
              tempat.
            </p>
          </div>
          <!-- Langkah 3 -->
          <div class="step-card text-center p-6">
            <div
              class="flex items-center justify-center w-20 h-20 mb-6 border-4 border-pink-500 text-pink-600 rounded-full mx-auto text-3xl font-bold">
              3
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Sesuaikan & Nikmati!</h3>
            <p class="text-gray-600 text-sm leading-relaxed">
              Lihat hasilnya di peta, atur ulang jika perlu, tambahkan catatan, dan itinerary Anda siap untuk
              petualangan!
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonial Section (Opsional) -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl font-bold text-gray-800 mb-8">Apa Kata Mereka?</h2>
        <div class="max-w-3xl mx-auto">
          <div class="p-6 bg-slate-100 rounded-lg shadow-md">
            <p class="text-gray-700 italic mb-4">
              "Travel Mind mengubah cara saya merencanakan liburan! AI-nya benar-benar mengerti apa yang saya inginkan,
              dan fitur petanya sangat membantu. Highly recommended!"
            </p>
            <p class="font-semibold text-gray-800">- Traveler Bahagia</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Bawah (Opsional) -->
    <section class="py-20 bg-indigo-600">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl font-bold text-white mb-6">Siap Memulai Petualangan Anda?</h2>
        <router-link v-if="!authStore.isAuthenticated" to="/register"
          class="inline-block bg-white text-indigo-600 font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-indigo-50 transition-colors text-lg">
          Daftar Sekarang, Gratis!
        </router-link>
        <router-link v-if="authStore.isAuthenticated" to="/itinerary/new"
          class="inline-block bg-white text-indigo-600 font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-indigo-50 transition-colors text-lg">
          Rencanakan Itinerary Berikutnya
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
/* Style khusus untuk HomeView jika diperlukan,
   misalnya untuk background image pada hero section jika tidak ingin gradient. */
.home-view {
  /* Contoh jika ingin animasi halus pada section */
  scroll-behavior: smooth;
}
</style>
