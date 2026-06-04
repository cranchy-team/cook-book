<template>
  <v-container class="fill-height" max-width="400">
    <v-card elevation="4">
      <v-card-title class="text-h5 justify-center py-4">
        {{ $t('auth.register') }}
      </v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="handleRegister" ref="form">
          <v-text-field
            v-model="email"
            :label="$t('auth.email')"
            type="email"
            required
            :rules="[rules.required, rules.email]"
            variant="outlined"
          ></v-text-field>
          
          <v-text-field
            v-model="password"
            :label="$t('auth.password')"
            type="password"
            required
            :rules="[rules.required, rules.minLength]"
            variant="outlined"
          ></v-text-field>
          
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mt-4"
          >
            {{ error }}
          </v-alert>
          
          <v-btn
            type="submit"
            color="primary"
            block
            class="mt-4"
            :loading="loading"
            size="large"
          >
            {{ $t('auth.registerSubmit') }}
          </v-btn>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="justify-center pb-4">
        <span class="text-body-2">{{ $t('auth.hasAccount') }}</span>
        <router-link :to="{ name: 'login' }" class="text-primary ml-1">
          {{ $t('auth.login') }}
        </router-link>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const form = ref(null)

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Невалидный email'
  },
  minLength: value => value.length >= 6 || 'Минимум 6 символов'
}

const handleRegister = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  try {
    await authStore.register(email.value, password.value)
    router.push({ name: 'login' })
  } catch (err) {
    error.value = err.response?.data?.detail || t('auth.error')
  } finally {
    loading.value = false
  }
}
</script>
