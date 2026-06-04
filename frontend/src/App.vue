<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Cook Book</v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn-toggle v-model="locale" color="secondary" variant="text" mandatory>
        <v-btn value="ru">RU</v-btn>
        <v-btn value="en">EN</v-btn>
      </v-btn-toggle>
      
      <template v-if="isLoggedIn">
        <v-btn :to="{ name: 'recipes' }" variant="text">{{ $t('nav.recipes') }}</v-btn>
        <v-btn :to="{ name: 'favorites' }" variant="text">{{ $t('nav.favorites') }}</v-btn>
        <v-btn @click="logout" variant="text">{{ $t('nav.logout') }}</v-btn>
      </template>
      <template v-else>
        <v-btn :to="{ name: 'login' }" variant="text">{{ $t('nav.login') }}</v-btn>
        <v-btn :to="{ name: 'register' }" variant="text">{{ $t('nav.register') }}</v-btn>
      </template>
    </v-app-bar>
    
    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
    
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
      <v-btn @click="snackbar.show = false" variant="text">
        {{ $t('close') }}
      </v-btn>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const i18n = useI18n()
const authStore = useAuthStore()

const locale = computed({
  get: () => i18n.locale.value,
  set: (value) => {
    i18n.locale.value = value
    localStorage.setItem('locale', value)
  }
})

const isLoggedIn = computed(() => authStore.isLoggedIn)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const logout = async () => {
  await authStore.logout()
  showSnackbar('Вы вышли из системы', 'info')
}

const showSnackbar = (text, color = 'success') => {
  snackbar.value = { show: true, text, color }
}

const savedLocale = localStorage.getItem('locale')
if (savedLocale && ['ru', 'en'].includes(savedLocale)) {
  locale.value = savedLocale
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
}
</style>
