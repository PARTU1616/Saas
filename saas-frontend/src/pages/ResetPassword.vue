<template>
  <div class="q-pa-md flex flex-center">
    <q-card style="width: 360px">
      <q-card-section>
        <div class="text-h6">Reset Password</div>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="password"
          label="New Password"
          type="password"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          label="Reset Password"
          color="primary"
          :loading="loading"
          @click="reset"
        />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'
import { Notify } from 'quasar'

const route = useRoute()
const router = useRouter()

const password = ref('')
const loading = ref(false)

async function reset() {
  loading.value = true
  try {
    await api.post('/auth/reset-password', {
      token: route.query.token,
      password: password.value
    })
    Notify.create({ type: 'positive', message: 'Password updated' })
    router.push('/login')
  } catch {
    Notify.create({ type: 'negative', message: 'Invalid or expired link' })
  } finally {
    loading.value = false
  }
}
</script>
