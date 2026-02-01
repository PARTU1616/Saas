<template>
  <div class="q-pa-md flex flex-center">
    <q-card style="width: 360px">
      <q-card-section>
        <div class="text-h6">Login</div>

      </q-card-section>

      <q-card-section>
        <q-input
          v-model="email"
          label="Email"
          type="email"
          dense
          outlined
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          dense
          outlined
          class="q-mt-md"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          label="Login"
          color="primary"
          :loading="loading"
          @click="submit"
        />
        <q-btn flat label="Forgot password?" to="/forgot-password" /> 
      </q-card-actions>

      <q-card-section v-if="error" class="text-negative">
        {{ error }}
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const auth = useAuthStore()
const router = useRouter()

const submit = async () => {
  loading.value = true
  error.value = ''

  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>
