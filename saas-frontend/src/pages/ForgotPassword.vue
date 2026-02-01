<template>
  <div class="q-pa-md flex flex-center">
    <q-card style="width: 360px">
      <q-card-section>
        <div class="text-h6">Forgot Password</div>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="email"
          label="Email"
          type="email"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          label="Send Reset Link"
          color="primary"
          :loading="loading"
          @click="submit"
        />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { Notify } from 'quasar'

const email = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await api.post('/auth/forgot-password', { email: email.value })
    Notify.create({ type: 'positive', message: 'Reset link sent' })
  } catch {
    Notify.create({ type: 'negative', message: 'An error occurred. Please try again later.' })
  } finally {
    loading.value = false
  }
}
</script>
