<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">{{ $t('recipes.title') }}</h1>
      <v-btn color="primary" :to="{ name: 'create-recipe' }" prepend-icon="mdi-plus">
        {{ $t('recipes.create') }}
      </v-btn>
    </div>
    
    <v-card class="mb-4">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              :label="$t('recipes.search')"
              prepend-icon="mdi-magnify"
              clearable
              @input="debouncedSearch"
              variant="outlined"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="difficultyFilter"
              :label="$t('recipes.difficulty')"
              :items="difficultyItems"
              clearable
              @update:model-value="fetchRecipes"
              variant="outlined"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <v-row v-if="recipes.length > 0">
      <v-col
        v-for="recipe in recipes"
        :key="recipe.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <RecipeCard :recipe="recipe" @edit="editRecipe" @delete="deleteRecipe" />
      </v-col>
    </v-row>
    
    <v-row v-else-if="loading">
      <v-col v-for="n in 8" :key="n" cols="12" sm="6" md="4" lg="3">
        <v-skeleton-loader
          type="card"
          class="mx-auto"
        ></v-skeleton-loader>
      </v-col>
    </v-row>
    
    <v-empty-state
      v-else
      headline
      :title="$t('recipes.noRecipes')"
      :text="$t('recipes.create')"
    ></v-empty-state>
    
    <v-pagination
      v-if="hasNext"
      v-model="page"
      :length="Infinity"
      @update:model-value="loadMore"
      class="justify-center mt-6"
    ></v-pagination>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { recipeApi } from '@/api/client'
import RecipeCard from '@/components/RecipeCard.vue'

const router = useRouter()
const { t } = useI18n()

const recipes = ref([])
const loading = ref(true)
const search = ref('')
const difficultyFilter = ref(null)
const cursor = ref(null)
const hasNext = ref(false)
const page = ref(1)

const difficultyItems = [
  { title: t('recipes.difficultyEasy'), value: 'easy' },
  { title: t('recipes.difficultyMedium'), value: 'medium' },
  { title: t('recipes.difficultyHard'), value: 'hard' }
]

let searchTimeout = null

const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    cursor.value = null
    recipes.value = []
    fetchRecipes()
  }, 500)
}

const fetchRecipes = async () => {
  loading.value = true
  try {
    const params = {
      limit: 12,
      search: search.value || undefined,
      difficulty: difficultyFilter.value || undefined
    }
    
    if (cursor.value) {
      params.cursor = cursor.value
    }
    
    const response = await recipeApi.get('/recipes/', { params })
    recipes.value = response.data
    hasNext.value = !!response.headers['x-next-cursor']
    cursor.value = response.headers['x-next-cursor'] || null
  } catch (error) {
    console.error('Error fetching recipes:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  if (cursor.value) {
    fetchRecipes()
  }
}

const editRecipe = (recipe) => {
  router.push({ name: 'edit-recipe', params: { id: recipe.id } })
}

const deleteRecipe = async (recipe) => {
  if (!confirm(t('recipes.deleteConfirm'))) return
  
  try {
    await recipeApi.delete(`/recipes/${recipe.id}`)
    recipes.value = recipes.value.filter(r => r.id !== recipe.id)
  } catch (error) {
    console.error('Error deleting recipe:', error)
  }
}

onMounted(() => {
  fetchRecipes()
})
</script>
