<template>
  <v-card class="recipe-card" hover>
    <v-card-media
      :src="recipe.image_path ? `/uploads/${recipe.image_path.replace('uploads/', '')}` : placeholder"
      height="200px"
      cover
    >
      <v-badge
        :content="difficultyLabel"
        :color="difficultyColor"
        location="top right"
        overlap
      >
      </v-badge>
    </v-card-media>
    
    <v-card-title class="text-body-1">
      {{ recipe.title }}
    </v-card-title>
    
    <v-card-text class="text-body-2 text-grey">
      <div class="d-flex align-center gap-2">
        <v-icon size="small" color="grey">mdi-clock-outline</v-icon>
        {{ recipe.cookingTime }} {{ $t('minutes') }}
      </div>
    </v-card-text>
    
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        variant="text"
        color="primary"
        @click="$emit('edit', recipe)"
        density="compact"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        variant="text"
        color="error"
        @click="$emit('delete', recipe)"
        density="compact"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  recipe: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'delete'])

const placeholder = 'https://via.placeholder.com/400x200?text=Cook+Book'

const difficultyLabel = computed(() => {
  const labels = {
    easy: t('recipes.difficultyEasy'),
    medium: t('recipes.difficultyMedium'),
    hard: t('recipes.difficultyHard')
  }
  return labels[props.recipe.difficulty] || props.recipe.difficulty
})

const difficultyColor = computed(() => {
  const colors = {
    easy: 'success',
    medium: 'warning',
    hard: 'error'
  }
  return colors[props.recipe.difficulty] || 'grey'
})
</script>

<style scoped>
.recipe-card {
  transition: transform 0.2s;
}

.recipe-card:hover {
  transform: translateY(-4px);
}

.gap-2 {
  gap: 8px;
}
</style>
