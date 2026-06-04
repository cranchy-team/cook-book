<template>
  <v-container max-width="800">
    <h1 class="text-h4 mb-6">{{ $t('recipes.create') }}</h1>
    
    <v-card>
      <v-card-text>
        <v-form @submit.prevent="handleCreate" ref="form">
          <v-text-field
            v-model="form_data.title"
            :label="$t('recipes.titleLabel')"
            required
            :rules="[rules.required]"
            variant="outlined"
            maxlength="200"
            counter
          ></v-text-field>
          
          <v-textarea
            v-model="form_data.ingredients"
            :label="$t('recipes.ingredients')"
            required
            :rules="[rules.required]"
            variant="outlined"
            rows="4"
          ></v-textarea>
          
          <v-textarea
            v-model="form_data.steps"
            :label="$t('recipes.steps')"
            required
            :rules="[rules.required]"
            variant="outlined"
            rows="6"
          ></v-textarea>
          
          <v-text-field
            v-model.number="form_data.cooking_time"
            :label="$t('recipes.cookingTime')"
            type="number"
            required
            :rules="[rules.required, rules.minZero]"
            variant="outlined"
            min="1"
          ></v-text-field>
          
          <v-select
            v-model="form_data.difficulty"
            :label="$t('recipes.difficulty')"
            :items="difficultyItems"
            required
            :rules="[rules.required]"
            variant="outlined"
          ></v-select>
          
          <v-file-input
            v-model="selectedImage"
            :label="$t('recipes.image')"
            accept="image/*"
            prepend-icon="mdi-camera"
            @change="handleImageSelect"
            variant="outlined"
          ></v-file-input>
          
          <v-card v-if="imagePreview" class="mt-4" elevation="2">
            <v-img
              :src="imagePreview"
              aspect-ratio="1"
              class="bg-grey lighten-3"
            >
              <v-overlay
                v-if="showCropper"
                contained
                class="align-center justify-center"
              >
                <v-btn color="primary" @click="cropImage">
                  <v-icon>mdi-check</v-icon>
                  {{ $t('recipes.save') }}
                </v-btn>
              </v-overlay>
            </v-img>
          </v-card>
          
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mt-4"
          >
            {{ error }}
          </v-alert>
        </v-form>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :to="{ name: 'recipes' }" variant="outlined">
          {{ $t('recipes.cancel') }}
        </v-btn>
        <v-btn
          color="primary"
          @click="handleCreate"
          :loading="loading"
        >
          {{ $t('recipes.save') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { recipeApi } from '@/api/client'
import Cropper from 'cropperjs'

const router = useRouter()
const { t } = useI18n()

const form = ref(null)
const form_data = ref({
  title: '',
  ingredients: '',
  steps: '',
  cooking_time: null,
  difficulty: ''
})
const selectedImage = ref(null)
const imagePreview = ref(null)
const showCropper = ref(false)
const cropper = ref(null)
const loading = ref(false)
const error = ref('')

const rules = {
  required: value => !!value || 'Обязательное поле',
  minZero: value => value > 0 || 'Значение должно быть больше 0'
}

const difficultyItems = [
  { title: t('recipes.difficultyEasy'), value: 'easy' },
  { title: t('recipes.difficultyMedium'), value: 'medium' },
  { title: t('recipes.difficultyHard'), value: 'hard' }
]

const handleImageSelect = (files) => {
  const file = files[0]
  if (!file) return
  
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    showCropper.value = true
  }
  reader.readAsDataURL(file)
}

const cropImage = () => {
  if (!cropper.value) return
  
  const canvas = cropper.value.getCroppedCanvas({
    width: 1200,
    height: 1200
  })
  
  canvas.toBlob((blob) => {
    croppedBlob = blob
    showCropper.value = false
  }, 'image/jpeg', 0.8)
}

const handleCreate = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  try {
    const response = await recipeApi.post('/recipes/', form_data.value)
    const recipeId = response.data.id
    
    if (croppedBlob) {
      const formData = new FormData()
      formData.append('image', croppedBlob, 'recipe.jpg')
      await recipeApi.post(`/recipes/${recipeId}/upload-image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    
    router.push({ name: 'recipes' })
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при создании рецепта'
  } finally {
    loading.value = false
  }
}
</script>
