<template>
  <div>
    <h1 class="text-h4 mb-6">{{ $t('favorites.title') }}</h1>
    
    <v-row v-if="favorites.length > 0">
      <v-col
        v-for="recipe in favorites"
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
      <v-col v-for="n in 4" :key="n" cols="12" sm="6" md="4" lg="3">
        <v-skeleton-loader
          type="card"
          class="mx-auto"
        ></v-skeleton-loader>
      </v-col>
    </v-row>
    
    <v-empty-state
      v-else
      headline
      :title="$t('favorites.empty')"
      :text="$t('recipes.title')"
    ></v-empty-state>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { recipeApi } from '@/api/client'
import RecipeCard from '@/components/RecipeCard.vue'

const router = useRouter()

const favorites = ref([])
const loading = ref(true)

const fetchFavorites = async () => {
  loading.value = true
  try {
    const response = await recipeApi.get('/favorites/')
    favorites.value = response.data
  } catch (error) {
    console.error('Error fetching favorites:', error)
  } finally {
    loading.value = false
  }
}

const editRecipe = (recipe) => {
  router.push({ name: 'edit-recipe', params: { id: recipe.id } })
}

const deleteRecipe = async (recipe) => {
  try {
    await recipeApi.delete(`/favorites/${recipe.id}`)
    favorites.value = favorites.value.filter(r => r.id !== recipe.id)
  } catch (error) {
    console.error('Error removing from favorites:', error)
  }
}

onMounted(() => {
  fetchFavorites()
})
</script>
