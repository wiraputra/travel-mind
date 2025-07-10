<template>
  <component :is="layout" />
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import DefaultLayout from './layouts/DefaultLayout.vue';
import AuthLayout from './layouts/AuthLayout.vue';

const route = useRoute();

const layout = computed(() => {
  // Cek meta field dari route yang paling dalam (jika nested)
  const matchedRoute = route.matched.slice().reverse().find(r => r.meta.layout);
  if (matchedRoute) {
    if (matchedRoute.meta.layout === 'AuthLayout') return AuthLayout;
  }
  return DefaultLayout;
});
</script>
